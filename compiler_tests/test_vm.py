
from compiler.vm import VM
from compiler_tests.utils import parse
from compiler.compiler import Compiler
from eval.eval import NULL
from eval.object import Array, Hash, Integer, Boolean


def test_vm_top():
    codes = [
        ["1", 1],
        ["2", 2],
        ["1+2", 3],
        ["1 - 2", -1],
        ["1 * 2", 2],
        ["4 / 2", 2],
        ["50 / 2 * 2 + 10 - 5", 55],
        ["5 + 5 + 5 + 5 - 10", 10],
        ["2 * 2 * 2 * 2 * 2", 32],
        ["5 * 2 + 10", 20],
        ["5 + 2 * 10", 25],
        ["5 * (2 + 10)", 60],
        ["true", True],
        ["false", False],
        ["1 < 2", True],
        ["1 > 2", False],
        ["1 < 1", False],
        ["1 > 1", False],
        ["1 == 1", True],
        ["1 != 1", False],
        ["1 == 2", False],
        ["1 != 2", True],
        ["true == true", True],
        ["false == false", True],
        ["true == false", False],
        ["true != false", True],
        ["false != true", True],
        ["(1 < 2) == true", True],
        ["(1 < 2) == false", False],
        ["(1 > 2) == true", False],
        ["(1 > 2) == false", True],
        # turn brace to bracket
        ["-5", -5],
        ["-10", -10],
        ["-50 + 100 + -]0", 0],
        ["(5 + 10 * 2 + 15 / 3) * 2 + -10", 50],
        ["!true", False],
        ["!false", True],
        ["!5", False],
        ["!!true", True],
        ["!!false", False],
        ["!!5", True],
        ["if (true) { 10 }", 10],
        ["if (true) { 10 } else { 20 }", 10],
        ["if (false) { 10 } else { 20 } ", 20],
        ["if (1) { 10 }", 10],
        ["if (1 < 2) { 10 }", 10],
        ["if (1 < 2) { 10 } else { 20 }", 10],
        ["if (1 > 2) { 10 } else { 20 }", 20],
        ["if (1 > 2) { 10 }", "Null"],
        ["if (false) { 10 }", "Null"],
        ["let one = 1; one", 1],
        ["let one = 1; let two = 2; one + two", 3],
        ["let one = 1; let two = one + one; one + two", 3],
        # string op
        [
            '"Hello, " + "World!"', "Hello, World!"
        ],
        # array
        [
            "[1,2,3]", [1, 2, 3]
        ],
        [
            "[1+1,2*3,4/2]", [2, 6, 2]
        ],
        # empty array
        [
            "[]", []
        ],
        # hash test
        [
            "{1:2, 3:4, 5:6}", {1: 2, 3: 4, 5: 6}
        ],
        [
            "{}", {}
        ],
        ["[1, 2, 3][1]", 2],
        ["[1, 2, 3][0 + 2]", 3],
        ["[[1, 1, 1]][0][0]", 1],
        ["[][0]", "Null"],
        ["[1, 2, 3][99]", "Null"],
        ["[1][-1]", 1],
        ["{1: 1, 2: 2}[1]", 1],
        ["{1: 1, 2: 2}[2]", 2],
        ["{1: 1}[0]", "Null"],
        ["{}[0]", "Null"],


    ]
    for code, expect in codes:
        compiler = Compiler()
        program = parse(code)
        compiler.compile(program)
        try:
            vm = VM(compiler.bytecodes())
            vm.run()
        except Exception as e:
            print("Error! Happen in the vm run!:", e)
            print(compiler.bytecodes().to_string())
            raise e
        try:
            if type(expect) == list:
                array_obj = vm.last_pop()
                assert isinstance(array_obj, Array)
                array_obj = array_obj.elements
                array_obj = [x.value for x in array_obj]
                assert array_obj == expect
            elif type(expect) == dict:
                hash_obj = vm.last_pop()
                assert isinstance(hash_obj, Hash)
                hash_obj = hash_obj.pairs
                hash_obj = {v.key.value: v.value.value for k,
                            v in hash_obj.items()}
                assert hash_obj == expect
            else:
                assert hasattr(vm.last_pop(), "value")
                assert vm.last_pop().value == expect
        except Exception as e:
            print(
                f"Error! {code} should return {expect}, but got {vm.last_pop()}")
            print(compiler.bytecodes().to_string())
            raise e
