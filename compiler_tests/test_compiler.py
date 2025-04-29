from compiler.compiler import Compiler
from compiler.make import make
from compiler.code import OpCode
from eval.object import Integer
from lexer.lexer import Lexer
from parser.parser import Parser


code = [{
    "input": "1+2",
    "expected_constants": [Integer(1), Integer(2)],
    "expected_instructions": [
        make(OpCode.CONST, 0),
        make(OpCode.CONST, 1),
        make(OpCode.ADD),
    ]

}]


def test_compiler():
    for test in code:
        lexer = Lexer(test["input"])
        program = Parser(lexer).parse_program()
        compiler = Compiler()
        compiler.compile(program)
        # print(compiler.instructions)
        # print(compiler.bytecodes().constants)
        assert compiler.bytecodes().constants == test["expected_constants"]
        assert compiler.bytecodes(
        ).instructions == b''.join(test["expected_instructions"])
