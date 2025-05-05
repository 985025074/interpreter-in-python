from compiler.compiler import Compiler
from compiler.vm import VM
from lexer.lexer import Lexer
from parser.parser import Parser


code = "len([1,2,3])"
lexer = Lexer(code)
parser = Parser(lexer)
program = parser.parse_program()
compiler = Compiler()
compiler.compile(program)
print(compiler.bytecodes())
vm = VM(compiler.bytecodes())
vm.run()
print(vm.last_pop())