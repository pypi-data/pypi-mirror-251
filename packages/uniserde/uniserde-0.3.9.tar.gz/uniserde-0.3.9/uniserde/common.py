import inspect
import re
import types
from datetime import datetime
from typing import *  # type: ignore

from .objectid_proxy import ObjectId

Recur = Callable[[Any, Type], Any]
Serializer = Callable[[Any, Type, Recur], Any]
Deserializer = Callable[[Any, Type, Recur], Any]


_SPLIT_CAMEL_CASE_PATTERN = re.compile(
    ".+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)"
)


class SerdeError(Exception):
    """
    Signals an error during serialization or deserialization.
    """

    def __init__(self, user_message: str):
        self.user_message = user_message


def as_child(cls: Type) -> Type:
    """
    Marks the class to be serialized as one of its children. This will add an
    additional "type" field in the result, so the child can be deserialized
    properly.

    This decorator applies to children of the class as well, i.e. they will also
    be serialized with the "type" field.
    """
    assert inspect.isclass(cls), cls
    cls.__serde_serialize_as_child__ = cls  # type: ignore
    return cls


def should_serialize_as_child(cls: Type) -> bool:
    """
    Checks whether the given class should be serialized as a child, i.e. it, or
    any parent has been marked with the `as_child` decorator.
    """
    assert inspect.isclass(cls), cls
    return hasattr(cls, "__serde_serialize_as_child__")


def common_serialize(
    value: Any,
    value_type: Optional[Type],
    class_serializer: Serializer,
    serializers: Dict[Type, Serializer],
    user_serializers: Dict[Type, Callable[[Any], Any]],
) -> Any:
    # Find the type
    if value_type is None:
        value_type = type(value)

    # Is there a custom serializer for this class?
    try:
        serializer = user_serializers[value_type]
    except KeyError:
        pass
    else:
        return serializer(value)

    # Find a matching serializer
    key = get_origin(value_type)
    if key is None:
        key = value_type

    # Handle new-style unions
    if key is types.UnionType:
        key = Union

    try:
        serializer = serializers[key]
    except KeyError:
        if inspect.isclass(value_type):
            serializer = class_serializer
        else:
            raise ValueError(f"Unsupported field of type {value_type}") from None

    # Define the recursion function
    def recur(value: Any, value_type: Type) -> Any:
        return common_serialize(
            value,
            value_type,
            class_serializer,
            serializers,
            user_serializers,
        )

    # Apply it
    return serializer(value, value_type, recur)


def common_deserialize(
    value: Any,
    value_type: Type,
    class_deserializer: Serializer,
    deserializers: Dict[Type, Deserializer],
    user_deserializers: Dict[Type, Callable[[Any], Any]],
) -> Any:
    # Is there a custom deserializer for this class?
    try:
        deserializer = user_deserializers[value_type]
    except KeyError:
        pass
    else:
        return deserializer(value)

    # Find a matching deserializer
    key = get_origin(value_type)
    if key is None:
        key = value_type

    # Handle new-style unions
    if key is types.UnionType:
        key = Union

    try:
        deserializer = deserializers[key]
    except KeyError:
        if inspect.isclass(value_type):
            deserializer = class_deserializer
        else:
            raise ValueError(f"Unsupported field of type {value_type}") from None

    # Define the recursion function
    def recur(value: Any, value_type: Type) -> Any:
        return common_deserialize(
            value,
            value_type,
            class_deserializer,
            deserializers,
            user_deserializers,
        )

    # Apply it
    return deserializer(value, value_type, recur)


def all_subclasses(cls: Type, include_cls: bool) -> Iterable[Type]:
    """
    Yields all classes directly on indirectly inheriting from `cls`. Does not
    perform any sort of cycle checks.

    :param cls: The class to start from.
    :param include_cls: Whether to include `cls` itself in the results.
    """

    if include_cls:
        yield cls

    for subclass in cls.__subclasses__():
        yield from all_subclasses(subclass, include_cls=True)
