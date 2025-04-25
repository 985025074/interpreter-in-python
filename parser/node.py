from abc import ABC, abstractmethod
from typing import Dict, List, Optional

from lexer.token import Token, TokenTypes


class Node(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def token_literal(self):
        pass

    def __str__(self):
        return self.token_literal()


class Statement(Node):
    def __init__(self):
        pass

#  infact this should be a abstarct c


class Expression(Node):
    def __init__(self, value):
        self.value = value
        pass


class EmptyExpression(Expression):
    def __init__(self):
        pass

    def token_literal(self):
        return ""

    def __str__(self):
        return ""


class IntegerLiteral(Expression):
    def __init__(self, token: Token):
        self.token = token
        self.value = int(token.Literal)

    def token_literal(self):
        return self.token.Literal

    def __str__(self):
        return str(self.value)

    def __eq__(self, other):
        return self.value == other.value


class StringLiteral(Expression):
    def __init__(self, token: Token):
        self.token = token
        self.value = str(token.Literal)

    def token_literal(self):
        return self.token.Literal

    def __str__(self):
        return str(self.value)

    def __eq__(self, other):
        return self.value == other.value


class BooleanLiteral(Expression):
    def __init__(self, token: Token):
        self.token = token
        if token.TokenType == TokenTypes.TRUE:
            self.value = True
        else:
            self.value = False

    def token_literal(self):
        return self.token.Literal

    def __str__(self):
        return str(self.value)

    def __eq__(self, other):
        return self.value == other.value


class Identifier(Expression):
    def __init__(self, token: Token):
        self.token = token
        self.value = token.Literal

    def token_literal(self):
        return self.token.Literal

    def __str__(self):
        return self.value

    def __eq__(self, other):
        return self.value == other.value


class PreFixExpression(Expression):
    def __init__(self, *, operator: Optional[Token] = None, right: Optional[Expression] = None):
        self.token = operator  # operator token
        self.right = right

    def token_literal(self):
        return self.token.Literal

    def __str__(self):
        return f"({self.token.Literal}{self.right})"

    def __eq__(self, other):
        return self.token.Literal == other.token.Literal and self.right == other.right


class InfixExpression(Expression):
    def __init__(self, *, left: Optional[Expression] = None, operator: Optional[Token] = None, right: Optional[Expression] = None):
        self.token = operator
        self.left = left
        self.right = right

    def token_literal(self):
        return self.token.Literal

    def __str__(self):
        return f"({self.left} {self.token.Literal} {self.right})"

    def __eq__(self, other):
        return self.token.Literal == other.token.Literal and self.left == other.left and self.right == other.right


class Program(Node):
    def __init__(self) -> None:
        self.statements: List[Statement] = []

    def token_literal(self) -> str:
        if len(self.statements) > 0:
            return self.statements[0].token_literal()
        else:
            return ""

    def __str__(self):
        statement_strs = [str(statement) for statement in self.statements]
        return "".join(statement_strs)

    def print_whole_program_nicely(self):
        statement_strs = [str(statement) for statement in self.statements]
        print(";\n".join(statement_strs))


class LetStatement(Statement):
    def __init__(self, token: Token, identifier: Identifier, right_expression: Expression):
        self.token = token
        self.identifier = identifier
        self.right_expression = right_expression

    def token_literal(self):
        return self.token.Literal

    def __str__(self):
        return "let " + str(self.identifier) + " = " + str(self.right_expression)

    def __eq__(self, other):
        return self.token.Literal == other.token.Literal and self.identifier == other.identifier and self.right_expression == other.right_expression


class ReturnStatement(Statement):
    def __init__(self, token: Token, return_value: Optional[Expression]):
        self.token = token
        self.return_value = return_value

    def token_literal(self):
        return self.token.Literal

    def __str__(self):
        return "return " + str(self.return_value)

    def __eq__(self, other):
        return self.token.Literal == other.token.Literal and self.return_value == other.return_value


class ExpressionStatement(Statement):
    def __init__(self, token: Token, expression: Expression):
        self.token = token
        self.expression = expression

    def token_literal(self):
        return super().token_literal()

    def __str__(self):
        return str(self.expression)

    def __eq__(self, other):
        return self.expression == other.expression


class BlockStatement(Statement):
    def __init__(self, token: Token) -> None:
        self.token = token
        self.statements: List[Statement] = []

    def token_literal(self) -> str:
        return self.token.Literal

    def __str__(self) -> str:
        statement_strs = [str(statement) for statement in self.statements]
        if len(statement_strs) > 0:
            statement_strs[-1] += ";\n"
        return "{ " + ";\n".join(statement_strs) + "}"

    def __eq__(self, other):
        return self.token.Literal == other.token.Literal and self.statements == other.statements


class IfExpression(Expression):
    def __init__(self, token: Token, true_branch: Optional[BlockStatement] = None, false_branch: Optional[BlockStatement] = None, condition: Optional[Expression] = None):
        self.token = token
        self.true_branch = true_branch
        self.false_branch = false_branch
        self.condition = condition

    def token_literal(self):
        return self.token.Literal

    def __str__(self):
        return f"if {self.condition} {self.true_branch} else {self.false_branch}"

    def __eq__(self, other):
        return self.token.Literal == other.token.Literal and self.true_branch == other.true_branch and self.false_branch == other.false_branch and self.condition == other.condition


class FunctionLiteral(Expression):
    def __init__(self, token: Token, parameters: Optional[List[Identifier]] = None, body: Optional[BlockStatement] = None):

        self.token = token
        self.parameters = parameters
        self.body = body

    def token_literal(self):
        return self.token.Literal

    def __str__(self):
        params = ", ".join(str(param) for param in self.parameters)
        return f"function({params}) {self.body}"


class CallExpression(Expression):
    def __init__(self, token: Token, function: Optional[Expression] = None, parameters: Optional[List[Expression]] = None):
        self.token = token
        self.function = function
        self.parameters = parameters

    def token_literal(self):
        return self.token.token_literal()

    def __str__(self):
        params = ", ".join(str(param) for param in self.parameters)
        return f"{self.function}({params})"


class ArrayExpression(Expression):
    def __init__(self, token: Token, elements: Optional[List[Expression]] = None):
        self.token = token
        self.elements = elements

    def token_literal(self):
        return self.token.Literal

    def __str__(self):
        elements_str = ", ".join(str(element) for element in self.elements)
        return f"[{elements_str}]"


class IndexExpression(Expression):
    def __init__(self, token: Token, left: Optional[Expression] = None, index: Optional[Expression] = None):
        self.token = token
        self.left = left
        self.index = index

    def token_literal(self):
        return self.token.Literal

    def __str__(self):
        return f"({self.left}[{self.index}])"


class HashLiteral(Expression):
    def __init__(self, token: Token, pairs: Optional[Dict[Expression, Expression]] = None, raw_keys: Optional[List[Expression]] = None, raw_values: Optional[List[Expression]] = None):
        self.token = token
        self.pairs = pairs
        self.raw_keys = raw_keys
        self.raw_values = raw_values

    def token_literal(self):
        return self.token.Literal

    def __str__(self):
        pairs_str = ", ".join(f"{key}: {value}" for key,
                              value in self.pairs.items())
        return f"{{{pairs_str}}}"
