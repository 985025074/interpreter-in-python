
from typing import List, Optional
from compiler.code import OpCode
from compiler.compiledfunction import CompiledFunction
from compiler.compiler_exception import CompilerException
from compiler.make import make, print_bytecode
from compiler.symtable import Scope, SymTable, ycSymbol
from eval.object import Integer, String, ycObject
from lexer.token import TokenTypes
from parser.node import ArrayExpression, BlockStatement, BooleanLiteral, ExpressionStatement, FunctionLiteral, HashLiteral, Identifier, IfExpression, IndexExpression, InfixExpression, IntegerLiteral, LetStatement, Node, PreFixExpression, Program, ReturnStatement, StringLiteral


class Bytecode:
    def __init__(self, constants: Optional[List[ycObject]] = None, instructions: Optional[List[bytes]] = None) -> None:
        self.constants: List[ycObject] = constants.copy() if constants is not None else [
        ]
        self.instructions: bytes = b''.join(
            instructions) if instructions is not None else b''

    def to_string(self):
        return print_bytecode(self.instructions)

    def __str__(self):
        return self.to_string()


class CompileScope:
    def __init__(self):
        self.instructions: List[bytes] = []
        self.last_instruction = b''
        self.previous_instruction = b''
        self.byteslen = 0


class Compiler:
    def __init__(self,) -> None:
        self.constants: List[ycObject] = []
        self.scopes = [CompileScope()]
        self.scope_index = 0
        self.symtable = SymTable()
        pass

    def bytecodes(self):
        return Bytecode(constants=self.constants, instructions=self.instructions)

    def add_const(self, obj: ycObject):
        self.constants.append(obj)
        return len(self.constants) - 1

    def enter_scope(self):
        self.scope_index += 1
        self.scopes.append(CompileScope())

    def leave_scope(self):
        self.scope_index -= 1
        scope = self.scopes.pop()
        return b''.join(scope.instructions)

    @property
    def instructions(self):
        return self.scopes[self.scope_index].instructions

    @instructions.setter
    def instructions(self, instructions):
        self.scopes[self.scope_index].instructions = instructions

    @property
    def last_instruction(self):
        return self.scopes[self.scope_index].last_instruction

    @last_instruction.setter
    def last_instruction(self, last_instruction):
        self.scopes[self.scope_index].last_instruction = last_instruction

    @property
    def previous_instruction(self):
        return self.scopes[self.scope_index].previous_instruction

    @previous_instruction.setter
    def previous_instruction(self, previous_instruction):
        self.scopes[self.scope_index].previous_instruction = previous_instruction

    @property
    def byteslen(self):
        return self.scopes[self.scope_index].byteslen

    @byteslen.setter
    def byteslen(self, byteslen):
        self.scopes[self.scope_index].byteslen = byteslen

    def add_instruction(self, op_code: OpCode, *args):
        self.instructions.append(make(op_code, *args))
        self.last_instruction = self.instructions[-1]
        self.previous_instruction = self.instructions[-2] if len(
            self.instructions) > 1 else b''
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
            elif type(node) == StringLiteral:
                string_obj = String(node.value)
                index = self.add_const(string_obj)
                self.add_instruction(OpCode.CONST, index)
            elif type(node) == ArrayExpression:
                if node.elements is not None:
                    for element in node.elements:
                        self.compile(element)
                    self.add_instruction(OpCode.ARRAY, len(node.elements))
                else:
                    self.add_instruction(OpCode.ARRAY, 0)
            elif type(node) == HashLiteral:
                if node.raw_keys is not None and node.raw_values is not None:
                    for k, v in zip(node.raw_keys, node.raw_values):
                        self.compile(k)
                        self.compile(v)
                    self.add_instruction(OpCode.HASH, len(node.raw_keys) * 2)
                else:
                    self.add_instruction(OpCode.HASH, 0)
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
            elif type(node) == LetStatement:
                self.compile(node.right_expression)

                sym = self.symtable.add_symbol(
                    node.identifier.value, Scope.GLOBAL)

                self.add_instruction(OpCode.SETGLOBAL, sym.index)
            elif type(node) == Identifier:
                sym = self.symtable.resolve_symbol(node.value)
                if sym is None:
                    raise CompilerException(
                        f"Identifier {node.value} not found in symbol table")
                else:
                    assert isinstance(sym, ycSymbol)
                    self.add_instruction(OpCode.GETGLOBAL, sym.index)
            elif type(node) == IndexExpression:
                self.compile(node.left)
                self.compile(node.index)
                self.add_instruction(OpCode.INDEX)
            elif type(node) == FunctionLiteral:
                self.enter_scope()
                self.compile(node.body)
                ins = self.leave_scope()

                self.add_const(CompiledFunction(ins))
                self.add_instruction(OpCode.CONST, len(self.constants) - 1)
            elif type(node) == ReturnStatement:
                if node.return_value is not None:
                    self.compile(node.return_value)
                else:
                    pass
                self.add_instruction(OpCode.RETURN)

        except Exception as e:
            # print(f"Error compiling: {e}")
            raise CompilerException(f"{e}")
        return
