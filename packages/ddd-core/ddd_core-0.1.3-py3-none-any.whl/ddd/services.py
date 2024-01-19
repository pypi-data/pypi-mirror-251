"""Implementation of services using a CQRS approach"""

import abc
import asyncio
import importlib
import inspect
import re
from typing import Any, Type

from .aggregates import Aggregate, BusinessException
from .infra import EventBusClient
from .values import Value


class DataTransfer(Value):
    """Base class for all data transfer object to answer the queries to services"""

    def to_jsonable_dict(self):
        raise NotImplementedError()


class Query(Value):
    """Interface for a Command patterns implementing any query."""

    async def fetch(self, _: "Service") -> DataTransfer:
        """Return the results of a query done to the service."""
        raise NotImplementedError()


class Command(Value):
    """Interface for a Command pattern."""

    async def execute(self, _: "Service"):
        """Execute a command using the injected service."""
        raise NotImplementedError()


class Service(abc.ABC):
    _loop = asyncio.new_event_loop()

    def __init__(
        self,
        event_bus_client: EventBusClient | None = None,
        commands_module_name: str = ".",
        validate: bool = False,
    ):
        self._fry = CommandFactory(self.__class__, commands_module_name, validate)
        self.event_bus_client = event_bus_client
        self._tasks = {}

    @property
    def all_command_names(self):
        return self._fry.all_command_names

    @property
    def all_query_names(self):
        return self._fry.all_query_names

    async def execute(self, command_name: str, *args, **kwargs) -> None:
        """Execute command."""
        command = self._fry.create_command(command_name, *args, **kwargs)

        return await command.execute(self)

    async def fetch(self, query_name: str, **query_filter) -> Any:
        """Execute query and return its result to client."""
        query: Query = self._fry.create_query(query_name, **query_filter)
        return await query.fetch(self)

    def observe_events(self, aggregate: Aggregate, command_name: str, level: int = 0):
        if not self.event_bus_client:
            return

        def callback(event, aggregate_):
            loop = asyncio.get_running_loop()

            self._tasks[command_name].append(
                loop.create_task(
                    self.event_bus_client.publish(event, aggregate_, command_name)
                )
            )

            if event.level == 5:
                raise BusinessException(aggregate, event)

        if not command_name in self._tasks:
            self._tasks[command_name] = []

        aggregate.add_event_observer(callback, level)

    async def assure_events_are_published(self, command_name: str):
        if command_name not in self._tasks:
            return

        tasks = self._tasks[command_name]
        self._tasks[command_name] = []

        await asyncio.gather(*tasks)

    def execute_syncronous(self, command_name: str, *args, **kwargs) -> None:
        """Execute command syncronously for syncronous clients."""
        if Service._loop.is_closed():
            Service._loop = asyncio.new_event_loop()

        result = self._loop.run_until_complete(
            self.execute(command_name, *args, **kwargs)
        )
        return result

    def fetch_syncronous(self, query_name: str, **query_filter) -> Any:
        """Execute query syncronously for syncronous clients."""
        if Service._loop.is_closed():
            Service._loop = asyncio.new_event_loop()

        result = self._loop.run_until_complete(self.fetch(query_name, **query_filter))
        return result


def _to_snake_case(camel_case):
    return re.sub(r"(?<!^)(?=[A-Z])", "_", camel_case).lower()


class CommandFactory:
    """Create commands for use of service"""

    def __init__(
        self,
        service_class: Type[Service],
        module_name: str = ".",
        validate: bool = False,
    ):
        self._service_class = service_class
        module_name = service_class.__module__ if module_name == "." else module_name
        self._validate = validate

        self._set_all_commands(module_name)

    def _set_all_commands(self, module_name):
        def has_compatible_method(value, method_name):
            return (
                hasattr(value, method_name)
                and "service" in getattr(value, method_name).__annotations__
                and getattr(value, method_name).__annotations__["service"]
                is self._service_class
            )

        def predicate(value):
            condition = (
                inspect.isclass(value)
                and value not in (Query, Command)
                and issubclass(value, (Query, Command))
                and (
                    has_compatible_method(value, "fetch")
                    or has_compatible_method(value, "execute")
                )
            )
            return condition

        command_module = importlib.import_module(module_name)

        self._commands = {}
        members = inspect.getmembers(command_module, predicate=predicate)
        for member in members:
            name = _to_snake_case(member[0])
            if "command" == name[-7:] or "query" == name[-5:]:
                name = name[: name.rfind("_")]
            self._commands[name] = member[1]

    @property
    def all_command_names(self):
        return [
            key for key, value in self._commands.items() if issubclass(value, Command)
        ]

    @property
    def all_query_names(self):
        return [
            key for key, value in self._commands.items() if issubclass(value, Query)
        ]

    def create_command(self, command_name, *args, **kwargs) -> Command:
        if command_name not in self.all_command_names:
            raise ValueError(
                f'"{command_name}" command is not available for service "{self._service_class.__name__}"'
            )

        CommandClass = self._commands[command_name]
        if self._validate:
            kwargs["_validate"] = True

        return CommandClass(*args, **kwargs)

    def create_query(self, query_name, **kwargs) -> Query:
        if query_name not in self.all_query_names:
            raise ValueError(
                f'"{query_name}" query is not available for service "{self._service_class.__name__}"'
            )

        QueryClass = self._commands[query_name]
        if self._validate:
            kwargs["_validate"] = True

        return QueryClass(**kwargs)
