
import unittest
from lexer.lexer import Lexer
from lexer.token import Token, TokenTypes
from parser.node import Expression, Identifier, LetStatement, ReturnStatement
from parser.parser import Parser
from tests.testUtills import print_if_error, test_let_statement


class TestStringAST(unittest.TestCase):
    def test_let_statements(self):
        pass
        # let_stmt = LetStatement(Token(TokenTypes.LET, "let"), Identifier(
        #     Token(TokenTypes.IDENT, "x"), "x"), "")
        # self.assertEqual(str(let_stmt), "let x = a;")
        # # self.assertEqual(str(program.statements[1]), "let y = 10;")
        # # self.assertEqual(str(program.statements[2]), "let foobar = 838383;")


if __name__ == '__main__':
    unittest.main()
