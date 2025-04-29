
from io import StringIO
from typing import List, Tuple
from compiler.code import OpCode, OpCodeInfo


def make(OpCode: OpCode, *args):
    # return a bytes which represents the op code and its arguments
    info_obj = OpCodeInfo.get(OpCode)
    final_bytes = OpCode.bytes
    if info_obj is None:
        raise ValueError(f"Invalid OpCode: {OpCode}")
    if len(args) != len(info_obj["args_length"]):
        raise ValueError(f"Invalid number of arguments for {OpCode}")
    for index, arg in enumerate(args):
        final_bytes += int.to_bytes(arg,
                                    info_obj["args_length"][index], byteorder="big")
    return final_bytes


def unmake(bytes: bytes) -> Tuple[List[int], int]:
    # try parse one byte op code with its arguments
    op_num = int.from_bytes(bytes[0:1], byteorder="big")
    op_code = OpCode(op_num)
    try:
        info_obj = OpCodeInfo[op_code]
    except KeyError:
        raise ValueError(f"Invalid OpCode: {op_code}")
    para_list = []
    offset = 1
    for arg_len in info_obj["args_length"]:
        para_list.append(int.from_bytes(
            bytes[offset:offset+arg_len], byteorder="big"))
        offset += arg_len
    return para_list, offset


def print_bytecode(bytes: bytes):
    i = 0
    finalString = ""
    while True:
        try:
            info = OpCodeInfo[OpCode(int.from_bytes(
                bytes[i:i+1], byteorder="big"))]
            para_list, offset = unmake(bytes[i:])
        except Exception as e:
            print(f"Error: {e}")
            print(bytes[i:i+1])
            break

        finalString += f"{i:04d} {info['name']} {para_list}\n"
        i += offset
        if i >= len(bytes):
            break
    return finalString[:-1]
