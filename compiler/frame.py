
from compiler.compiler import Bytecode


class Frame:
    def __init__(self, instructions: bytes, pc=0, bp=0):
        self.instructions = instructions
        self.pc = pc
        self.bp = bp
