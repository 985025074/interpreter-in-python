from compiler.code import OpCode
from compiler.compiler import CompileScope, Compiler
from compiler.symtable import SymTable
from compiler.vm import VM
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

first_call = True


def eval(code, constants, scopes, globals):
    global first_call
    if code == "":
        return None
    lexer = Lexer(code)
    parser = Parser(lexer)
    compiler = Compiler()
    compiler.scopes = scopes
    compiler.constants = constants
    if first_call:
        compiler.init_builtins()
        first_call = False

    compiler.compile(parser.parse_program())
    if compiler.instructions != [] and compiler.instructions[-1][0:1] == OpCode.POP.bytes:
        compiler.instructions.pop()

    vm = VM(compiler.bytecodes())

    vm.globals = globals
    # print(vm.globals[:10])
    # print(compiler.constants)
    vm.run()

    result = vm.top()

    print_if_error(None, parser)
    return result


def repl():
    import code
    import sys
    global_sym = SymTable()
    globals = [0 for i in range(65535)]
    global_constants = []
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
                result = eval(source, constants=global_constants, scopes=[
                              CompileScope(global_sym)], globals=globals)
                if result is not None:
                    print(result)
            except SyntaxError:
                try:
                    exec(source)
                except Exception as e:
                    print(f"Error during exec: {e}")
            except Exception as e:
                print(f"Error during eval: {e}")
                raise e
            buffer = []
            prompt = ">>> "
        else:
            buffer.append(line)
            prompt = "... "


repl()
