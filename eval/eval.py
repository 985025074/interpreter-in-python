

from types import NoneType
from typing import Callable, Dict, Hashable
from eval.builtin_func import BuiltinFunction
from eval.env import Environment
from parser.node import Node
from eval.object import *
from parser.node import *
from eval.modify import modify
NULL = Null()
TRUE = Boolean(True)
FALSE = Boolean(False)
default_env = Environment()

# quote
def evalUnquote(node: Expression, env: Environment):
    if isinstance(node, CallExpression) and isinstance(node.function, Identifier) and node.function.value == "unquote":
        if node.parameters is not None and len(node.parameters) == 1:
            return turnObjectToNode(ycEval(node.parameters[0], env))

    return node


def quote(node: Expression, env: Environment):
    node = modify(node, lambda node: evalUnquote(node, env))
    return Quote(node)

def evalBoolean(bool_node: BooleanLiteral, env: Environment):
    if bool_node.value:
        return TRUE
    else:
        return FALSE


def evalInteger(int_node: IntegerLiteral, env: Environment):
    return Integer(int_node.value)


def evalString(string_node: StringLiteral, env: Environment):
    return String(string_node.value)


def evalProgram(p_node: Program, env: Environment):
    result: ycObject = NULL
    for stmt in p_node.statements:

        result = ycEval(stmt, env)
        if result.type() == ObjectType.RETURN or result.type() == ObjectType.ERROR:
            return result
    return result


def evalExpressionStatement(stmt: ExpressionStatement, env: Environment):
    return ycEval(stmt.expression, env)


def handleBang(right_val: ycObject):
    if not hasattr(right_val, "value"):
        return Error(f"unknown operator: !{right_val.type()}")
    match right_val.value:
        case True:
            return FALSE
        case False:
            return TRUE
        case "Null":
            return TRUE
        case _:  # Wildcard case moved to the end
            return FALSE


def handleInfix(op_token: Token, left_val: ycObject, right_val: ycObject):
    if not hasattr(left_val, "value") or not hasattr(right_val, "value"):
        return Error(f"type mismatch: {left_val.type()} {op_token.Literal} {right_val.type()}")
    if left_val.type() != right_val.type():
        return Error(f"type mismatch: {left_val.type()} {op_token.Literal} {right_val.type()}")
    match op_token.TokenType:
        case TokenTypes.EQ:
            return TRUE if left_val.value == right_val.value else FALSE
        case TokenTypes.NOT_EQ:
            return FALSE if left_val.value == right_val.value else TRUE
        case TokenTypes.GT:
            return TRUE if left_val.value > right_val.value else FALSE
        case TokenTypes.LT:
            return TRUE if left_val.value < right_val.value else FALSE
        case TokenTypes.GTE:
            return TRUE if left_val.value >= right_val.value else FALSE
        case TokenTypes.LTE:
            return TRUE if left_val.value <= right_val.value else FALSE
    if type(left_val) == String and op_token.TokenType == TokenTypes.PLUS:
        return String(left_val.value + right_val.value)
    if type(left_val) != Integer:
        return Error(f"unknown operator: {left_val.type()} {op_token.Literal} {right_val.type()}")
    match op_token.TokenType:
        case TokenTypes.MINUS:
            return Integer(left_val.value - right_val.value)
        case TokenTypes.PLUS:
            return Integer(left_val.value + right_val.value)
        case TokenTypes.SLASH:
            return Integer(left_val.value / right_val.value)
        case TokenTypes.ASTERISK:
            return Integer(left_val.value * right_val.value)
        case _:
            return Error(f"unknown operator: {left_val.inspect()} {op_token.Literal} {right_val.inspect()}")


def evalPrefixExpression(prefix_exp: PreFixExpression, env: Environment):
    if prefix_exp.right is None or prefix_exp.token is None:
        return NULL
    right_val = ycEval(prefix_exp.right, env)
    match prefix_exp.token.TokenType if prefix_exp.token is not None else None:
        case TokenTypes.MINUS:
            if isinstance(right_val, Integer):
                return Integer(-right_val.inspect())
            return Error(f"unknown operator: {prefix_exp.token.Literal}{right_val.type()}")
        case TokenTypes.BANG:
            return handleBang(right_val)
        case _:
            return Error(f"unknown operator: {prefix_exp.token.Literal}{right_val.type()}")


def evalInfixExpression(infix_exp: InfixExpression, env: Environment):
    if infix_exp.left is None or infix_exp.right is None:
        return NULL
    right_val = ycEval(infix_exp.right, env)
    left_val = ycEval(infix_exp.left, env)

    return handleInfix(infix_exp.token, left_val, right_val)


def isTrue(r: ycObject):
    if r is TRUE:
        return True
    elif r is FALSE:
        return False
    elif r is NULL:
        return False
    else:
        return True


def evalIfExpression(if_exp: IfExpression, env: Environment):
    if not if_exp.condition:
        return NULL
    if isTrue(ycEval(if_exp.condition, env)):
        if if_exp.true_branch:
            return ycEval(if_exp.true_branch, env)
    else:
        if if_exp.false_branch:
            return ycEval(if_exp.false_branch, env)
    return NULL


def evalReturnStatement(ret_stmt: ReturnStatement, env: Environment):
    if not ret_stmt.return_value:
        return None
    return ReturnObject(ycEval(ret_stmt.return_value, env))


def evalError(error: Error):
    return error


