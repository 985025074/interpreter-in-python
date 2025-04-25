import unittest
from eval.env import Environment
from eval.eval import ycEval
from eval.macro import expand_macro, handle_macro
from eval.modify import modify
from eval.object import Quote
from lexer.lexer import Lexer
from lexer.token import Token, TokenTypes
from parser.node import Expression, ExpressionStatement, FunctionLiteral, Identifier, IfExpression, IndexExpression, InfixExpression, IntegerLiteral, LetStatement, Node, PreFixExpression, ReturnStatement
from parser.parser import Parser
from tests.testUtills import print_if_error, test_let_statement
one = IntegerLiteral(Token(TokenTypes.INT, "1"))
two = IntegerLiteral(Token(TokenTypes.INT, "2"))


def change_one_to_two(node: Node):
    if not isinstance(node, IntegerLiteral):
        return node
    if node == one:
        return two
    else:
        return node


class TestMacro(unittest.TestCase):
    def test_quote(self):
        codes = [
            ["quote(5)", "5"],
            [
                "quote(5 + 8)",
                "(5 + 8)",
            ],
            [
                "quote(foobar)",
                "foobar",
            ],
            [
                "quote(foobar + barfoo)",
                "(foobar + barfoo)",
            ],
        ]
        for code, expect in codes:
            parser = Parser(Lexer(code))
            program = parser.parse_program()
            quote_expression = ycEval(program, Environment())
            self.assertIsInstance(quote_expression, Quote)
            if isinstance(quote_expression, Quote):
                self.assertEqual(str(quote_expression.node), expect)

    def test_unquote(self):
        codes = [
            ["quote(unquote(4))",
             "4",
             ], ["quote(unquote(4 + 4))",
                 "8",
                 ],
            ["quote(8 + unquote(4 + 4))",
             "(8 + 8)",
             ],
            ["quote(unquote(4 + 4) + 8)",
             "(8 + 8)",
             ],
            [
                "let foobar=8;quote(foobar)",
                "foobar"

            ],
            [
                "let foobar=8;quote(unquote(foobar))",
                "8"
            ],
            [
                "quote(unquote(true))",
                "True",
            ],
            [
                "quote(unquote(true == false))",
                "False",
            ],
            [
                "quote(unquote(quote(4 + 4)))",
                "(4 + 4)",
            ],
            ["let quotedInfixExpression = quote(4 + 4);quote(unquote(4 + 4) + unquote(quotedInfixExpression))",
                "(8 + (4 + 4))",
             ],
        ]
        for code, expect in codes:
            parser = Parser(Lexer(code))
            program = parser.parse_program()
            quote_expression = ycEval(program, Environment())
            self.assertIsInstance(quote_expression, Quote)
            if isinstance(quote_expression, Quote):
                self.assertEqual(str(quote_expression.node), expect)

    def test_modifier(self):

        code = "1"
        parser = Parser(Lexer(code))
        program = parser.parse_program()

        def change_one_to_two(node: Node):
            if not isinstance(node, IntegerLiteral):
                return node
            if node == one:
                return two
            else:
                return node
        self.assertEqual(
            modify(program.statements[0], change_one_to_two).expression, two)

    def test_infix_modifier(self):
        test_ast = InfixExpression(
            left=one, operator=Token(TokenTypes.PLUS, "+"), right=two)

        def change_one_to_two(node: Node):
            if not isinstance(node, IntegerLiteral):
                return node
            if node == one:
                return two
            else:
                return node

        self.assertEqual(modify(test_ast, change_one_to_two),
                         InfixExpression(left=two, operator=Token(TokenTypes.PLUS, "+"), right=two))

    def test_prefix_modifier(self):
        test_ast = PreFixExpression(
            operator=Token(TokenTypes.BANG, "!"), right=one)

        def change_one_to_two(node: Node):
            if not isinstance(node, IntegerLiteral):
                return node
            if node == one:
                return two
            else:
                return node

        self.assertEqual(modify(test_ast, change_one_to_two),
                         PreFixExpression(operator=Token(TokenTypes.BANG, "!"), right=two))

    def test_index_modifier(self):
        test_ast = IndexExpression(token=Token(
            TokenTypes.LBRACKET, "["), left=one, index=two)
        expected_ast = IndexExpression(token=Token(
            TokenTypes.LBRACKET, "["), left=two, index=two)

        self.assertEqual(modify(test_ast, change_one_to_two),
                         expected_ast, msg=f"{test_ast}:{expected_ast}")

    def test_if_modifier(self):
        test_ast = IfExpression(one, one, one, one)
        expected_ast = IfExpression(one, two, two, two)
        self.assertEqual(modify(test_ast, change_one_to_two),
                         expected_ast, msg=f"{test_ast}:{expected_ast}")

    def test_return_modifier(self):
        test_ast = ReturnStatement(one, one)
        expected_ast = ReturnStatement(one, two)

        self.assertEqual(modify(test_ast, change_one_to_two),
                         expected_ast, msg=f"{test_ast}:{expected_ast}")

    def test_let_modifier(self):
        test_ast = LetStatement(Token(TokenTypes.LET, "let"), Identifier(
            Token(TokenTypes.IDENT, "x")), one)
        expected_ast = LetStatement(Token(TokenTypes.LET, "let"), Identifier(
            Token(TokenTypes.IDENT, "x")), two)
        self.assertEqual(modify(test_ast, change_one_to_two),
                         expected_ast, msg=f"{test_ast}:{expected_ast}")

    def test_handle_macro(self):
        code = """
         let Macro = macro(x) {
             quote(unquote(x) + 1)
         };
         let x = 1;
         """
        env = Environment()
        parser = Parser(Lexer(code))
        program = parser.parse_program()
        handle_macro(program, env)
        self.assertEqual(env.has_key("Macro"), True)
        self.assertEqual(len(program.statements), 1)
        self.assertEqual(program.statements[0], LetStatement(Token(TokenTypes.LET, "let"), Identifier(
            Token(TokenTypes.IDENT, "x")), IntegerLiteral(Token(TokenTypes.INT, "1"))))

    def test_expand_macro(self):
        codes = [
            [
                'let infixExpression = macro() {quote(1 + 2); }; infixExpression();',
                '(1 + 2)',
            ],
            [
                'let reverse = macro(a, b) { quote(unquote(b) - unquote(a)); };reverse(2 + 2, 10 - 5);',
                '((10 - 5) - (2 + 2))',
            ]
        ]
        for code, expected in codes:

            lexer = Lexer(code)
            parser = Parser(lexer)
            program = parser.parse_program()
            env = Environment()
            handle_macro(program, env)

            expanded_program = expand_macro(program, env)
            # program.print_whole_program_nicely()
            self.assertEqual(str(expanded_program.statements[-1]), expected)

    def test_unless(self):
        code = """
           let unless = macro(condition, consequence, alternative) {
             quote(if (!(unquote(condition))) {
            unquote(consequence);
            } else {
            unquote(alternative);
            });
            };
            unless(10 > 5, puts("not greater"), puts("greater"));
        """
        expected = """if (!(10 > 5)) { puts("not greater");
        } else { puts("greater");}
        """
        lexer = Lexer(code)
        parser = Parser(lexer)
        program = parser.parse_program()
        env = Environment()
        handle_macro(program, env)
        expected = str(Parser(Lexer(expected)).parse_program().statements[0])
        expanded_program = expand_macro(program, env)
        # program.print_whole_program_nicely()
        self.assertEqual(str(expanded_program.statements[-1]), expected)


if __name__ == '__main__':
    unittest.main()
