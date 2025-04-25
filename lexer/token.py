from enum import Enum
whitespaces = [' ', '\t', '\n', '\r']
# in this case:the token might be consisted of two letters.
special_chars = ["!", "=", ">", "<"]


class TokenTypes(Enum):
    ILLEGAL = "ILLEGAL"
    EOF = "EOF"

    IDENT = "IDENT"  # add, foobar, x, y, ...
    INT = "INT"  # 1343456
    STRING = "STRING"  # "hello world"

    ASSIGN = "="
    PLUS = "+"
    BANG = "!"
    MINUS = "-"
    SLASH = "/"
    ASTERISK = "*"
    LT = "<"
    GT = ">"
    COMMA = ","
    SEMICOLON = ";"
    COLON = ":"
    LPAREN = "("
    RPAREN = ")"

    LBRACE = "{"
    RBRACE = "}"
    LBRACKET = "["
    RBRACKET = "]"

    EQ = "=="
    NOT_EQ = "!="
    GTE = ">="
    LTE = "<="
    FUNCTION = "FUNCTION"
    LET = "LET"
    IF = "IF"
    ELSE = "ELSE"
    RETURN = "RETURN"
    TRUE = "TRUE"
    FALSE = "FALSE"
    MACRO = "MACRO"


class Token(object):
    def __init__(self, TokenType: TokenTypes, Literal: str):
        self.TokenType = TokenType
        self.Literal = Literal

    def __eq__(self, other):
        if not isinstance(other, Token):
            return False
        return self.TokenType == other.TokenType and self.Literal == other.Literal

    def __str__(self):
        return (f"Token({self.TokenType}, {self.Literal})")


#  we use None to replace the book's 0 value
LiteralToTokenMap = {
    "+": Token(TokenTypes.PLUS, "+"),
    "=": Token(TokenTypes.ASSIGN, "="),
    ",": Token(TokenTypes.COMMA, ","),
    ";": Token(TokenTypes.SEMICOLON, ";"),
    "(": Token(TokenTypes.LPAREN, "("),
    ")": Token(TokenTypes.RPAREN, ")"),
    "{": Token(TokenTypes.LBRACE, "{"),
    "}": Token(TokenTypes.RBRACE, "}"),
    "let": Token(TokenTypes.LET, "let"),
    "function": Token(TokenTypes.FUNCTION, "function"),
    "!": Token(TokenTypes.BANG, "!"),
    "-": Token(TokenTypes.MINUS, "-"),
    "/": Token(TokenTypes.SLASH, "/"),
    "*": Token(TokenTypes.ASTERISK, "*"),
    "<": Token(TokenTypes.LT, "<"),
    ">": Token(TokenTypes.GT, ">"),
    "if": Token(TokenTypes.IF, "if"),
    "else": Token(TokenTypes.ELSE, "else"),
    "return": Token(TokenTypes.RETURN, "return"),
    "true": Token(TokenTypes.TRUE, "true"),
    "false": Token(TokenTypes.FALSE, "false"),
    "==": Token(TokenTypes.EQ, "=="),
    "!=": Token(TokenTypes.NOT_EQ, "!="),
    ">=": Token(TokenTypes.GTE, ">="),
    "<=": Token(TokenTypes.LTE, "<="),
    "[": Token(TokenTypes.LBRACKET, "["),
    "]": Token(TokenTypes.RBRACKET, "]"),
    ":": Token(TokenTypes.COLON, ":"),
    "macro": Token(TokenTypes.MACRO, "macro"),
    None: Token(TokenTypes.EOF, ""),

}


def IsLetter(c):
    return 'a' <= c <= 'z' or 'A' <= c <= 'Z' or c == '_' or ('0' <= c and c <= '9')


def IsDigit(c):
    return '0' <= c and c <= '9'


def lookup_ident(ident) -> TokenTypes:
    if ident in LiteralToTokenMap:
        return LiteralToTokenMap[ident].TokenType
    else:
        return TokenTypes.IDENT


if __name__ == '__main__':
    me = Token(TokenTypes.IDENT, "me")