def evalLetStatement(let_stmt: LetStatement, env: Environment):
    right_obj = ycEval(let_stmt.right_expression, env)
    if right_obj.type() == ObjectType.ERROR:
        return right_obj
    if env.has_key(let_stmt.identifier.value):
        return Error(f"identifier {let_stmt.identifier.value} already declared in this scope")
    env.set_var(let_stmt.identifier.value, right_obj)
    return NULL


def evalIdentifier(identifier: Identifier, env: Environment):
    if env.has_key_recursive(identifier.value):
        return env.get_var_recursive(identifier.value)
    elif identifier.value in BuiltinFunction:
        return BuiltinFunction[identifier.value]
    else:
        return Error(f"identifier not found:{identifier.value}")


def evalFunctionLiteral(func_lit: FunctionLiteral, env: Environment):
    params = [param for param in func_lit.parameters]
    body = func_lit.body
    return Function(params, body, env)


def unwrapReturn(obj: ycObject):
    if isinstance(obj, ReturnObject):
        return obj.value
    else:
        return obj


def applyFunction(function: Function | Builtin, evaled_para):

    if isinstance(function, Function):
        if len(evaled_para) != len(function.params):
            return Error("wrong number of arguments: expected " + str(len(function.params)) + ", got " + str(len(evaled_para)))
        param_names = [param.value for param in function.params]
        new_env = function.env.extended_with(
            dict(zip(param_names, evaled_para)))
        return unwrapReturn(ycEval(function.body, new_env))
    else:

        return function.fn(*evaled_para)


def evalCallExpression(calledFunction: CallExpression, env: Environment):
    if calledFunction.function is None:
        return Error("function not found")
    # quote handle：
    if isinstance(calledFunction.function, Identifier) and calledFunction.function.value == "quote":
        return quote(calledFunction.parameters[0], env)
    function = ycEval(calledFunction.function, env)
    if isinstance(function, Error):
        return function
    if not isinstance(function, Function) and not isinstance(function, Builtin):
        return Error(str(function) + "not a function")
    para_list = calledFunction.parameters
    if para_list is None:
        return Error("paralist is None!,function is:"
                     + str(function))
    evaled_para: List[ycObject] = []
    for para in para_list:
        evaled_p = ycEval(para, env)
        if isinstance(evaled_para, Error):
            return evaled_p
        evaled_para.append(evaled_p)
    return applyFunction(function, evaled_para)


def evalArray(array_exp: ArrayExpression, env: Environment):
    if array_exp.elements is None:
        return NULL
    Array_obj = Array([])
    for element in array_exp.elements:
        Array_obj.elements.append(ycEval(element, env))
    return Array_obj


def evalIndexExpression(index_exp: IndexExpression, env: Environment):
    if index_exp.left is None or index_exp.index is None:
        return NULL
    left_val = ycEval(index_exp.left, env)
    index_val = ycEval(index_exp.index, env)
    if not isinstance(left_val, Array) and not isinstance(left_val, Hash):
        return Error(f"index operator not supported for {left_val.type()}")
    if isinstance(left_val, Array):
        if not isinstance(index_val, Integer):
            return Error(f"index operator not supported for {index_val.type()}")
        if index_val.value < 0:
            index_val = Integer(len(left_val.elements) + index_val.value)
        if index_val.value < 0 or index_val.value >= len(left_val.elements):
            return Error(f"index out of range: {index_val.value}")
        return left_val.elements[index_val.value]
    elif isinstance(left_val, Hash):
        if not isinstance(index_val, HashAble):
            return Error(f"index operator not hashbale for {index_val.type()}")
        if index_val.hash_key() not in left_val.pairs.keys():
            return Error(f"key not found: {index_val}")
        return left_val.pairs[index_val.hash_key()].value
    else:
        return Error(f"index operator not supported for {left_val.type()}")


def evalHashLiteral(hash_exp: HashLiteral, env: Environment):
    hash_obj = Hash({})
    if hash_exp.raw_keys is None or hash_exp.raw_values is None:
        return Hash({})
    for k, v in zip(hash_exp.raw_keys, hash_exp.raw_values):
        hashable = ycEval(k, env)
        if not isinstance(hashable, HashAble):
            return Error(f"key is not a valid type: {hashable.type()}")
        hashkey = hashable.hash_key()
        if hashkey in hash_obj.pairs:
            return Error(f"duplicate key: {hashkey.value}")
        value = ycEval(v, env)
        hash_obj.pairs[hashkey] = HashPair(hashable, value)
    return hash_obj


def evalNone(obj: None, env: Environment):
    return NULL


NodeToEval: Dict[type, Callable] = {
    BooleanLiteral: evalBoolean,
    IntegerLiteral: evalInteger,
    Program: evalProgram,
    ExpressionStatement: evalExpressionStatement,
    InfixExpression: evalInfixExpression,
    PreFixExpression: evalPrefixExpression,
    IfExpression: evalIfExpression,
    BlockStatement: evalProgram,
    ReturnStatement: evalReturnStatement,
    Error: evalError,
    LetStatement: evalLetStatement,
    Identifier: evalIdentifier,
    FunctionLiteral: evalFunctionLiteral,
    CallExpression: evalCallExpression,
    StringLiteral: evalString,
    ArrayExpression: evalArray,
    IndexExpression: evalIndexExpression,
    HashLiteral: evalHashLiteral,
    NoneType: evalNone

}


def ycEval(node: Node, env: Environment = default_env) -> ycObject:
    try:
        evalFunc = NodeToEval[type(node)]
        return evalFunc(node, env)
    except:

        return Error("unknown node type: " + str(type(node)))
