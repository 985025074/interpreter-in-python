from eval.env import Environment
from eval.eval import NULL, ycEval
from eval.macro import expand_macro, handle_macro
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

    program = parser.parse_program()
    handle_macro(program, env)
    program = expand_macro(program, env)
    result = ycEval(program, env)
    if not isinstance(result, Null):
        print(result)
    print_if_error(None, parser)


def repl():
    import code
    import sys

    prompt = ">>> "
    buffer = []

    while True:
        try:
            line = input(prompt)
        except EOFError:
            break

        if line.strip() == "":  # 用户输入空行，表示代码输入完毕
            source = "\n".join(buffer)
            try:
                result = eval(source)
                if result is not None:
                    print(result)
            except SyntaxError:
                try:
                    exec(source)
                except Exception as e:
                    print(f"Error during exec: {e}")
            except Exception as e:
                print(f"Error during eval: {e}")
            buffer = []
            prompt = ">>> "
        else:
            buffer.append(line)
            prompt = "... "

repl()
