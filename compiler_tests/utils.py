from lexer.lexer import Lexer
from parser.node import Program
from parser.parser import Parser


def parse(code: str) -> Program:
    return Parser(Lexer(code)).parse_program()
