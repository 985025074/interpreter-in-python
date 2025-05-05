
from typing import Optional

from eval.object import *


def builtin_len(stringObj: Optional[String] = None):
    if stringObj is None:
        return Error("No string provided")
    if isinstance(stringObj, Array):
        return Integer(len(stringObj.elements))
    try:
        return Integer(len(stringObj.value))
    except Exception as e:
        return Error(str(e))


def builtin_first(arrayObj: Optional[Array] = None):
    if arrayObj is None:
        return Error("No array provided")
    if not isinstance(arrayObj, Array):
        return Error("Not an array")
    if len(arrayObj.elements) == 0:
        return Null()
    return arrayObj.elements[0]


def builtin_last(arrayObj: Optional[Array] = None):
    if arrayObj is None:
        return Error("No array provided")
    if not isinstance(arrayObj, Array):
        return Error("Not an array")
    if len(arrayObj.elements) == 0:
        return Null()
    return arrayObj.elements[-1]


def builtin_rest(arrayObj: Optional[Array] = None):
    if arrayObj is None:
        return Error("No array provided")
    if not isinstance(arrayObj, Array):
        return Error("Not an array")
    if len(arrayObj.elements) == 0:
        return Null()
    return Array(arrayObj.elements[1:])


def builtin_push(arrayObj: Optional[Array] = None, value: Optional[ycObject] = None):
    if arrayObj is None:
        return Error("No array provided")
    if not isinstance(arrayObj, Array):
        return Error("Not an array")
    if value is None:
        return Error("No value provided")
    newarray = Array(arrayObj.elements.copy())

    newarray.elements.append(value)
    return newarray


def builtin_print(value: Optional[ycObject] = None):
    if value is None:
        return Error("No value provided")
    print(value.inspect())
    return Null()


BuiltinFunction = [
    {"name": "len", "func": builtin_len},
    {"name": "first", "func": builtin_first},
    {"name": "last", "func": builtin_last},
    {"name": "rest", "func": builtin_rest},
    {"name": "push", "func": builtin_push},
    {"name": "print", "func": builtin_print},

]


class BuiltinWrapper:
    def __init__(self, name, func):
        self.name = name
        self.func = func

    @staticmethod
    def generate_from_index(index: int):
        return BuiltinWrapper(BuiltinFunction[index]["name"], BuiltinFunction[index]["func"])


def ret_index_builtin_func(name: str):
    for index, func in enumerate(BuiltinFunction):
        if func["name"] == name:
            return index
