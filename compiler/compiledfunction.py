from typing import List
from eval.object import ObjectType, ycObject


class CompiledFunction(ycObject):
    def __init__(self, instructions: bytes):

        self.instructions = instructions
        if isinstance(instructions, list):
            self.instructions = b''.join(instructions)
        self.value = instructions

    def type(self) -> ObjectType:
        return ObjectType.COMPILED_FUNCTION

    def inspect(self):
        return f"compiled function{self.instructions}"

    def __eq__(self, other):
        return isinstance(other, CompiledFunction) and self.instructions == other.instructions

    def __str__(self):
        return f"CompiledFunction({self.instructions})"

    @staticmethod
    def from_bytes_array(list: List[bytes]):
        return CompiledFunction(b''.join(list))
