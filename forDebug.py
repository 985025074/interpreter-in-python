from compiler.code import OpCode
from compiler.compiler import Compiler
from compiler.make import make
from eval.object import Integer
from lexer.lexer import Lexer
from parser.parser import Parser


test = {
    "input": "if (true){ 10 };3333",
    "expected_constants": [Integer(10), Integer(3333)],
    "expected_instructions": [
        # 0000
        make(OpCode.TRUE),
        # 0001
        make(OpCode.JUMP_IF_NOT_TRUE, 10),
        # 0004
        make(OpCode.CONST, 0),
        # 0007
        make(OpCode.JUMP, 11),
        # 0010
        make(OpCode.NULL),
        # 0011
        make(OpCode.POP),
        # 0012
        make(OpCode.CONST, 1),
        # 0015
        make(OpCode.POP),
    ],

}

print(test["expected_instructions"])
print(b''.join(test["expected_instructions"]))