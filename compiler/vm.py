from compiler.code import OpCode
from compiler.compiler import Bytecode
from eval.object import ycObject


class VM:
    def __init__(self, bytecode: Bytecode = None):
        self.stack = []
        self.bytecode = bytecode
        # note : sp points the len(stack) + 1 loc
        self.sp = 0

    def run(self):
        pc = 0
        instructions = self.bytecode.instructions
        while True:
            if pc >= len(instructions):
                break
            op_code = int.from_bytes(instructions[pc:pc+1], byteorder='big')
            op = OpCode(op_code)
            match op:
                case OpCode.CONST:
                    # two bytes long
                    index = int.from_bytes(
                        instructions[pc+1:pc+3], byteorder='big')
                    self.push(self.bytecode.constants[index])
                    pc += 3
                case OpCode.ADD:
                    # two bytes long
                    pc += 1
                    pass
        pass

    def push(self, value: ycObject):
        self.stack.append(value)
        self.sp += 1

    def stack_top(self):
        return self.stack[-1]
