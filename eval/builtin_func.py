
from typing import Optional

from eval.object import *


def builtin_go(stringObj: Optional[String] = None):
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
    newarray = Array(arrayObj.elements)

    newarray.elements.append(value)
    return arrayObj


def builtin_print(value: Optional[ycObject] = None):
    if value is None:
        return Error("No value provided")
    print(value.inspect())
    return Null()


BuiltinFunction = {
    "len": Builtin(builtin_go),
    "first": Builtin(builtin_first),
    "last": Builtin(builtin_last),
    "rest": Builtin(builtin_rest),
    "push": Builtin(builtin_push),
    "print": Builtin(builtin_print),
}
