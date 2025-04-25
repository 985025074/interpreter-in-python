from typing import List
import unittest
from lexer.lexer import Lexer
from lexer.token import Token, TokenTypes


class BaseLexerTest(unittest.TestCase):
    def test_base(self):
        code = """
        let five = 5;
        let ten = 10;
        let add = function(x, y) {
        x + y;
        };
        """
        lexer = Lexer(code)
        tokens: List[Token] = []
        while True:
            tokens.append(lexer.next_token())
            if tokens[-1].TokenType == TokenTypes.EOF:
                break
        # print:
        # for index,token in enumerate(tokens):
        #     print(f"index{index} {token}")
        self.assertEqual(tokens, [
            Token(TokenTypes.LET, "let"),
            Token(TokenTypes.IDENT, "five"),
            Token(TokenTypes.ASSIGN, "="),
            Token(TokenTypes.INT, "5"),
            Token(TokenTypes.SEMICOLON, ";"),
            Token(TokenTypes.LET, "let"),
            Token(TokenTypes.IDENT, "ten"),
            Token(TokenTypes.ASSIGN, "="),
            Token(TokenTypes.INT, "10"),
            Token(TokenTypes.SEMICOLON, ";"),
            Token(TokenTypes.LET, "let"),
            Token(TokenTypes.IDENT, "add"),
            Token(TokenTypes.ASSIGN, "="),
            Token(TokenTypes.FUNCTION, "function"),
            Token(TokenTypes.LPAREN, "("),
            Token(TokenTypes.IDENT, "x"),
            Token(TokenTypes.COMMA, ","),
            Token(TokenTypes.IDENT, "y"),
            Token(TokenTypes.RPAREN, ")"),
            Token(TokenTypes.LBRACE, "{"),
            Token(TokenTypes.IDENT, "x"),
            Token(TokenTypes.PLUS, "+"),
            Token(TokenTypes.IDENT, "y"),
            Token(TokenTypes.SEMICOLON, ";"),
            Token(TokenTypes.RBRACE, "}"),
            Token(TokenTypes.SEMICOLON, ";"),
            Token(TokenTypes.EOF, ""),
        ])

    def test_base2(self):
        code = """
       let five = 5;
        let ten = 10;
        let add = function(x, y) {
        x + y;
        };
        let result = add(five, ten);
        !-/*5;
        5 < 10 > 5;
        if else return true false
        == !=
        """
        lexer = Lexer(code)
        tokens: List[Token] = []
        while True:
            tokens.append(lexer.next_token())
            if tokens[-1].TokenType == TokenTypes.EOF:
                break
        # print:
        # for index,token in enumerate(tokens):
        #     print(f"index{index} {token}")
        self.assertEqual(tokens, [
            Token(TokenTypes.LET, "let"),
            Token(TokenTypes.IDENT, "five"),
            Token(TokenTypes.ASSIGN, "="),
            Token(TokenTypes.INT, "5"),
            Token(TokenTypes.SEMICOLON, ";"),
            Token(TokenTypes.LET, "let"),
            Token(TokenTypes.IDENT, "ten"),
            Token(TokenTypes.ASSIGN, "="),
            Token(TokenTypes.INT, "10"),
            Token(TokenTypes.SEMICOLON, ";"),
            Token(TokenTypes.LET, "let"),
            Token(TokenTypes.IDENT, "add"),
            Token(TokenTypes.ASSIGN, "="),
            Token(TokenTypes.FUNCTION, "function"),
            Token(TokenTypes.LPAREN, "("),
            Token(TokenTypes.IDENT, "x"),
            Token(TokenTypes.COMMA, ","),
            Token(TokenTypes.IDENT, "y"),
            Token(TokenTypes.RPAREN, ")"),
            Token(TokenTypes.LBRACE, "{"),
            Token(TokenTypes.IDENT, "x"),
            Token(TokenTypes.PLUS, "+"),
            Token(TokenTypes.IDENT, "y"),
            Token(TokenTypes.SEMICOLON, ";"),
            Token(TokenTypes.RBRACE, "}"),
            Token(TokenTypes.SEMICOLON, ";"),
            Token(TokenTypes.LET, "let"),
            Token(TokenTypes.IDENT, "result"),
            Token(TokenTypes.ASSIGN, "="),
            Token(TokenTypes.IDENT, "add"),
            Token(TokenTypes.LPAREN, "("),
            Token(TokenTypes.IDENT, "five"),
            Token(TokenTypes.COMMA, ","),
            Token(TokenTypes.IDENT, "ten"),
            Token(TokenTypes.RPAREN, ")"),
            Token(TokenTypes.SEMICOLON, ";"),
            Token(TokenTypes.BANG, "!"),
            Token(TokenTypes.MINUS, "-"),
            Token(TokenTypes.SLASH, "/"),
            Token(TokenTypes.ASTERISK, "*"),
            Token(TokenTypes.INT, "5"),
            Token(TokenTypes.SEMICOLON, ";"),
            Token(TokenTypes.INT, "5"),
            Token(TokenTypes.LT, "<"),
            Token(TokenTypes.INT, "10"),
            Token(TokenTypes.GT, ">"),
            Token(TokenTypes.INT, "5"),
            Token(TokenTypes.SEMICOLON, ";"),
            Token(TokenTypes.IF, "if"),
            Token(TokenTypes.ELSE, "else"),
            Token(TokenTypes.RETURN, "return"),
            Token(TokenTypes.TRUE, "true"),
            Token(TokenTypes.FALSE, "false"),
            Token(TokenTypes.EQ, "=="),
            Token(TokenTypes.NOT_EQ, "!="),
            Token(TokenTypes.EOF, ""),

        ])

    def test_string(self):
        code = """
        let str = "hello world";
        let str2 = "helloworld";
        """
        lexer = Lexer(code)
        tokens = []
        while True:
            tokens.append(lexer.next_token())
            if tokens[-1].TokenType == TokenTypes.EOF:
                break

        # for index,token in enumerate(tokens):
        #     print(f"index{index} {token}")
        self.assertEqual(tokens, [
            Token(TokenTypes.LET, "let"),
            Token(TokenTypes.IDENT, "str"),
            Token(TokenTypes.ASSIGN, "="),
            Token(TokenTypes.STRING, "hello world"),
            Token(TokenTypes.SEMICOLON, ";"),
            Token(TokenTypes.LET, "let"),
            Token(TokenTypes.IDENT, "str2"),
            Token(TokenTypes.ASSIGN, "="),
            Token(TokenTypes.STRING, "helloworld"),
            Token(TokenTypes.SEMICOLON, ";"),
            Token(TokenTypes.EOF, ""),

        ])

    def test_array(self):
        code = """
        let arr = [1, 2, 3];
        let arr2 = [1, 2, 3,];
        :
        """
        lexer = Lexer(code)
        tokens = []
        while True:
            tokens.append(lexer.next_token())
            if tokens[-1].TokenType == TokenTypes.EOF:
                break
        # for index,token in enumerate(tokens):
        #     print(f"index{index} {token}")
        self.assertEqual(tokens, [
            Token(TokenTypes.LET, "let"),
            Token(TokenTypes.IDENT, "arr"),
            Token(TokenTypes.ASSIGN, "="),
            Token(TokenTypes.LBRACKET, "["),
            Token(TokenTypes.INT, "1"),
            Token(TokenTypes.COMMA, ","),
            Token(TokenTypes.INT, "2"),
            Token(TokenTypes.COMMA, ","),
            Token(TokenTypes.INT, "3"),
            Token(TokenTypes.RBRACKET, "]"),
            Token(TokenTypes.SEMICOLON, ";"),
            Token(TokenTypes.LET, "let"),
            Token(TokenTypes.IDENT, "arr2"),
            Token(TokenTypes.ASSIGN, "="),
            Token(TokenTypes.LBRACKET, "["),
            Token(TokenTypes.INT, "1"),
            Token(TokenTypes.COMMA, ","),
            Token(TokenTypes.INT, "2"),
            Token(TokenTypes.COMMA, ","),
            Token(TokenTypes.INT, "3"),
            Token(TokenTypes.COMMA, ","),
            Token(TokenTypes.RBRACKET, "]"),
            Token(TokenTypes.SEMICOLON, ";"),
            Token(TokenTypes.COLON, ":"),
            Token(TokenTypes.EOF, ""),

        ])
if __name__ == '__main__':
    unittest.main()
