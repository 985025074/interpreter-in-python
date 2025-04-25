

from eval.env import Environment
from eval.eval import quote, ycEval
from eval.modify import modify
from eval.object import Quote
from parser.node import CallExpression, Expression, ExpressionStatement, LetStatement, Macro, Node, Program, Statement


def is_macro_define(stmt: Statement):
    # let statement
    if isinstance(stmt, LetStatement):
        if isinstance(stmt.right_expression, Macro):
            return True
        else:
            return False
    return False


def is_macro_call(stmt: Expression, env: Environment):
    if isinstance(stmt, CallExpression):
        if env.has_key_recursive(stmt.function.value):
            possible_macro = env.get_var_recursive(stmt.function.value)
            if isinstance(possible_macro, Macro):
                return True, possible_macro
    return False, None


def handle_macro(program: Program, env: Environment):
    macro_line = []
    for index, stmt in enumerate(program.statements):
        if is_macro_define(stmt):
            # add macro to env:
            # type narrow

            if not (isinstance(stmt, LetStatement) and isinstance(stmt.right_expression, Macro)):
                return None  # should never happen
            if env.has_key(stmt.identifier.value):
                return None  # TODO
            env.set_var(stmt.identifier.value, stmt.right_expression)
            macro_line.append(index)
    # remove macro definition from program:
    for index in macro_line[::-1]:
        program.statements.pop(index)


def expand_macro_node(node: Node, env: Environment):
    result, macro = is_macro_call(node, env)
    if not result:
        return node
    else:
        if not isinstance(node, CallExpression) or not isinstance(macro, Macro):
            return node  # never happend
        var_name = [identifier.value for identifier in macro.parameters]
        paras = [Quote(param) for param in node.parameters]
        kv = dict(zip(var_name, paras))
        newEnv = env.extended_with(kv)
        expanded = ycEval(macro.body, newEnv)
        if not isinstance(expanded, Quote):
            raise Exception("macro must return quote object(quote)")
        return expanded.node


def expand_macro(program: Program, env: Environment):
    return modify(program, lambda node: expand_macro_node(node, env))
