from typing import List
from compiler.compiledfunction import CompiledFunction
from eval.object import ObjectType, ycObject


class Closure(ycObject):
    def __init__(self, compiled_function: CompiledFunction, free_variables: List[ycObject]):
        self.compiled_function = compiled_function
        self.free_variables = free_variables

    def type(self) -> ObjectType:
        return ObjectType.CLOSURE

    def inspect(self):
        return f"closure{self.compiled_function.instructions}"

    def __eq__(self, other):
        return isinstance(other, Closure) and self.compiled_function == other.compiled_function and self.free_variables == other.free_variables

    def __str__(self):
        return f"Closure({self.instructions})"
