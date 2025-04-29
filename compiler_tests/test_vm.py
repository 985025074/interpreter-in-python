from compiler.vm import VM
from compiler_tests.utils import parse
from compiler.compiler import Compiler
from eval.object import Integer


def test_vm_top():
    codes = [
        ["1", 1],
        ["2", 2],
        ["1+2", 2]
    ]
    for code, expect in codes:
        compiler = Compiler()
        program = parse(code)
        compiler.compile(program)
        vm = VM(compiler.bytecodes())
        vm.run()
        assert vm.stack_top() == Integer(expect)
