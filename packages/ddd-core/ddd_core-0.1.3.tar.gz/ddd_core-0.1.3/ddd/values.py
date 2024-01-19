"""Implementation of Value Objects

They are inmutable. Other inmutable objects of domain are inside."""
from types import UnionType
from typing import Literal, Optional, Self, Union, get_args, get_origin


def _validate_hint(field_name, value, hint):
    def _explode_hint(hint, literals, types):
        operator = get_origin(hint)
        if operator is Literal:
            literals.extend(get_args(hint))
        elif operator in (UnionType, Union, Optional):
            for hint_ in get_args(hint):
                _explode_hint(hint_, literals, types)
        elif operator is None:
            types.append(hint)
        elif operator is list:
            types.append(list)
        else:
            raise TypeError(f"Operator {operator} not implemented")

    literals = []
    types = []
    _explode_hint(hint, literals, types)

    if not value in literals and not isinstance(value, tuple(types)):
        raise TypeError(
            f'Invalid type for "{field_name}". "{value}" no match expected {hint}'
        )


class _WithFields(type):
    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)
        cls._fields = {}
        for class_ in reversed(cls.mro()[:-1]):
            cls._fields.update(class_.__annotations__)


class Value(metaclass=_WithFields):
    """Value objects are inmutable."""

    __slots__ = ("_is_inmutable",)
    _fields = {}

    def __init__(self, *args, **kwargs):
        attrs, validate = self._cast_to_kwargs(args, kwargs)
        if validate:
            self._validate_attributes(attrs)

        for key, value in attrs.items():
            setattr(self, key, value)

        self._is_inmutable = True

    def _cast_to_kwargs(self, args, kwargs):
        validate = kwargs.pop("_validate", False)

        attrs = {}
        for name, value in zip(self._fields.keys(), args):
            attrs[name] = value

        attrs.update(kwargs)
        return attrs, validate

    @property
    def field_names(self):
        return list(self._fields.keys())

    def _validate_attributes(self, attrs):
        missed_fields = set(self._fields.keys()) - set(attrs.keys())
        for field in missed_fields:
            if not hasattr(self, field):
                raise ValueError(f'Misssed the field "{field}" when constructing')

        wrong_fields = set(attrs.keys()) - set(self._fields.keys())
        if wrong_fields:
            messages = []
            for field in wrong_fields:
                messages.append(
                    f'{self.__class__.__name__} has not field/s with name/s "{field}"'
                )
            raise AttributeError("\n".join(messages))

        for key, value in attrs.items():
            _validate_hint(key, value, self._fields[key])

        return attrs

    def as_dict(self):
        return self.__dict__.copy()

    def __setattr__(self, name: str, value: str):
        if hasattr(self, "_is_inmutable"):
            raise AttributeError("Value object is inmutable")
        super().__setattr__(name, value)

    def __hash__(self):
        all_values = [self.__class__.__name__]
        attrs = [getattr(self, name) for name in self._fields]
        for index, value in enumerate(attrs):
            if type(value) is list:
                attrs[index] = tuple(value)
        all_values.extend(attrs)
        return hash(tuple(all_values))

    def __eq__(self, other: Self) -> bool:
        return hash(self) == hash(other)

    def __repr__(self):
        args = []
        for name in self._fields.keys():
            args.append(f"{name}={getattr(self, name)}")

        all_args = ", ".join(args)
        return self.__class__.__name__ + "(" + all_args + ")"
