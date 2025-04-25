import unittest

from eval.env import Environment
from eval.eval import ycEval
from eval.object import Boolean, HashAble, HashKey, Integer, String
from lexer.lexer import Lexer
from parser.parser import Parser
from tests.testUtills import test_integer


class TestEval(unittest.TestCase):

    def test_1unit(self):
        code = """
            5;
        """
        lexer = Lexer(code)
        parser = Parser(lexer)
        program = parser.parse_program()
        test_integer(self, ycEval(program), 5)
        pass

    def test_prefix(self):
        code = [
            ["!5", False],
            ["!!5", True],
            ["!true", False],
            ["!false", True],
            ["-1", -1],
            ["--123", 123]

        ]

        for test_code, result in code:
            lexer = Lexer(test_code)
            parser = Parser(lexer)
            program = parser.parse_program()
            self.assertEqual(ycEval(program).inspect(), result,
                             msg=f" testcode {test_code}")

    def test_infix(self):
        code = [
            ["-5", -5],
            ["10", 10],
            ["-10", -10],
            ["5", 5],
            ["5 + 5 + 5 + 5 - 10", 10],
            ["2 * 2 * 2 * 2 * 2", 32],
            ["-50 + 100 + -50", 0],
            ["5 * 2 + 10", 20],
            ["5 + 2 * 10", 25],
            ["20 + 2 * -10", 0],
            ["50 / 2 * 2 + 10", 60],
            ["2 * (5 + 10)", 30],
            ["3 * 3 * 3 + 10", 37],
            ["3 * (3 * 3) + 10", 37],
            ["(5 + 10 * 2 + 15 / 3) * 2 + -10", 50],
            ['"asd"+"qwe"+"zxc"', "asdqwezxc"],

        ]

        for test_code, result in code:
            lexer = Lexer(test_code)
            parser = Parser(lexer)
            program = parser.parse_program()
            self.assertEqual(ycEval(program).inspect(), result)

    def test_logic_infix(self):
        code = [
            ["true", True],
            ["false", False],
            ["1 == 1", True],
            ["1 != 2", True],
            ["1 > 2", False],
            ["1 < 2", True],
            ["1 >= 2", False],
            ["1 <= 2", True],
            ["true == true", True],
            ["true != false", True],
            ["false == false", True],
            ["false != true", True],
            ['"asd" == "asd"', True],
            ['"asd" == "qwe"', False],
        ]

        for test_code, result in code:
            lexer = Lexer(test_code)
            parser = Parser(lexer)
            program = parser.parse_program()
            self.assertEqual(ycEval(program).inspect(), result,
                             msg=f" testcode {test_code}")

    def test_if(self):
        code = [
            ["if (true) { 10 }", 10],
            ["if (false) { 10 }", "Null"],
            ["if (1) { 10 }", 10],
            ["if (1 < 2) { 10 }", 10],
            ["if (1 > 2) { 10 }", "Null"],
            ["if (1 > 2) { 10 } else { 20 }", 20],
            ["if (1 < 2) { 10 } else { 20 }", 10]
        ]

        for test_code, result in code:
            lexer = Lexer(test_code)
            parser = Parser(lexer)
            program = parser.parse_program()
            self.assertEqual(ycEval(program).inspect(), result,
                             msg=f" testcode {test_code}")

    def test_return(self):
        code = [
            ["return 10;", 10],
            ["return 10; 9;", 10],
            ["return 2 * 5; 9;", 10],
            ["9; return 2 * 5; 9;", 10],
            ["""if (10 > 1) {
            if (10 > 1) {
                if (10 > 1) {
                return 10;
            }

            }
            return 1;
            }""", 10]
        ]

        for test_code, result in code:
            lexer = Lexer(test_code)
            parser = Parser(lexer)
            program = parser.parse_program()
            self.assertEqual(ycEval(program).inspect(), result,
                             msg=f" testcode {test_code}")

    def test_error(self):
        code = [
            [
                "5 + true;",
                "type mismatch: ObjectType.INTEGER + ObjectType.BOOLEAN", ],
            [
                "5 + true; 5;",
                "type mismatch: ObjectType.INTEGER + ObjectType.BOOLEAN", ],
            [
                "-true",
                "unknown operator: -ObjectType.BOOLEAN", ],
            [
                "true + false;",
                "unknown operator: ObjectType.BOOLEAN + ObjectType.BOOLEAN", ],
            [
                "5; true + false; 5",
                "unknown operator: ObjectType.BOOLEAN + ObjectType.BOOLEAN", ],
            [
                "if (10 > 1) { true + false; }",
                "unknown operator: ObjectType.BOOLEAN + ObjectType.BOOLEAN", ],

            [
                """
            if (10 > 1) {
            if (10 > 1) {
            return true + false;
            }
            return 1;}
            """,
                "unknown operator: ObjectType.BOOLEAN + ObjectType.BOOLEAN", ],

        ]
        for test_code, result in code:
            lexer = Lexer(test_code)
            parser = Parser(lexer)
            program = parser.parse_program()
            self.assertEqual(ycEval(program).inspect(), result,
                             msg=f" testcode {test_code}")

    def test_identifier(self):

        code = [
            ["x", "identifier not found:x"],
            ["let x = 5; x + 5;", 10]
        ]

        for test_code, result in code:
            lexer = Lexer(test_code)
            parser = Parser(lexer)
            program = parser.parse_program()
            default_env = Environment()
            self.assertEqual(ycEval(program, default_env).inspect(), result,
                             msg=f" testcode {test_code}")
            default_env = Environment()

    def test_let_statement(self):

        code = [
            ["let x = 5; x;", 5],
            ["let y = true; y;", True],
            ["let foobar = 8 * 2; foobar;", 16],
            ["let a = 5; let b = a; b;", 5],
            ["let a = 5; let b = a; let c = a + b + 5; c;", 15],
            ["let a = 5; let b = a; let c = a + b + 5; c + b;", 20],
            ["let a = 5; let b = a; let c = a + b + 5; c + b + a;", 25],
            ["let a = 5; let b = a; let c = a + b + 5; c + b + a + 100;", 125],
            ["let a = 5; let b = a; let c = a + b + 5; c + b + a + 100; a;", 5],
        ]
        for test_code, result in code:
            lexer = Lexer(test_code)
            parser = Parser(lexer)
            program = parser.parse_program()
            self.assertEqual(ycEval(program, Environment()).inspect(), result,
                             msg=f" testcode {test_code}")

    def test_function(self):

        code = [
            ["let identity = function(x) { x; }; identity(5);", 5],
            ["let identity = function(x) { return x; }; identity(5);", 5],
            ["let double = function(x) { x * 2; }; double(5);", 10],
            ["let add = function(x, y) { x + y; }; add(5, 5);", 10],
            ["let add = function(x, y) { x + y; }; add(5 + 5, add(5, 5));", 20],
            ["function(x) { x; }(5)", 5],
            ["""
                let newAdder = function(x) {
                function(y) { x + y };
                };
                let addTwo = newAdder(2);
                addTwo(2);""", 4],
        ]
        for test_code, result in code:
            lexer = Lexer(test_code)
            parser = Parser(lexer)
            program = parser.parse_program()
            self.assertEqual(ycEval(program, Environment()).inspect(), result,
                             msg=f" testcode {test_code}")

    def test_array(self):
        code = [
            ["[1, 2, 3]", [1, 2, 3]],
            ["[1 + 2, 3 * 4, 5 - 6]", [3, 12, -1]],
            [
                "[1, 2, 3][0]",
                1,

            ],
            [
                "[1, 2, 3][1]",
                2,
            ],
            [
                "[1, 2, 3][2]",
                3,
            ],
            [
                "let i = 0; [1][i];",
                1,
            ],
            [
                "[1, 2, 3][1 + 1];",
                3,
            ],
            [
                "let myArray = [1, 2, 3]; myArray[2];",
                3,
            ],
            [
                "let myArray = [1, 2, 3]; myArray[0] + myArray[1] + myArray[2];",
                6,
            ],
            [
                "let myArray = [1, 2, 3]; let i = myArray[0]; myArray[i]",
                2,
            ],
            [
                "[1, 2, 3][3]",
                "index out of range: 3",
            ],
            [
                "[1, 2, 3][-1]",
                3,
            ],

            [
                "[1, 2, 3][-1]",
                3,
            ],


        ]
        for test_code, result in code:
            lexer = Lexer(test_code)
            parser = Parser(lexer)
            program = parser.parse_program()
            self.assertEqual(ycEval(program, Environment()).inspect(), result,
                             msg=f" testcode {test_code}")

    def test_hash(self):
        hashkey1 = HashKey("key1", "123")
        hashkey2 = HashKey("key2", "456")
        hashkey3 = HashKey("key1", "123")
        hashkey4 = HashKey("key1", 123)
        hashkey5 = HashKey("key1", True)
        hashkey6 = HashKey("key1", False)
        self.assertEqual(hashkey1, hashkey3)
        self.assertNotEqual(hashkey1, hashkey2)
        self.assertNotEqual(hashkey1, hashkey4)
        self.assertNotEqual(hashkey1, hashkey5)
        self.assertNotEqual(hashkey1, hashkey6)
        self.assertIsInstance(Integer(1), HashAble)
        self.assertIsInstance(String("123"), HashAble)
        self.assertIsInstance(Boolean(True), HashAble)

    def test_hash_use(self):
        code = """
        let two = "two";
        {
            "one": 10 - 9,
            two: 1 + 1,
            "thr" + "ee": 6 / 2,
            4: 4,
            true: 5,
            false: 6 
        }
        
        """
        lexer = Lexer(code)
        parser = Parser(lexer)
        program = parser.parse_program()
        self.assertEqual(ycEval(program, Environment()).inspect(), {
                         "one": 1, "two": 2, "three": 3, 4: 4, True: 5, False: 6})

    def test_hash_use_2(self):
        code = [[
            '{"foo": 5}["foo"]',
            5,
        ], [
            '{"foo": 5}["bar"]',
            'key not found: bar',
        ],
            ['let key= "foo"; {"foo": 5}[key]',
             5,
             ],
            [
            'let key = "foo"; {"foo": 5, "bar": 6}[key]',
            5,
        ],
            [
            'let key = "bar"; {"foo": 5, "bar": 6}[key]',
            6,
        ],
            [
            "let key = 4; {4: 5}[key]",
            5,
        ],
            [
            "let key = true; {true: 5}[key]",
            5,
        ],
           
        ]
        for test_code, result in code:
            lexer = Lexer(test_code)
            parser = Parser(lexer)
            program = parser.parse_program()
            self.assertEqual(ycEval(program, Environment()).inspect(), result,
                             msg=f" testcode {test_code}")
