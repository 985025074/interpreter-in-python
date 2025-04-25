from abc import abstractmethod, ABC
from enum import Enum
from typing import Dict, List

from eval.env import Environment
from lexer.token import Token, TokenTypes
from parser.node import BlockStatement, BooleanLiteral, Identifier, IntegerLiteral, Node, StringLiteral


class ObjectType(Enum):
    INTEGER = "INTEGER"
    BOOLEAN = "BOOLEAN"
    NULL = "NULL"
    RETURN = "RETURN"
    ERROR = "ERROR"
    FUNCTION = "FUNCTION"
    STRING = "STRING"
    BUILTIN = "BUILTIN"
    ARRAY = "ARRAY"
    HASH = "HASH"
    QUOTE = "QUOTE"
    MACRO = "MACRO"


class ycObject(ABC):
    @abstractmethod
    def type(self) -> ObjectType:
        pass

    @abstractmethod
    def inspect(self):
        pass

    def __eq__(self, other):
        return self.inspect() == other.inspect()


class HashKey:
    def __init__(self, type_: ObjectType, value: str | int | bool):
        self.type = type_
        self.value = hash(value)

    def __eq__(self, other):
        return self.type == other.type and self.value == other.value

    def __hash__(self):
        return self.value


class HashAble(ABC):
    def hash_key(self) -> HashKey:
        return HashKey(self.type(), self.value)


class HashPair:
    def __init__(self, key: ycObject, value: ycObject):
        self.key = key
        self.value = value

    def __eq__(self, other):
        return self.key == other.key and self.value == other.value


class Hash(ycObject):
    def __init__(self, pairs: Dict[HashKey, HashPair]):
        self.pairs = pairs

    def type(self):
        return ObjectType.HASH

    def inspect(self):
        return {v.key.inspect(): v.value.inspect() for k, v in self.pairs.items()}

    def __str__(self):
        return str(self.inspect())


class Integer(ycObject, HashAble):
    def __init__(self, value: int):
        self.value = value

    def type(self):
        return ObjectType.INTEGER

    def inspect(self):
        return self.value

    def __str__(self):
        return str(self.value)


class String(ycObject, HashAble):
    def __init__(self, value: int):
        self.value = value

    def type(self):
        return ObjectType.STRING

    def inspect(self):
        return self.value

    def __str__(self):
        return str(self.value)


class Boolean(ycObject, HashAble):
    def __init__(self, value: bool):
        self.value = value

    def type(self):
        return ObjectType.BOOLEAN

    def inspect(self):
        return self.value

    def __str__(self):
        return str(self.value)


class Null(ycObject):
    def __init__(self):
        pass

    def type(self):
        return ObjectType.NULL

    def inspect(self):
        return "Null"

    def __str__(self):
        return "Null"


class ReturnObject(ycObject):
    def __init__(self, value: ycObject):
        self.value = value

    def type(self):
        return ObjectType.RETURN

    def inspect(self):
        return self.value.inspect()

    def __str__(self):
        return str(self.value)


class Error(ycObject):
    def __init__(self, msg: str):
        self.error_mssage = msg

    def type(self):
        return ObjectType.ERROR

    def inspect(self):
        return self.error_mssage

    def __str__(self):
        return self.inspect()


class Function(ycObject):
    def __init__(self, params: List[Identifier], body: BlockStatement, env: Environment):
        self.params = params
        self.body = body
        self.env = env

    def type(self):
        return ObjectType.FUNCTION

    def inspect(self):
        return "function(params:{}, body:{}, env:{})".format(self.params, self.body, self.env)

    def __str__(self):
        return self.inspect()


class Builtin(ycObject):
    def __init__(self, fn):
        self.fn = fn

    def type(self):
        return ObjectType.BUILTIN

    def inspect(self):
        return "builtin function"

    def __str__(self):
        return self.inspect()


class Array(ycObject):

    def __init__(self, elements: List[ycObject]):
        self.elements = elements

    def type(self):
        return ObjectType.ARRAY

    def inspect(self):
        return [x.inspect() for x in self.elements]

    def __str__(self):
        return str(self.inspect())


class Quote(ycObject):
    def __init__(self, node: Node):
        self.node = node

    def type(self):
        return ObjectType.QUOTE

    def inspect(self):
        return "QUOTE({})".format(self.node)

    def __str__(self):
        return self.inspect()


class MacroObject(ycObject):
    def __init__(self, params: List[Identifier], body: BlockStatement, env: Environment):
        self.params = params
        self.body = body
        self.env = env

    def type(self):
        return ObjectType.MACRO

    def inspect(self):
        return "Macro(params:{}, body:{}, env:{})".format(self.params, self.body, self.env)

    def __str__(self):
        return self.inspect()


def turnObjectToNode(obj: ycObject):
    if obj.type() == ObjectType.INTEGER:
        return IntegerLiteral(Token(TokenTypes.INT, str(obj.inspect())))
    elif obj.type() == ObjectType.STRING:
        return StringLiteral(Token(TokenTypes.STRING, str(obj.inspect())))
    elif obj.type() == ObjectType.BOOLEAN:
        return BooleanLiteral(Token(TokenTypes.TRUE if obj.inspect() else TokenTypes.FALSE, str(obj.inspect())))
    elif obj.type() == ObjectType.QUOTE:
        return obj.node
    else:
        return None
