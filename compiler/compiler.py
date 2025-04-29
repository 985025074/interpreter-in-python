from typing import List
from compiler.code import OpCode
from compiler.make import make, print_bytecode
from eval.object import Integer, ycObject
from lexer.token import TokenTypes
from parser.node import ExpressionStatement, InfixExpression, IntegerLiteral, Node, Program


class Bytecode:
    def __init__(self, constants: List[ycObject] = [], instructions: List[bytes] = []) -> None:
        self.constants: List[ycObject] = constants
        self.instructions: bytes = b''.join(instructions)
        pass

    def to_string(self):
        return print_bytecode(self.instructions)


class Compiler:
    def __init__(self,) -> None:
        self.constants: List[ycObject] = []
        self.instructions: List[bytes] = []
        pass

    def bytecodes(self):
        return Bytecode(constants=self.constants, instructions=self.instructions)

    def add_const(self, obj: ycObject):
        self.constants.append(obj)
        return len(self.constants) - 1

    def add_instruction(self, op_code: OpCode, *args):
        self.instructions.append(make(op_code, *args))

    def compile(self, node: Node | None):
        try:
            # go through the ast tree and add instructions to the bytecode
            if type(node) == Program:
                for statement in node.statements:
                    self.compile(statement)
            elif type(node) == ExpressionStatement:
                self.compile(node.expression)
            elif type(node) == InfixExpression:
                self.compile(node.left)
                self.compile(node.right)
                match node.token.TokenType:  # type: ignore
                    case TokenTypes.PLUS:
                        self.add_instruction(OpCode.ADD)
                        pass
            elif type(node) == IntegerLiteral:
                integer_obj = Integer(value=node.value)
                index = self.add_const(integer_obj)
                self.add_instruction(OpCode.CONST, index)
        except Exception as e:
            print(f"Error compiling: {e}")
        return
