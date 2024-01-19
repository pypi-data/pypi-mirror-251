"""Implement core of ddd: entity & aggregates"""

import abc
import uuid
from typing import Callable, Self

from .values import Value


class Id(Value):
    """Unique identification for a entity."""

    uuid: uuid.UUID

    @classmethod
    def create_randomly(cls):
        return cls(uuid.uuid4())

    @classmethod
    def create_from_key(cls, value: str):
        """Construct a Identificator from key values."""
        concatenated_keys = ".".join([cls.__name__, value])
        return cls(uuid.uuid5(uuid.NAMESPACE_DNS, concatenated_keys))

    @property
    def aggregate_name(self):
        return self.__class__.__name__[:-2]


class _Attribute:
    def __init__(self, name, default=None):
        self.name = name
        self._name = "_" + name
        self._default = default

    def __get__(self, entity, objtype):
        if objtype is None:
            return self
        else:
            if not hasattr(entity, self._name):
                setattr(entity, self._name, self._default)

            return getattr(entity, self._name)

    def __set__(self, obj, val):
        raise AttributeError(
            f"Attribute {self.name} is not writable directly, use methods!"
        )


class Entity:
    """Implementation of Entity following ddd."""

    def __init__(self):
        if hasattr(type(self), "_with_descriptors"):
            return

        fields = list(type(self).__annotations__.keys())
        if "id" not in fields:
            raise AttributeError("Always an Entity shall have id attribute!!")

        for name in fields:
            default_value = None
            if hasattr(Entity, name):
                default_value = getattr(self, name)
            setattr(Entity, name, _Attribute(name, default_value))

        type(self)._with_descriptors = True
        self._id = None

    def __eq__(self, other: Self) -> bool:
        return self.id == other.id

    def __hash__(self):
        return hash(self.id) ^ hash(self.__class__.__qualname__)


class Event(Value):
    """Domain event triggered by an aggregate."""

    level: int

    def header(self, aggregate: "Aggregate") -> str:
        key = aggregate.key if aggregate.key else str(aggregate.id.uuid)
        return f"{self.__class__.__name__}@{aggregate.__class__.__name__}[{key}]"

    def message(self, aggregate: "Aggregate") -> str:
        """Human readable message for debugging purposes."""
        return self.header(aggregate)


class ChangeEvent(Event):
    """Event raised when the aggregate changes its internal state"""

    def __init__(self, *args, **kwargs):
        super().__init__(0, *args, **kwargs)

    def apply_on(self, _):
        """Apply event to aggregate updating its internal state."""
        raise NotImplementedError(f'Method "apply_on" shall be implemented!!')


class WarningEvent(Event):
    """Critical event which should not stop the application."""

    def __init__(self, *args, **kwargs):
        super().__init__(4, *args, **kwargs)


class ExceptionEvent(Event):
    """Critical event which should stop the application."""

    def __init__(self, *args, **kwargs):
        super().__init__(5, *args, **kwargs)


class Aggregate(Entity, metaclass=abc.ABCMeta):
    """Aggregate of domain, keeps integrity on domain transactions."""

    id: Id
    key: str

    def __init__(self):
        Entity.__init__(self)
        self._history = []
        self._callbacks = []
        self._key = ""

    def notify_event(self, event: Event):
        for callback, level in self._callbacks:
            if level is not None and event.level < level:
                continue
            callback(event, self)

    def apply_change(self, event: ChangeEvent):
        """Apply change in aggregate defined by the event change."""
        event.apply_on(self)
        self._history.append(event)
        self.notify_event(event)

    def add_event_observer(
        self, callback: Callable[[Event, Self], None], level: int = 0
    ):
        """Add event observer to aggregate when an event is raised."""
        if (callback, level) in self._callbacks:
            return

        if level == 0:
            for event in self._history:
                callback(event, self)

        self._callbacks.append((callback, level))


class BusinessException(Exception):
    """Exception due to a break in business rule."""

    def __init__(self, aggregate: Aggregate, event: ExceptionEvent):
        self.aggregate = aggregate
        self.event = event

        super().__init__(event.message(aggregate))
