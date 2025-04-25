# test
from eval.object import Boolean, Integer, ycObject
from parser.node import *
from parser.parser import *
import unittest


def test_let_statement(self: unittest.TestCase, stmt: Statement, name):
    # check if the statement is a let statement
    self.assertIsInstance(stmt, LetStatement, "stmt is not a let statement")

    # i have to use a if to make the type narrowing work
    if isinstance(stmt, LetStatement):
        self.assertEqual(stmt.identifier.value, name,
                         "identifier is not correct ")
    # check if the right expression is correct
        self.assertEqual(stmt.identifier.token_literal(),
                         name, "token literal dont work")


def test_identifier(self: unittest.TestCase, exp: Expression, value):
    # check if it is an identifier
    self.assertIsInstance(exp, Identifier)
    # check if the value is correct
    if isinstance(exp, Identifier):
        self.assertEqual(exp.value, value)


def test_integer_literal(self: unittest.TestCase, exp: Expression, value):
    # check if it is an integer literal
    self.assertIsInstance(exp, IntegerLiteral)
    # check if the value is correct
    if isinstance(exp, IntegerLiteral):
        self.assertEqual(exp.value, value)


def test_infix_expression(self: unittest.TestCase, exp: Expression, left: Expression, operator: Token, right: Expression):
    # check if it is an infix expression
    self.assertIsInstance(exp, InfixExpression)
    # check if the left expression is correct
    if isinstance(exp, InfixExpression):
        self.assertEqual(exp.left, left)
        # check if the operator is correct
        self.assertEqual(exp.token, operator)
        # check if the right expression is correct
        self.assertEqual(exp.right, right)


def get_statements_from_str(code: str):
    lexer = Lexer(code)
    parser = Parser(lexer)
    program = parser.parse_program()
    return program.statements


def test_if_expression_impl(self: unittest.TestCase, ifexp: Expression, condition: Expression, consequence: BlockStatement, alternative: BlockStatement):
    # check if it is a if expression
    self.assertIsInstance(ifexp, IfExpression)
    # check if condition is equal
    if isinstance(ifexp, IfExpression):
        self.assertEqual(ifexp.condition, condition)
        # check if consequence is equal

        self.assertEqual(ifexp.true_branch, consequence)
        if alternative is not None:
            # check if alternative is equal
            self.assertEqual(ifexp.false_branch, alternative)


def test_if_expression(self, ifexp: Expression, condition: str, consequence: str, alternative: str):
    condition_exp = get_statements_from_str(condition)[0].expression
    consequence_block = BlockStatement(
        token=Token(TokenType=TokenTypes.LBRACE, Literal="{"))
    consequence_block.statements = get_statements_from_str(consequence)
    if alternative is not None:
        alternative_block = BlockStatement(
            token=Token(TokenType=TokenTypes.LBRACE, Literal="{"))
        alternative_block.statements = get_statements_from_str(alternative)
    else:
        alternative_block = None

    return test_if_expression_impl(self, ifexp, condition_exp, consequence_block, alternative_block)


def test_function_literal(self: unittest.TestCase, exp: Expression, params: List[str], body: str):
    Identifier_list = [Identifier(token=Token(
        TokenType=TokenTypes.IDENT, Literal=param)) for param in params]
    block_stmts = get_statements_from_str(body)

    # check if it is a function literal

    self.assertIsInstance(exp, FunctionLiteral)
    # check if the parameters are correct
    if isinstance(exp, FunctionLiteral):
        self.assertEqual(exp.parameters, Identifier_list)
        # check if the body is correct

        self.assertIsNotNone(exp.body, "Function body is None")
        if exp.body is not None:
            self.assertEqual(exp.body.statements, block_stmts)


def test_call_expression(self: unittest.TestCase, exp: Expression, function: str, params: List[str]):
    Expression_list = [get_statements_from_str(
        param)[0].expression for param in params]
    self.assertIsInstance(exp, CallExpression)
    if isinstance(exp, CallExpression):
        self.assertEqual(get_statements_from_str(
            function)[0].expression, exp.function)
        self.assertEqual(Expression_list, exp.parameters)


def print_if_error(self: unittest.TestCase, parser: Parser):
    if len(parser.errors) > 0:
        print("parser has errors")
        for error in parser.errors:
            print(error)


def test_integer(self: unittest.TestCase, evalResult: ycObject, val: int):
    self.assertIsInstance(evalResult, Integer)
    if isinstance(evalResult, Integer):
        self.assertEqual(val, evalResult.inspect())


def test_boolean(self: unittest.TestCase, evalResult: ycObject, val: bool):
    self.assertIsInstance(evalResult, Boolean)
    if isinstance(evalResult, Boolean):
        self.assertEqual(val, evalResult.inspect())


def test_hash_literal(self: unittest.TestCase, hash: Expression, keys: List[str], values: List[str]):
    self.assertIsInstance(hash, HashLiteral)
    if isinstance(hash, HashLiteral):
        hash_k = hash.raw_keys
        hash_v = hash.raw_values
        hash_k = [node.value for node in hash_k]
        hash_v = [node.value for node in hash_v]
        self.assertEqual(hash_k, keys)
        self.assertEqual(hash_v, values)


def test_macro_literal(self: unittest.TestCase, exp: Expression, params: List[str], body: str):
    Identifier_list = [Identifier(token=Token(
        TokenType=TokenTypes.IDENT, Literal=param)) for param in params]
    block_stmts = get_statements_from_str(body)

    # check if it is a function literal

    self.assertIsInstance(exp, Macro)
    # check if the parameters are correct
    if isinstance(exp, Macro):
        self.assertEqual(exp.parameters, Identifier_list)
        # check if the body is correct

        self.assertIsNotNone(exp.body, "Function body is None")
        if exp.body is not None:
            self.assertEqual(exp.body.statements, block_stmts)
