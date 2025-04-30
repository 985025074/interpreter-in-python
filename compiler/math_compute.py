from compiler.code import OpCode
from compiler.compiler_exception import CompilerException


def compute(left: int, right: int, operator: OpCode):
    match operator:
        case OpCode.ADD:
            return left + right
        case OpCode.SUB:
            return left - right
        case OpCode.MUL:
            return left * right
        case OpCode.DIV:
            return left // right
        case OpCode.GT:
            return left > right
        case OpCode.EQ:
            return left == right
        case OpCode.NOTEQ:
            return left != right
        case _:
            raise CompilerException(f"Invalid operator: {operator}")
