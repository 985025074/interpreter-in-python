from eval.env import Environment
from eval.eval import NULL, ycEval
from eval.object import Null
from lexer.lexer import Lexer
from lexer.token import TokenTypes
# this is for the move function. when you input in the repl.
import readline

from parser.parser import Parser
from tests.testUtills import print_if_error

welcome_message = "Welcome to Cong's Interpreter!"
prompt = ">>>"
env = Environment()
print(welcome_message)


def eval(code):
    lexer = Lexer(code)
    parser = Parser(lexer)
    result = ycEval(parser.parse_program(), env)
    if not isinstance(result, Null):
        print(result)
    print_if_error(None, parser)


while True:
    code = input(prompt)
    eval(code)
