from typing import Callable
from eval.env import Environment

from eval.object import Quote
from parser.node import *


def modify(ast_node: Node, func: Callable):
    if isinstance(ast_node, Program):
        for index, statement in enumerate(ast_node.statements):
            ast_node.statements[index] = modify(statement, func)
    elif isinstance(ast_node, ExpressionStatement):
        ast_node.expression = modify(ast_node.expression, func)
    elif isinstance(ast_node, InfixExpression):
        ast_node.left = modify(ast_node.left, func)
        ast_node.right = modify(ast_node.right, func)
    elif isinstance(ast_node, PreFixExpression):
        ast_node.right = modify(ast_node.right, func)
    elif isinstance(ast_node, IndexExpression):
        ast_node.left = modify(ast_node.left, func)
        ast_node.index = modify(ast_node.index, func)
    elif isinstance(ast_node, BlockStatement):
        for index, statement in enumerate(ast_node.statements):
            ast_node.statements[index] = modify(statement, func)
    elif isinstance(ast_node, IfExpression):
        ast_node.condition = modify(ast_node.condition, func)
        ast_node.true_branch = modify(ast_node.true_branch, func)
        ast_node.false_branch = modify(ast_node.false_branch, func)
    elif isinstance(ast_node, ReturnStatement):
        ast_node.return_value = modify(ast_node.return_value, func)

    elif isinstance(ast_node, LetStatement):
        ast_node.right_expression = modify(ast_node.right_expression, func)
        ast_node.identifier = modify(ast_node.identifier, func)
    elif isinstance(ast_node, FunctionLiteral):
        ast_node.body = modify(ast_node.body, func)
        ast_node.parameters = [modify(para, func)
                               for para in ast_node.parameters]
    elif isinstance(ast_node, ArrayExpression):
        ast_node.elements = [modify(element, func)
                             for element in ast_node.elements]
    elif isinstance(ast_node, HashLiteral):
        ast_node.raw_keys = [modify(key, func) for key in ast_node.raw_keys]
        ast_node.raw_values = [modify(value, func)
                               for value in ast_node.raw_values]

    return func(ast_node)
