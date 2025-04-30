import pytest
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
            make(OpCode.POP),
        ]

        },

        {
        "input": "1;2",
        "expected_constants": [Integer(1), Integer(2)],
        "expected_instructions": [
            make(OpCode.CONST, 0),
            make(OpCode.POP),
            make(OpCode.CONST, 1),
            make(OpCode.POP),
        ]
        },
        {
        "input": "1;",
        "expected_constants": [Integer(1)],
        "expected_instructions": [
            make(OpCode.CONST, 0),
            make(OpCode.POP),
        ]
        },
        {
        "input": "true;",
        "expected_constants": [],
        "expected_instructions": [
            make(OpCode.TRUE),
            make(OpCode.POP),
        ]
        },
        {
        "input": "!true;",
        "expected_constants": [],
        "expected_instructions": [
            make(OpCode.TRUE),
            make(OpCode.BANG),
            make(OpCode.POP),
        ]

        },
        {
        "input": "if (true) { 10 }; 3333;",
        "expected_constants": [Integer(10), Integer(3333)],
        "expected_instructions": [
            make(OpCode.TRUE),  # 1
            make(OpCode.JUMP_IF_NOT_TRUE, 7),  # 4
            make(OpCode.CONST, 0),  # 7
            make(OpCode.POP),  # 8
            make(OpCode.CONST, 1),  # 11
            make(OpCode.POP),  # 12
        ]

        },
        {
        "input": "if (true) { 10 } else{50}; 3333;",
        "expected_constants": [Integer(10), Integer(50), Integer(3333)],
        "expected_instructions": [
            make(OpCode.TRUE),  # 1
            make(OpCode.JUMP_IF_NOT_TRUE, 10),  # 4
            make(OpCode.CONST, 0),  # 7
            make(OpCode.JUMP, 13),  # 10
            make(OpCode.CONST, 1),  # 13
            make(OpCode.POP),  # 14
            make(OpCode.CONST, 2),  # 17
            make(OpCode.POP),  # 18
        ]

        },
        {
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
        ]


def test_compiler():

    for test in code:
        lexer = Lexer(test["input"])
        program = Parser(lexer).parse_program()
        compiler = Compiler()
        try:
            compiler.compile(program)
            print("----")
            print(test["expected_instructions"][1])
            print(make(OpCode.JUMP_IF_NOT_TRUE, 10))
            print(test)
            print("-----")
        except Exception as e:
            print("compiler ERROR:", e)
            print(compiler.bytecodes().to_string())
            raise e
        try:
            assert compiler.bytecodes().constants == test["expected_constants"]
            assert compiler.bytecodes(
            ).instructions == b''.join(test["expected_instructions"])
        except Exception as e:
            for i, (actual, expected) in enumerate(zip(compiler.constants, test["expected_constants"])):
                if actual != expected:
                    print(
                        f"constant {i} is not equal, actual: {actual}, expected: {expected}")
            for i, (actual, expected) in enumerate(zip(compiler.instructions, test["expected_instructions"])):
                if actual != expected:
                    print(
                        f"instruction {i} is not equal, actual: {actual}, expected: {expected}")
            print(compiler.bytecodes().to_string())
            raise e
