
from compiler.builtin_funcs import BuiltinWrapper
from compiler.code import OpCode
from compiler.compiledfunction import CompiledFunction
from compiler.compiler import Bytecode
from compiler.math_compute import compute
from eval.eval import FALSE, TRUE, handleBang, NULL
from eval.object import Array, Hash, HashAble, HashKey, HashPair, Integer, String, ycObject, Boolean
from compiler.frame import Frame


class VM:
    def __init__(self, bytecode: Bytecode = None):
        # machine stack
        self.stack = []
        # note : sp points the len(stack) + 1 loc
        self.sp = 0
        # storeglobal varaiables
        self.globals = [0 for i in range(65535)]
        self.frame_stack = [0 for i in range(65535)]
        self.frame_stack[0] = Frame(bytecode.instructions)
        self.frame_index = 0
        self.const = bytecode.constants

    @property
    def current_frame(self):
        return self.frame_stack[self.frame_index]

    @current_frame.setter
    def current_frame(self, frame):
        self.frame_stack[self.frame_index] = frame

    @property
    def instructions(self):
        return self.frame_stack[self.frame_index].instructions

    @property
    def pc(self):
        return self.frame_stack[self.frame_index].pc

    @instructions.setter
    def instructions(self, instructions):
        self.frame_stack[self.frame_index].instructions = instructions

    @pc.setter
    def pc(self, pc: int):
        self.frame_stack[self.frame_index].pc = pc

    def builtin_call(self, functionwrapper: BuiltinWrapper, num_args: int):
        args = []
        for i in range(num_args):
            args.insert(0, self.pop())
        result = functionwrapper.func(*args)
        # pop func itself
        assert isinstance(self.top(), BuiltinWrapper)
        self.pop()
        self.push(result)


    def run(self):
        instructions = self.instructions
        pc = self.pc
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
                    self.push(self.const[index])
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
                case OpCode.LOAD_BUILTIN:

                    
                    index = int.from_bytes(
                        instructions[pc+1:pc+2], byteorder='big')
                    self.push(BuiltinWrapper.generate_from_index(index))
                    pc += 2
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
                case OpCode.CALL:
                    # save the current frame
                    num_args = int.from_bytes(
                        instructions[pc+1:pc+2], byteorder='big')
                    compiled_function = self.stack[self.sp-num_args-1]
                    
                    if isinstance(compiled_function, BuiltinWrapper):
                        self.builtin_call(compiled_function, num_args)
                        pc += 2
                    else:
                        self.current_frame.pc = pc + 2
                        assert isinstance(compiled_function, CompiledFunction)
                        if num_args != compiled_function.num_args:
                            raise Exception("num_args not match")
                        self.frame_index += 1

                        self.current_frame = Frame(
                            compiled_function.instructions, pc=0, bp=self.sp-num_args)
                        # allocate space for local variables
                        for i in range(compiled_function.num_locals):
                            self.push(NULL)

                        pc = self.current_frame.pc
                        instructions = self.current_frame.instructions

                case OpCode.RETURN:

                    rt = self.pop()
                    # print("return value:", rt)
                    # print("now stack", [str(i) for i in self.stack[:10]])
                    # print("now sp", self.sp)

                    pc += 1
                    self.current_frame.pc = pc
                    old_frame = self.current_frame

                    self.frame_index -= 1
                    pc = self.current_frame.pc
                    instructions = self.current_frame.instructions
                    self.sp = old_frame.bp - 1

                    # print("old fram bp", old_frame.bp)
                    # print("fram stack", self.frame_stack[:10])
                    assert isinstance(self.stack[self.sp], CompiledFunction)
                    # -1 means popping the compiled function
                    self.push(rt)
                case OpCode.RETURN_NULL:
                    pc += 1
                    self.current_frame.pc = pc

                    self.frame_index -= 1
                    pc = self.current_frame.pc
                    instructions = self.current_frame.instructions
                    self.sp = self.current_frame.bp - 1
                    # print(self.stack[self.sp])
                    assert isinstance(self.stack[self.sp], CompiledFunction)
                    self.push(NULL)
                case OpCode.SETLOCAL:
                    index = int.from_bytes(
                        instructions[pc+1:pc+3], byteorder='big')
                    # print(self.stack[:10])
                    # print(self.current_frame.bp, index)
                    self.stack[self.current_frame.bp+index] = self.pop()
                    pc += 3
                case OpCode.GETLOCAL:
                    index = int.from_bytes(
                        instructions[pc+1:pc+3], byteorder='big')
                    self.push(self.stack[self.current_frame.bp+index])
                    pc += 3

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
