from enum import Enum
from typing import Dict, List, TypedDict


class OpCode(Enum):
    CONST = 0
    PUSH = 1
    ADD = 2
    POP = 3
    SUB = 4
    MUL = 5
    DIV = 6
    TRUE = 7
    FALSE = 8
    GT = 9
    EQ = 10
    NOTEQ = 11
    BANG = 12
    MINUS = 13
    JUMP_IF_NOT_TRUE = 14
    JUMP = 15
    NULL = 16
    SETGLOBAL = 17
    GETGLOBAL = 18
    ARRAY = 19
    HASH = 20
    INDEX = 21
    RETURN = 22
    RETURN_NULL = 23
    CALL = 24
    SETLOCAL = 25
    GETLOCAL = 26
    LOAD_BUILTIN = 27
    GETCLOSURE = 28

    @property
    def bytes(self):
        return int.to_bytes(self.value, 1, byteorder='big')


class OpcodeInfoPair(TypedDict):
    name: str
    args_length: List[int]


OpCodeInfo: Dict[OpCode, OpcodeInfoPair] = {
    OpCode.CONST: {"name": "CONST", "args_length": [2]},
    OpCode.POP: {"name": "POP", "args_length": []},
    # arithmetic
    OpCode.ADD: {"name": "ADD", "args_length": []},
    OpCode.SUB: {"name": "SUB", "args_length": []},
    OpCode.MUL: {"name": "MUL", "args_length": []},
    OpCode.DIV: {"name": "DIV", "args_length": []},
    OpCode.TRUE: {"name": "TRUE", "args_length": []},
    OpCode.FALSE: {"name": "FALSE", "args_length": []},
    OpCode.GT: {"name": "GT", "args_length": []},
    OpCode.EQ: {"name": "EQ", "args_length": []},
    OpCode.NOTEQ: {"name": "NOTEQ", "args_length": []},
    OpCode.BANG: {"name": "BANG", "args_length": []},
    OpCode.MINUS: {"name": "MINUS", "args_length": []},
    OpCode.JUMP_IF_NOT_TRUE: {"name": "JUMP_IF_NOT_TRUE", "args_length": [2]},
    OpCode.JUMP: {"name": "JUMP", "args_length": [2]},
    OpCode.NULL: {"name": "NULL", "args_length": []},
    OpCode.SETGLOBAL: {"name": "SETGLOBAL", "args_length": [2]},
    OpCode.GETGLOBAL: {"name": "GETGLOBAL", "args_length": [2]},
    OpCode.ARRAY: {"name": "ARRAY", "args_length": [2]},
    OpCode.HASH: {"name": "HASH", "args_length": [2]},
    OpCode.INDEX: {"name": "INDEX", "args_length": []},
    OpCode.RETURN: {"name": "RETURN", "args_length": []},
    OpCode.CALL: {"name": "CALL", "args_length": [1]},
    OpCode.RETURN_NULL: {"name": "RETURN_NULL", "args_length": []},
    OpCode.SETLOCAL: {"name": "SETLOCAL", "args_length": [2]},
    OpCode.GETLOCAL: {"name": "GETLOCAL", "args_length": [2]},
    OpCode.LOAD_BUILTIN: {"name": "LOAD_BUILTIN", "args_length": [1]},
    OpCode.GETCLOSURE: {"name": "GETCLOSURE", "args_length": [2,1]},
    
}