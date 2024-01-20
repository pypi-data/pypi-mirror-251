from typing import Callable
from enum import Enum, auto

from ._key_extractor import default_dict_key_extractor
from ._basic import list_to_dict, extend_list


class DifferenceType(Enum):
    TYPE = auto()
    MISSING = auto()
    NOT_EQUAL = auto()

class DifferencePointer(Enum):
    A = auto()
    B = auto()


class Field:

    __slots__ = ("name",)

    def __init__(self, name) -> None:
        self.name = name


class Difference:

    __slots__ = (
        "key", "type", "pointer", "value_a", "value_b", "references"
    )

    def __init__(
        self,
        key: list[str],
        type: DifferenceType,
        pointer: DifferencePointer = None,
        value_a = None,
        value_b = None,
        references: list = None
    ) -> None:
        self.key = key
        self.type = type
        self.pointer = pointer
        self.value_a = value_a
        self.value_b = value_b
        self.references = references

    @property
    def key_str(self):
        return ".".join(self.key)

    def __repr__(self) -> str:
        return f"{self.type} {self.key_str} {self.value_a}!={self.value_b}"

    def __eq__(self, other) -> bool:
        if isinstance(other, str):
            return repr(self) == other
        return (
            type(self) == type(other)
            and repr(self) == repr(other)
        )

    def build_dict(self) -> dict:
        current = {"type": self.type}
        if self.value_a: current["value_a"] = self.value_a
        if self.value_b: current["value_b"] = self.value_b
        if self.pointer: current["pointer"] = self.pointer

        for key in reversed(self.key):
            if key.startswith("[") and key.endswith("]"):
                rtn = []
                index = key[1:-1]
                if index.isnumeric():
                    index = int(index)
                    extend_list(rtn, index)
                    rtn[index] = current
                else:
                    key, value = index.split(":")
                    rtn.append({key: value} | (current or {}))
                current = rtn
            else:
                current = {key: current}
        return current
                
def get_index(entry: dict, *index_keys) -> str:
    for index_key in index_keys:
        if index := entry.get(index_key):
            return index

def compare(
    data_a,
    data_b,
    current_key: list[str] = None,
    ignore_keys: list[list[str]] = None,
    key_extractors: list[Callable] = [default_dict_key_extractor],
):

    if current_key and ignore_keys and current_key in ignore_keys:
        return

    if data_a == data_b:
        return

    if not current_key:
        current_key = []

    type_a = type(data_a)
    type_b = type(data_b)

    if type_a != type_b:
        yield Difference(
            current_key,
            DifferenceType.TYPE,
            type_a,
            type_b
        )
        return

    if data_a == data_b:
        return

    if type_a == dict:
        keys_a = data_a.keys()
        keys_b = data_b.keys()

        for key in keys_a:
            if not key in keys_b:
                yield Difference(
                    current_key + [key],
                    DifferenceType.MISSING,
                    DifferencePointer.B
                )

        for key in keys_b:
            if not key in keys_a:
                yield Difference(
                    current_key + [key],
                    DifferenceType.MISSING,
                    DifferencePointer.A
                )
            else:
                yield from compare(
                    data_a[key], data_b[key], current_key + [key])
    elif type_a == list:
        list_a = list_to_dict(data_a, key_extractors)
        list_b = list_to_dict(data_b, key_extractors)
        yield from compare(list_a, list_b, current_key)
    else:
        yield Difference(
            current_key,
            DifferenceType.NOT_EQUAL,
            value_a = data_a,
            value_b = data_b
        )
