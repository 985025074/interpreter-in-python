
import unittest
from lexer.lexer import Lexer
from parser.node import ArrayExpression, BlockStatement, BooleanLiteral, Expression, ExpressionStatement, HashLiteral, Identifier, IndexExpression, InfixExpression, IntegerLiteral, LetStatement, PreFixExpression, ReturnStatement, StringLiteral
from parser.parser import Parser
from tests.testUtills import print_if_error, test_call_expression, test_function_literal, test_hash_literal, test_if_expression, test_let_statement


class TestParser(unittest.TestCase):
    def test_let_statements(self):
        input_code = """
        let x = 5;
        let y = 10;
        let foobar = 838383;

        """

        lexer = Lexer(input_code)
        parser = Parser(lexer)
        program = parser.parse_program()
        print_if_error(self, parser)
        self.assertIsNotNone(program, "parse_program() returned None")

        self.assertEqual(
            len(program.statements), 3,

            f"program.statements does not contain 3 statements. got={len(program.statements)}"
        )

        tests = [
            {"expected_identifier": "x"},
            {"expected_identifier": "y"},
            {"expected_identifier": "foobar"},
        ]

        for i, tt in enumerate(tests):
            stmt = program.statements[i]
            test_let_statement(self, stmt, tt["expected_identifier"]),

    def test_return_statement(self):
        input_code = """
        return 5;
        return 10;
        return 5;
        """
        lexer = Lexer(input_code)
        parser = Parser(lexer)
        program = parser.parse_program()
        print_if_error(self, parser)
        self.assertIsNotNone(program, "parse_program() returned None")

        self.assertEqual(
            len(program.statements), 3,
            f"program.statements does not contain 3 statements. got={len(program.statements)}"
        )

        tests = [
            "5",
            "10",
            "5"
        ]

        for i, tt in enumerate(tests):
            stmt = program.statements[i]
            self.assertEqual(
                stmt.token_literal(), "return",
                f"stmt.token_literal is not 'return'. got={stmt.token_literal()}"
            )
            # basic check
            self.assertIsInstance(stmt, ReturnStatement,
                                  "stmt is not a ReturnStatement")
            self.assertIsInstance(
                stmt.return_value, Expression, "stmt.return_value is not an Expression")
            # check value here
            if isinstance(stmt.return_value, IntegerLiteral):
                self.assertEqual(
                    stmt.return_value.value, int(tt),
                    f"stmt.return_value.value is not {tt}. got={stmt.return_value.value}"
                )

    def test_expression_statement_1unit(self):
        input_code = """
        x ;
        1231231231;
        let y = 10;
        return ;
        """

        lexer = Lexer(input_code)
        parser = Parser(lexer)
        program = parser.parse_program()
        print_if_error(self, parser)

        self.assertIsInstance(program.statements[0], ExpressionStatement)
        if isinstance(program.statements[0], ExpressionStatement):
            self.assertIsInstance(program.statements[0].expression, Identifier)

        self.assertIsInstance(program.statements[1], ExpressionStatement)
        if isinstance(program.statements[1], ExpressionStatement):
            self.assertIsInstance(
                program.statements[1].expression, IntegerLiteral)

        self.assertIsInstance(program.statements[2], LetStatement)
        self.assertIsInstance(program.statements[3], ReturnStatement)

    def test_expression_statement_prefix_operator(self):
        code = [
            ["!5", "!", 5],
            ["-15", "-", 15]

        ]
        for i, test_case in enumerate(code):
            lexer = Lexer(test_case[0])
            parser = Parser(lexer)
            program = parser.parse_program()
            stmt = program.statements[0]
            print_if_error(self, parser)
            # len

            self.assertEqual(len(program.statements), 1)

            # base check
            self.assertIsInstance(stmt, ExpressionStatement)
            self.assertIsInstance(stmt.expression, PreFixExpression)
            # check expression
            if isinstance(stmt, ExpressionStatement):
                if isinstance(stmt.expression, PreFixExpression):
                    if isinstance(test_case[2], int):
                        self.assertIsInstance(
                            stmt.expression.right, IntegerLiteral)
                    elif isinstance(test_case[2], str):
                        self.assertIsInstance(
                            stmt.expression.right, Identifier)
            # check value:both integer and identifier will be checked properly
            if isinstance(stmt, ExpressionStatement):
                self.assertEqual(stmt.expression.right.value, test_case[2])
            # check operator:
            if isinstance(stmt.expression, PreFixExpression):
                self.assertEqual(stmt.expression.token.Literal, test_case[1])

    def test_expression_statement_infix_operator(self):
        code = [
            ["5+5", 5, "+", 5],
            ["10-5", 10, "-", 5],
            ["5*5", 5, "*", 5],
            ["10/5", 10, "/", 5],
            ["5>5", 5, ">", 5],
            ["10<5", 10, "<", 5],
            ["5==5", 5, "==", 5],
            ["10!=5", 10, "!=", 5],

        ]
        for i, test_case in enumerate(code):
            lexer = Lexer(test_case[0])
            parser = Parser(lexer)
            program = parser.parse_program()
            stmt = program.statements[0]
            print_if_error(self, parser)
            # len

            self.assertEqual(len(program.statements), 1)

            # base check
            self.assertIsInstance(stmt, ExpressionStatement)
            self.assertIsInstance(stmt.expression, Expression)
            # check expression
            if isinstance(stmt, ExpressionStatement):
                if isinstance(stmt.expression, InfixExpression):
                    if isinstance(test_case[1], int):
                        self.assertIsInstance(
                            stmt.expression.left, IntegerLiteral)
                        self.assertEqual(
                            stmt.expression.left.value, test_case[1])
                    elif isinstance(test_case[1], str):
                        self.assertIsInstance(stmt.expression.left, Identifier)
                    if isinstance(test_case[3], int):
                        self.assertIsInstance(
                            stmt.expression.right, IntegerLiteral)
                        self.assertEqual(
                            stmt.expression.right.value, test_case[3])
                    elif isinstance(test_case[3], str):
                        self.assertIsInstance(
                            stmt.expression.right, Identifier)
                        self.assertEqual(
                            stmt.expression.right.value, test_case[3])
            # check operator:
            if isinstance(stmt.expression, InfixExpression):
                self.assertEqual(stmt.expression.token.Literal, test_case[2])

    def test_expression_statement_deeper(self):
        codes = [
            [
                "-a * b",
                "((-a) * b)",
            ],
            [
                "!-a",
                "(!(-a))",
            ], [
                "a + b + c",
                "((a + b) + c)",
            ],
            [
                "a + b - c",
                "((a + b) - c)",
            ],
            [
                "a * b * c",
                "((a * b) * c)",
            ],
            [
                "a * b / c",
                "((a * b) / c)",
            ],
            [
                "a + b / c",
                "(a + (b / c))",
            ],
            [
                "a + b * c + d / e - f",
                "(((a + (b * c)) + (d / e)) - f)",
            ],
            [
                "3 + 4; -5 * 5",
                "(3 + 4)((-5) * 5)",
            ],
            [
                "5 > 4 == 3 < 4",
                "((5 > 4) == (3 < 4))", ],
            [
                "5 < 4 != 3 > 4",
                "((5 < 4) != (3 > 4))",
            ],
            [
                "3 + 4 * 5 == 3 * 1 + 4 * 5",
                "((3 + (4 * 5)) == ((3 * 1) + (4 * 5)))",
            ],


        ]
        for code, expected in codes:
            lexer = Lexer(code)
            parser = Parser(lexer)
            program = parser.parse_program()
            self.assertEqual(str(program), expected)

    def test_booleanliteral(self):
        code = """
        true;
        false;
        let x = true;
        let y = false;
        """
        lexer = Lexer(code)
        parser = Parser(lexer)
        program = parser.parse_program()

        #  s1:
        if isinstance(program.statements[0], ExpressionStatement):
            self.assertIsInstance(
                program.statements[0].expression, BooleanLiteral)
            self.assertEqual(program.statements[0].expression.value, True)
        if isinstance(program.statements[1], ExpressionStatement):
            self.assertIsInstance(
                program.statements[1].expression, BooleanLiteral)
            self.assertEqual(program.statements[1].expression.value, False)
        if isinstance(program.statements[2], LetStatement):
            self.assertIsInstance(
                program.statements[2].right_expression, BooleanLiteral)
            self.assertEqual(
                program.statements[2].right_expression.value, True)
        if isinstance(program.statements[3], LetStatement):
            self.assertIsInstance(
                program.statements[3].right_expression, BooleanLiteral)
            self.assertEqual(
                program.statements[3].right_expression.value, False)

    def test_group_parse(self):
        codes = [
            [
                "1 + (2 + 3) + 4",
                "((1 + (2 + 3)) + 4)",
            ],
            [
                "(5 + 5) * 2",
                "((5 + 5) * 2)",
            ],
            [
                "2 / (5 + 5)",
                "(2 / (5 + 5))",
            ],
            [
                "-(5 + 5)",
                "(-(5 + 5))",
            ],
            [
                "!(true == true)",
                "(!(True == True))",
            ],
            [
                "a + add(b * c) + d",
                "((a + add((b * c))) + d)",
            ],
            ["add(a, b, 1, 2 * 3, 4 + 5, add(6, 7 * 8))",
             "add(a, b, 1, (2 * 3), (4 + 5), add(6, (7 * 8)))",
             ],
            [
                "add(a + b + c * d / f + g)",
                "add((((a + b) + ((c * d) / f)) + g))",
            ],
            [
                "a * [1, 2, 3, 4][b * c] * d",
                "((a * ([1, 2, 3, 4][(b * c)])) * d)",

            ],
            [
                "add(a * b[2], b[1], 2 * [1, 2][1])",
                "add((a * (b[2])), (b[1]), (2 * ([1, 2][1])))",
            ],

        ]
        for code, expected in codes:
            lexer = Lexer(code)
            parser = Parser(lexer)
            program = parser.parse_program()
            self.assertEqual(str(program), expected)

    def test_if_expression(self):
        code = """
        if (x < y) {
            x
        } else {
            y
            }
        """
        lexer = Lexer(code)
        parser = Parser(lexer)
        program = parser.parse_program()
        test_if_expression(
            self, program.statements[0].expression, "x<y", "x", "y")

    def test_if_expression_no_else(self):
        code = """
        if (x < y) {
            x
        }
        """
        lexer = Lexer(code)
        parser = Parser(lexer)
        program = parser.parse_program()
        test_if_expression(
            self, program.statements[0].expression, "x<y", "x", None)

    def test_function_literal(self):
        code = """
        function (x,y) {
            x + y;
            return 123;
        };
        function () {
            x + y;
            return 123;
        };
        function (x){

        };
        """
        lexer = Lexer(code)
        parser = Parser(lexer)
        program = parser.parse_program()
        test_function_literal(self, program.statements[0].expression, [
                              "x", "y"], "x+y;return 123;")
        test_function_literal(self, program.statements[1].expression, [
        ], "x+y;return 123;")
        test_function_literal(self, program.statements[2].expression, [
            "x"], "")

    def test_complex_if(self):
        code = """
        if (x < y) {
            if (y > x) {
                return x;
            } else {
                return y;
            }
        } else {
            return 0;
        }
        """
        lexer = Lexer(code)
        parser = Parser(lexer)
        program = parser.parse_program()
        print_if_error(self, parser)
        test_if_expression(
            self, program.statements[0].expression, "x<y", "if(y>x){return x;}else{return y;}", "return 0;")

    def test_callexpression(self):
        code = """
            add(1, 2 * 3, 4 + 5);
        """
        lexer = Lexer(code)
        parser = Parser(lexer)
        program = parser.parse_program()
        print_if_error(self, parser)
        test_call_expression(self, program.statements[0].expression, "add", [
                             "1", "2*3", "4+5"],)

    def test_string_parse(self):
        code = """
            "hello world";
        """
        lexer = Lexer(code)
        parser = Parser(lexer)
        program = parser.parse_program()
        print_if_error(self, parser)
        self.assertIsInstance(program.statements[0], ExpressionStatement)
        if isinstance(program.statements[0], ExpressionStatement):
            self.assertIsInstance(
                program.statements[0].expression, StringLiteral)
            self.assertEqual(
                program.statements[0].expression.value, "hello world")
    #  hey ! this test file is generate by ai, so it may look like a mess, but it works

    def test_array_parse(self):
        code = """
            [1, 2, 3];
            [];
        """
        lexer = Lexer(code)
        parser = Parser(lexer)
        program = parser.parse_program()
        print_if_error(self, parser)
        self.assertIsInstance(program.statements[0], ExpressionStatement)
        if isinstance(program.statements[0], ExpressionStatement):
            self.assertIsInstance(
                program.statements[0].expression, ArrayExpression)
            self.assertEqual(len(program.statements[0].expression.elements), 3)
            if len(program.statements[0].expression.elements) == 3:
                self.assertIsInstance(
                    program.statements[0].expression.elements[0], IntegerLiteral)
                self.assertIsInstance(
                    program.statements[0].expression.elements[1], IntegerLiteral)
                self.assertIsInstance(
                    program.statements[0].expression.elements[2], IntegerLiteral)
                self.assertEqual(
                    program.statements[0].expression.elements[0].value, 1)
                self.assertEqual(
                    program.statements[0].expression.elements[1].value, 2)
                self.assertEqual(
                    program.statements[0].expression.elements[2].value, 3)
        self.assertIsInstance(program.statements[1], ExpressionStatement)
        if isinstance(program.statements[1], ExpressionStatement):
            self.assertIsInstance(
                program.statements[1].expression, ArrayExpression)
            self.assertEqual(len(program.statements[1].expression.elements), 0)

    def test_arr_expression(self):
        code = """
            a[1+2];
            a[];
        """
        lexer = Lexer(code)
        parser = Parser(lexer)
        program = parser.parse_program()
        print_if_error(self, parser)
        self.assertIsInstance(program.statements[0], ExpressionStatement)
        if isinstance(program.statements[0], ExpressionStatement):
            self.assertIsInstance(
                program.statements[0].expression, IndexExpression)
            self.assertIsInstance(
                program.statements[0].expression.left, Identifier)
            self.assertIsInstance(
                program.statements[0].expression.index, InfixExpression)
            self.assertIsInstance(
                program.statements[0].expression.index.left, IntegerLiteral)
            self.assertIsInstance(
                program.statements[0].expression.index.right, IntegerLiteral)
            self.assertEqual(
                program.statements[0].expression.index.left.value, 1)
            self.assertEqual(
                program.statements[0].expression.index.right.value, 2)
        self.assertIsInstance(program.statements[1], ExpressionStatement)
        if isinstance(program.statements[1], ExpressionStatement):
            self.assertIsInstance(
                program.statements[1].expression, IndexExpression)
            self.assertIsInstance(
                program.statements[1].expression.left, Identifier)

    def test_hash_map_parse(self):
        code = """
            {"key": "value", "key2": 123};
            {};
        """
        lexer = Lexer(code)
        parser = Parser(lexer)
        program = parser.parse_program()
        print_if_error(self, parser)
        test_hash_literal(self, program.statements[0].expression, [
                          "key", "key2"], ["value", 123])
        test_hash_literal(self, program.statements[1].expression, [], [])


if __name__ == '__main__':
    
    unittest.main()
