"""Interfaces of common infrastructures used for connecting to core ddd"""
import abc
from typing import Callable

from .aggregates import Aggregate, Event, Id


class AggregateNotFound(Exception):
    """Aggregate is not found in persistence infrastructure"""


class EventBusClient(abc.ABC):
    """Event broker for publishing and receiving domain events and business exceptions."""

    @abc.abstractmethod
    async def publish(self, event: Event, aggregate: Aggregate, command_name: str):
        """Publish to the event bus an event raised by an aggregate while executing a command defined by its name."""

    @abc.abstractmethod
    async def subscribe(self, callback: Callable, **filters):
        """Subscribe to event bus for recieving events and the aggregate id who triggered it."""


class Store(abc.ABC):
    """Very light version of Repository, removing queries"""

    @abc.abstractmethod
    async def load(self, aggregate_id: Id) -> Aggregate:
        """Load from persistence layer an aggregate"""

    @abc.abstractmethod
    async def save(self, aggregate_id: Id) -> None:
        """Persist an aggregate"""


class Projection(abc.ABC):
    """Read from persistence layer queries about domain"""
