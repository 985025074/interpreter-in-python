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
}
