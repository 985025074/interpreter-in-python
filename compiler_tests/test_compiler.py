import pytest
from compiler.compiledfunction import CompiledFunction
from compiler.compiler import Compiler
from compiler.make import make
from compiler.code import OpCode
from eval.object import Integer, String
from lexer.lexer import Lexer
from parser.parser import Parser


def test_compiler():
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

            },
            {
                "input": "let x = 10; x",
            "expected_constants": [Integer(10)],
            "expected_instructions": [
                # 0000
                make(OpCode.CONST, 0),
                make(OpCode.SETGLOBAL, 0),
                make(OpCode.GETGLOBAL, 0),
                make(OpCode.POP),
            ]
            }, {
                "input": "let x = 10; let y = 20; ",
                "expected_constants": [Integer(10), Integer(20)],
                "expected_instructions": [
                    # 0000
                    make(OpCode.CONST, 0),
                    make(OpCode.SETGLOBAL, 0),
                    make(OpCode.CONST, 1),
                    make(OpCode.SETGLOBAL, 1),
                ]
    },
        # this is string example
        {
            "input": "let x = \"hello world\";",
            "expected_constants": [String("hello world")],
            "expected_instructions": [
                # 0000
                make(OpCode.CONST, 0),
                make(OpCode.SETGLOBAL, 0),
            ]


    },
        {
        "input": "[1, 2, 3]",
        "expected_constants": [Integer(1), Integer(2), Integer(3)],
        "expected_instructions": [
            make(OpCode.CONST, 0),
            make(OpCode.CONST, 1),
            make(OpCode.CONST, 2),
            make(OpCode.ARRAY, 3),
            make(OpCode.POP),

        ],
    },
        {
        "input": "[1 + 2, 3 - 4, 5 * 6]",
        "expected_constants": [Integer(1), Integer(2), Integer(3), Integer(4), Integer(5), Integer(6)],
        "expected_instructions": [
            make(OpCode.CONST, 0),
            make(OpCode.CONST, 1),
            make(OpCode.ADD),
            make(OpCode.CONST, 2),
            make(OpCode.CONST, 3),
            make(OpCode.SUB),
            make(OpCode.CONST, 4),
            make(OpCode.CONST, 5),
            make(OpCode.MUL),
            make(OpCode.ARRAY, 3),
            make(OpCode.POP),
        ],
    },
        {
        "input": "{}",
        "expected_constants": [],
        "expected_instructions": [
            make(OpCode.HASH, 0),
            make(OpCode.POP),
        ]
    },
        {
        "input": "{1: 2, 3: 4, 5: 6}",
        "expected_constants": [
            Integer(1), Integer(2),
            Integer(3), Integer(4),
            Integer(5), Integer(6)
        ],
        "expected_instructions": [
            make(OpCode.CONST, 0),
            make(OpCode.CONST, 1),
            make(OpCode.CONST, 2),
            make(OpCode.CONST, 3),
            make(OpCode.CONST, 4),
            make(OpCode.CONST, 5),
            make(OpCode.HASH, 6),
            make(OpCode.POP),
        ]
    },
        {
        "input": "{1: 2 + 3, 4: 5 * 6}",
        "expected_constants": [
            Integer(1), Integer(2), Integer(3),
            Integer(4), Integer(5), Integer(6)
        ],
        "expected_instructions": [
            make(OpCode.CONST, 0),
            make(OpCode.CONST, 1),
            make(OpCode.CONST, 2),
            make(OpCode.ADD),
            make(OpCode.CONST, 3),
            make(OpCode.CONST, 4),
            make(OpCode.CONST, 5),
            make(OpCode.MUL),
            make(OpCode.HASH, 4),
            make(OpCode.POP),
        ]
    },
        # index example
        {
            "input": "[0,1,2][0]",
            "expected_constants": [Integer(0), Integer(1), Integer(2), Integer(0)],
            "expected_instructions": [
                make(OpCode.CONST, 0),
                make(OpCode.CONST, 1),
                make(OpCode.CONST, 2),
                make(OpCode.ARRAY, 3),
                make(OpCode.CONST, 3),
                make(OpCode.INDEX),
                make(OpCode.POP),
            ]
    },
        # index hash
        {
            "input": "{1: 2, 3: 4, 5: 6}[1]",
            "expected_constants": [
                Integer(1), Integer(2),
                Integer(3), Integer(4),
                Integer(5), Integer(6),
                Integer(1)
            ],
            "expected_instructions": [
                make(OpCode.CONST, 0),
                make(OpCode.CONST, 1),
                make(OpCode.CONST, 2),
                make(OpCode.CONST, 3),
                make(OpCode.CONST, 4),
                make(OpCode.CONST, 5),
                make(OpCode.HASH, 6),
                make(OpCode.CONST, 6),
                make(OpCode.INDEX),
                make(OpCode.POP),
            ]

    },
        # index var
        {
            "input": "let arr = [0,1,2]; arr[0]",
            "expected_constants": [Integer(0), Integer(1), Integer(2), Integer(0)],
            "expected_instructions": [
                # 0000
                make(OpCode.CONST, 0),
                make(OpCode.CONST, 1),
                make(OpCode.CONST, 2),
                make(OpCode.ARRAY, 3),
                make(OpCode.SETGLOBAL, 0),
                make(OpCode.GETGLOBAL, 0),
                make(OpCode.CONST, 3),
                make(OpCode.INDEX),
            ]
    },
        # function test
        {
            "input": "function() {return 5+10; };",
            "expected_constants": [
                Integer(5), Integer(10),
                CompiledFunction(b''.join([
                    make(OpCode.CONST, 0),
                    make(OpCode.CONST, 1),
                    make(OpCode.ADD),
                    make(OpCode.RETURN),
                ])),
            ],
        "expected_instructions": [
            make(OpCode.CONST, 2),
            make(OpCode.POP)
        ]
    }
    ]
    for test in code:
        lexer = Lexer(test["input"])
        program = Parser(lexer).parse_program()
        compiler = Compiler()
        try:
            compiler.compile(program)
        except Exception as e:
            print("compiler ERROR:", e)
            raise e
        try:
            if not compiler.bytecodes().constants == test["expected_constants"]:
                raise AssertionError(f"compiler ERROR: {test['input']}")
            if not compiler.bytecodes().instructions == b''.join(test["expected_instructions"]):
                raise AssertionError(f"compiler ERROR: {test['input']}")
        except Exception as e:
            print(test)
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


def test_compiler_error():
    code = [
        {
            "input": "let x = 10; let y = 20;z ",
        }
    ]
    for test in code:
        lexer = Lexer(test["input"])
        program = Parser(lexer).parse_program()
        compiler = Compiler()
        with pytest.raises(Exception):
            compiler.compile(program)
