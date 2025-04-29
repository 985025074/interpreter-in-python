from enum import Enum
from typing import Dict, List, TypedDict


class OpCode(Enum):
    CONST = 0
    PUSH = 1
    ADD = 2

    @property
    def bytes(self):
        return int.to_bytes(self.value, 1, byteorder='big')


class OpcodeInfoPair(TypedDict):
    name: str
    args_length: List[int]


OpCodeInfo: Dict[OpCode, OpcodeInfoPair] = {
    OpCode.CONST: {"name": "CONST", "args_length": [2]},
    OpCode.ADD: {"name": "ADD", "args_length": []}

}
