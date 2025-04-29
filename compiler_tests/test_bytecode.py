from functools import reduce
import pytest
from compiler.code import OpCode
from compiler.make import make, print_bytecode, unmake


def test_make_code():
    # big endian yhe big part ff should comes first
    assert make(OpCode.CONST, 65534) == b'\x00\xff\xfe'
    with pytest.raises(AssertionError):
        assert make(OpCode.CONST, 65534) == b'\x00\x01\x00'
    with pytest.raises(OverflowError):
        make(OpCode.CONST, 65536)
    with pytest.raises(ValueError):
        make(OpCode.CONST)
    # add test
    assert make(OpCode.ADD) == OpCode.ADD.bytes


def test_bytecode_to_string():
    bytecodes = [
        make(OpCode.CONST, 0),
        make(OpCode.CONST, 1),
        make(OpCode.ADD),
    ]
    bytecodes = b''.join(bytecodes)
    expected_string = """0000 CONST [0]\n0003 CONST [1]\n0006 ADD []"""
    print(expected_string)
    print(print_bytecode(bytecodes))
    assert expected_string == print_bytecode(bytecodes)


def test_decode_bytecode():
    bytecode = [
        make(OpCode.CONST, 0),
        make(OpCode.CONST, 1),
        make(OpCode.ADD),
    ]
    expected_result = [
        ([0], 3),
        ([1], 3),
        ([], 1),
    ]
    decode_result = [unmake(bytecode[i])
                     for i in range(len(bytecode))]
    assert expected_result == decode_result
