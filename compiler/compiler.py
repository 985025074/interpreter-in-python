from typing import List
from compiler.code import OpCode
from compiler.make import make, print_bytecode
from eval.object import Integer, ycObject
from lexer.token import TokenTypes
from parser.node import BlockStatement, BooleanLiteral, ExpressionStatement, IfExpression, InfixExpression, IntegerLiteral, Node, PreFixExpression, Program


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
        self.byteslen = 0
        self.last_instruction = b''
        self.previous_instruction = b''
        pass

    def bytecodes(self):
        return Bytecode(constants=self.constants, instructions=self.instructions)

    def add_const(self, obj: ycObject):
        self.constants.append(obj)
        return len(self.constants) - 1

    def add_instruction(self, op_code: OpCode, *args):
        self.instructions.append(make(op_code, *args))
        self.previous_instruction = self.last_instruction
        self.last_instruction = self.instructions[-1]
        self.byteslen += len(self.instructions[-1])
        return len(self.instructions) - 1

    def compile(self, node: Node | None):
        try:
            # go through the ast tree and add instructions to the bytecode
            if type(node) == Program:
                for statement in node.statements:
                    self.compile(statement)
            elif type(node) == ExpressionStatement:
                self.compile(node.expression)
                self.add_instruction(OpCode.POP)
            elif type(node) == InfixExpression:
                if node.token.TokenType == TokenTypes.LT:  # type:ignore
                    self.compile(node.right)
                    self.compile(node.left)
                else:
                    self.compile(node.left)
                    self.compile(node.right)
                match node.token.TokenType:  # type: ignore
                    case TokenTypes.PLUS:
                        self.add_instruction(OpCode.ADD)
                    case TokenTypes.MINUS:
                        self.add_instruction(OpCode.SUB)
                    case TokenTypes.SLASH:
                        self.add_instruction(OpCode.DIV)
                    case TokenTypes.ASTERISK:
                        self.add_instruction(OpCode.MUL)
                    case TokenTypes.GT | TokenTypes.LT:
                        self.add_instruction(OpCode.GT)
                    case TokenTypes.EQ:
                        self.add_instruction(OpCode.EQ)
                    case TokenTypes.NOT_EQ:
                        self.add_instruction(OpCode.NOTEQ)
                    case _:
                        pass
            elif type(node) == IntegerLiteral:
                integer_obj = Integer(value=node.value)
                index = self.add_const(integer_obj)
                self.add_instruction(OpCode.CONST, index)
            elif type(node) == BooleanLiteral:
                if node.value:
                    self.add_instruction(OpCode.TRUE)
                else:
                    self.add_instruction(OpCode.FALSE)
            elif type(node) == PreFixExpression:
                match node.token.TokenType:  # type: ignore
                    case TokenTypes.BANG:
                        self.compile(node.right)
                        self.add_instruction(OpCode.BANG)
                    case TokenTypes.MINUS:
                        self.compile(node.right)
                        self.add_instruction(OpCode.MINUS)
            elif type(node) == IfExpression:
                self.compile(node.condition)
                first_jump_loc = self.add_instruction(
                    OpCode.JUMP_IF_NOT_TRUE, 9999)
                self.compile(node.true_branch)
                if self.last_instruction[0] == OpCode.POP.bytes[0]:
                    # move the last pop sentence
                    self.instructions.pop()
                    self.byteslen -= len(self.last_instruction)

                second_jump_loc = self.add_instruction(OpCode.JUMP, 999)
                self.instructions[first_jump_loc] = make(
                    OpCode.JUMP_IF_NOT_TRUE, self.byteslen)
                if node.false_branch is None:
                    self.add_instruction(OpCode.NULL)
                else:
                    self.compile(node.false_branch)
                    if self.last_instruction[0] == OpCode.POP.bytes[0]:
                        # move the last pop sentence
                        self.instructions.pop()
                        self.byteslen -= len(self.last_instruction)

                self.instructions[second_jump_loc] = make(
                    OpCode.JUMP, self.byteslen)

            elif type(node) == BlockStatement:
                for statement in node.statements:
                    self.compile(statement)

        except Exception as e:
            print(f"Error compiling: {e}")
            raise e
        return
