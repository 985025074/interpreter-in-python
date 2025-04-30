
from compiler.code import OpCode
from compiler.compiler import Bytecode
from compiler.math_compute import compute
from eval.eval import FALSE, TRUE, handleBang, NULL
from eval.object import Array, Hash, HashAble, HashKey, HashPair, Integer, String, ycObject, Boolean


class VM:
    def __init__(self, bytecode: Bytecode = None):
        self.stack = []
        self.bytecode = bytecode
        # note : sp points the len(stack) + 1 loc
        self.sp = 0
        self.globals = [0 for i in range(65535)]

    def run(self):
        pc = 0
        instructions = self.bytecode.instructions
        while True:
            if pc >= len(instructions):
                break
            op_code = int.from_bytes(instructions[pc:pc+1], byteorder='big')
            op = OpCode(op_code)
            match op:
                case OpCode.POP:
                    self.pop()
                    pc += 1
                case OpCode.CONST:
                    # two bytes long
                    index = int.from_bytes(
                        instructions[pc+1:pc+3], byteorder='big')
                    self.push(self.bytecode.constants[index])
                    pc += 3
                case OpCode.ADD | OpCode.SUB | OpCode.MUL | OpCode.DIV:
                    # two bytes long
                    right = self.pop()
                    left = self.pop()
                    assert isinstance(
                        left, Integer) or isinstance(left, String)
                    assert isinstance(
                        right, Integer) or isinstance(right, String)
                    assert type(left) == type(right)
                    result = compute(left.value, right.value, op)
                    self.push(Integer(result))

                    pc += 1
                case OpCode.TRUE | OpCode.FALSE:
                    self.push(TRUE if op == OpCode.TRUE else FALSE)
                    pc += 1
                case OpCode.GT | OpCode.EQ | OpCode.NOTEQ:
                    right = self.pop()
                    left = self.pop()
                    assert isinstance(left, ycObject)
                    assert isinstance(right, ycObject)
                    result = compute(left.value, right.value, op)
                    self.push(Boolean(result))
                    pc += 1
                case OpCode.BANG | OpCode.MINUS:
                    right = self.pop()
                    assert isinstance(right, ycObject)
                    match op:
                        case OpCode.BANG:
                            result = handleBang(right)
                            self.push(result)
                        case OpCode.MINUS:
                            result = -right.value
                            self.push(Integer(result))
                    pc += 1
                case OpCode.JUMP:
                    target_loc = int.from_bytes(
                        instructions[pc+1:pc+3], byteorder='big')
                    pc = target_loc
                case OpCode.JUMP_IF_NOT_TRUE:
                    previous_result = self.pop()

                    if not previous_result.value:
                        target_loc = int.from_bytes(
                            instructions[pc+1:pc+3], byteorder='big')
                        pc = target_loc
                    else:
                        pc += 3
                case OpCode.NULL:
                    self.push(NULL)
                    pc += 1
                case OpCode.SETGLOBAL:
                    self.globals[int.from_bytes(
                        instructions[pc+1:pc+3], byteorder='big')] = self.pop()
                    pc += 3
                case OpCode.GETGLOBAL:
                    index = int.from_bytes(
                        instructions[pc+1:pc+3], byteorder='big')
                    self.push(self.globals[index])
                    pc += 3
                case OpCode.ARRAY:
                    array = []
                    for i in range(int.from_bytes(instructions[pc+1:pc+3], byteorder='big')):
                        array.insert(0, self.pop())
                    self.push(Array(array))
                    pc += 3
                case OpCode.HASH:
                    dic = {}
                    for i in range(int.from_bytes(instructions[pc+1:pc+3], byteorder='big')):
                        value = self.pop()
                        key = self.pop()
                        dic[HashKey(key.type(), key.value)
                            ] = HashPair(key, value)
                    self.push(Hash(dic))
                    pc += 3
                case OpCode.INDEX:
                    index = self.pop()
                    indexable = self.pop()

                    assert isinstance(indexable, Array) or isinstance(
                        indexable, Hash)
                    assert isinstance(index, HashAble)
                    try:
                        if isinstance(indexable, Array):
                            self.push(indexable[index])
                        else:
                            self.push(indexable[index.hash_key()])
                    except:
                        self.push(NULL)
                    pc += 1
                case _:
                    pass

        pass

    def push(self, value: ycObject):
        if self.sp >= len(self.stack):
            self.stack.append(value)
            self.sp += 1
        else:
            self.stack[self.sp] = value
            self.sp += 1

    def pop(self) -> ycObject:
        self.sp -= 1
        return self.stack[self.sp]

    def last_pop(self):
        try:
            return self.stack[self.sp]
        except IndexError:
            return None

    def top(self):
        if self.sp > 0:
            return self.stack[self.sp-1]
        else:
            return None
