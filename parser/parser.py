import time
from typing import List
from lexer.lexer import Lexer, TokenTypes, Token
from .node import ArrayExpression, BlockStatement, BooleanLiteral, CallExpression, EmptyExpression, Expression, ExpressionStatement, FunctionLiteral, HashLiteral, Identifier, IfExpression, IndexExpression, InfixExpression, IntegerLiteral, LetStatement, PreFixExpression, Program, ReturnStatement, StringLiteral
from enum import Enum, IntEnum

# 优先级


class Priority(IntEnum):
    LOWEST = 0
    EQUALS = 1
    LESSGREATER = 2
    SUM = 3
    PRODUCT = 4
    PREFIX = 5
    CALL = 6
    INDEX = 7


TokenTypesToPriority = {
    TokenTypes.EQ: Priority.EQUALS,
    TokenTypes.NOT_EQ: Priority.EQUALS,
    TokenTypes.LT: Priority.LESSGREATER,
    TokenTypes.GT: Priority.LESSGREATER,
    TokenTypes.LTE: Priority.LESSGREATER,
    TokenTypes.GTE: Priority.LESSGREATER,
    TokenTypes.PLUS: Priority.SUM,
    TokenTypes.MINUS: Priority.SUM,
    TokenTypes.SLASH: Priority.PRODUCT,
    TokenTypes.ASTERISK: Priority.PRODUCT,
    TokenTypes.LPAREN: Priority.CALL,
    TokenTypes.LBRACKET: Priority.INDEX,
}


class ParseException(Exception):
    pass

# expression parse flow:
# other statement? no ->
# parse_expression_statement->
# parse_expression {expression contains prefix expression,identifier,integer...}
# -> try parse_prefix_expression first{contain:integer,identifier,and bang! or others}
#


class Parser:
    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        self.current_token: Token = Token(TokenTypes.ILLEGAL, "")
        self.next_token: Token = Token(TokenTypes.ILLEGAL, "")
        self.errors: List[ParseException] = []
        self.advance_token()
        self.advance_token()
        self.token_to_node_map = {
            TokenTypes.LET: self.parse_let_statement,
            TokenTypes.RETURN: self.parse_return_statement,

        }
        self.prefix_parse_functions = {
            TokenTypes.IDENT: self.parse_identifier,
            TokenTypes.INT: self.parse_integer,
            TokenTypes.BANG: self.parse_prefix,
            TokenTypes.MINUS: self.parse_prefix,
            TokenTypes.TRUE: self.parse_boolean,
            TokenTypes.FALSE: self.parse_boolean,
            TokenTypes.LPAREN: self.parse_group,
            TokenTypes.IF: self.parse_if_expression,
            TokenTypes.FUNCTION: self.parse_function_literal,
            TokenTypes.STRING: self.parse_string,
            TokenTypes.LBRACKET: self.parse_array,
            TokenTypes.LBRACE: self.parse_hash_literal,


        }
        self.infix_parse_functions = {
            TokenTypes.EQ: self.parse_infix,
            TokenTypes.NOT_EQ: self.parse_infix,
            TokenTypes.LT: self.parse_infix,
            TokenTypes.GT: self.parse_infix,
            TokenTypes.PLUS: self.parse_infix,
            TokenTypes.MINUS: self.parse_infix,
            TokenTypes.SLASH: self.parse_infix,
            TokenTypes.ASTERISK: self.parse_infix,
            TokenTypes.LPAREN: self.parse_call,
            TokenTypes.LTE: self.parse_infix,
            TokenTypes.GTE: self.parse_infix,
            TokenTypes.LBRACKET: self.parse_index,
        }

    def advance_token(self):
        self.current_token = self.next_token
        self.next_token = self.lexer.next_token()

    def peek_token(self):
        return self.next_token

    def peek_token_priority(self):
        return TokenTypesToPriority.get(self.next_token.TokenType, Priority.LOWEST)

    def current_token_priority(self):
        return TokenTypesToPriority.get(self.current_token.TokenType, Priority.LOWEST)

    def expect_token(self, token: Token, expected_token_type: TokenTypes):
        if token.TokenType != expected_token_type:
            self.errors.append(ParseException(
                f"Expected token type {expected_token_type}, but got {token.TokenType}"))
            return False
        return True

    def peek_expect_token(self, expected_token_type: TokenTypes):
        return self.expect_token(self.peek_token(), expected_token_type)

    def peek_expect_token_advance(self, expected_token_type: TokenTypes):
        if self.expect_token(self.peek_token(), expected_token_type):
            self.advance_token()
            return True
        else:
            return False

    def cur_expect_token_advance(self, expected_token_type: TokenTypes):
        if self.expect_token(self.current_token, expected_token_type):
            self.advance_token()
            return True
        else:
            return False

    def cur_expect_token(self, expected_token_type: TokenTypes):
        return self.expect_token(self.current_token, expected_token_type)
    # each statement parse function should ensure the current_token is ";" when it ends work

    def parse_program(self) -> Program:
        root_program = Program()
        while True:
            if self.current_token.TokenType == TokenTypes.EOF:
                break
            statement = self.parse_statement()
            if statement is not None:
                root_program.statements.append(statement)
            #  this sentence will help us skip the semicolon
            self.advance_token()
        return root_program

    def parse_statement(self):
        try:
            #  check if the statement is  let state ment ? return statement?
            return self.token_to_node_map[self.current_token.TokenType]()
        except KeyError:
            #  if not,then it is expression statement.(we will add other statement like if while later)
            return self.parse_expression_statement()

    def parse_let_statement(self):
        self.cur_expect_token(TokenTypes.LET)
        let_token = self.current_token
        if not self.peek_expect_token(TokenTypes.IDENT):
            return None
        self.advance_token()
        identifier_token = self.current_token
        if not self.peek_expect_token(TokenTypes.ASSIGN):
            return None
        self.advance_token()
        # now current token is =
        self.advance_token()
        # now current token is the start of the exp
        expression = self.parse_expression(Priority.LOWEST)
        if self.next_token.TokenType == TokenTypes.SEMICOLON:
            self.advance_token()
        # now cur token is the ";"
        return LetStatement(let_token, Identifier(identifier_token), expression)

    def parse_return_statement(self):
        self.cur_expect_token(TokenTypes.RETURN)
        return_token = self.current_token
        self.advance_token()
        if self.current_token.TokenType != TokenTypes.SEMICOLON and self.current_token.TokenType != TokenTypes.EOF:
            expression = self.parse_expression(Priority.LOWEST)

        else:
            expression = EmptyExpression()
        if self.next_token.TokenType == TokenTypes.SEMICOLON:
            self.advance_token()
        return ReturnStatement(return_token, expression)

    def parse_expression_statement(self):
        expression = ExpressionStatement(self.current_token, None)
        expression.expression = self.parse_expression(Priority.LOWEST)
        # in normal case we should advance here,so that the parse_program will skip the semicolon
        # only advance if next is ";",this is for repl's sake.
        if self.peek_token().TokenType == TokenTypes.SEMICOLON:
            self.advance_token()
        return expression
    #  hey! attetion: for expression parse,
    # you just need to keep the curToken's position = semicon -1 after each Expression parsed,
    # we will advance token outside(with a special check)
    #                                               a+1=5;
    # in other word: after parse_expression,loc is here:^(5)
    # this is diff from parse statement!

    def parse_expression(self, priority: Priority):
        # i dont like the description in the book about here
        # maybe my explanation will help?
        # priority means the expression being constructed's level.
        # if the priority is higher ,it should lay on the deeper location
        # so consider if we are constructing a expression,and we run into this function
        # we get left expression by the current token( a number) and keep going,
        # if we access a op with higher priority,we will recursively run this function again
        # ,until the final right node is finished
        try:

            prefix_parse_function = self.prefix_parse_functions[self.current_token.TokenType]
            left_expression = prefix_parse_function()

            while self.peek_token().TokenType != TokenTypes.SEMICOLON and priority < self.peek_token_priority():
                self.advance_token()

                # TODO: NO INFIX HANDLE

                left_expression = self.infix_parse_functions[self.current_token.TokenType](
                    left=left_expression)

            return left_expression
        except KeyError:

            self.errors.append(ParseException(
                f"no prefix parse function,prefix token is {self.current_token.TokenType}"))
            return None

    #  outside function parse_expression ensure legality

    def parse_integer(self):
        return IntegerLiteral(self.current_token)

    def parse_string(self):
        return StringLiteral(self.current_token)

    def parse_identifier(self):
        return Identifier(self.current_token)

    def parse_boolean(self):
        return BooleanLiteral(self.current_token)

    def parse_prefix(self):
        expression = PreFixExpression(operator=self.current_token)
        self.advance_token()
        expression.right = self.parse_expression(Priority.PREFIX)
        return expression
    # attention:we have a argument left here

    def parse_infix(self, left: Expression):

        expression = InfixExpression(
            left=left, operator=self.current_token, right=EmptyExpression())
        temp_priority = self.current_token_priority()
        self.advance_token()
        expression.right = self.parse_expression(temp_priority)

        return expression

    def parse_group(self):
        self.advance_token()
        # this is not safe
        if self.current_token.TokenType == TokenTypes.RPAREN:
            return None
        expression = self.parse_expression(Priority.LOWEST)
        if not self.peek_expect_token(TokenTypes.RPAREN):
            return None
        self.advance_token()

        return expression

    def parse_block_statement(self, not_consume_last=True):
        block_statement = BlockStatement(self.current_token)
        if not self.cur_expect_token_advance(TokenTypes.LBRACE):
            return None
        while True:
            if self.current_token.TokenType == TokenTypes.RBRACE:
                break
            statement = self.parse_statement()
            if statement is not None:
                block_statement.statements.append(statement)
            #  this sentence will help us skip the semicolon
            self.advance_token()
        # consume  }
        if not not_consume_last:
            if not self.cur_expect_token_advance(TokenTypes.RBRACE):
                return None
        return block_statement

    def parse_if_expression(self):
        if_expression = IfExpression(self.current_token)
        # consume if
        self.advance_token()
        # consume (
        if not self.cur_expect_token_advance(TokenTypes.LPAREN):
            return None

        # parse condition
        if_expression.condition = self.parse_expression(Priority.LOWEST)
        self.advance_token()
        # consume )
        if not self.cur_expect_token_advance(TokenTypes.RPAREN):
            return None

        # we dont need consume the { }manually,parseblock will do the work
        if_expression.true_branch = self.parse_block_statement(
            not_consume_last=True)
        if not self.cur_expect_token(TokenTypes.RBRACE):
            return None
        if self.next_token.TokenType == TokenTypes.ELSE:
            # now is else
            if not self.peek_expect_token_advance(TokenTypes.ELSE):
                return None
            # now is {
            if not self.peek_expect_token_advance(TokenTypes.LBRACE):
                return None
            if_expression.false_branch = self.parse_block_statement(
                not_consume_last=True)
            if not self.cur_expect_token(TokenTypes.RBRACE):
                return None
        return if_expression

    def parse_array(self):
        array_literal = ArrayExpression(self.current_token)
        array_exp = []
        self.advance_token()
        while True:
            if self.current_token.TokenType == TokenTypes.RBRACKET:
                break
            array_exp.append(self.parse_expression(Priority.LOWEST))
            self.advance_token()
            if self.current_token.TokenType == TokenTypes.RBRACKET:
                break

            if self.cur_expect_token(TokenTypes.COMMA):
                self.advance_token()
        array_literal.elements = array_exp
        return array_literal

    def parse_function_literal(self):
        function_literal = FunctionLiteral(self.current_token)
        # consume function
        self.advance_token()
        # consume (
        if not self.cur_expect_token_advance(TokenTypes.LPAREN):
            return None
        # parse_list here
        Identifier_list = []
        while self.current_token.TokenType != TokenTypes.RPAREN:

            Identifier_list.append(self.parse_identifier())
            if not self.cur_expect_token_advance(TokenTypes.IDENT):
                return None
            if self.current_token.TokenType != TokenTypes.RPAREN:
                if not self.cur_expect_token_advance(TokenTypes.COMMA):
                    return None

        # consume )
        if not self.cur_expect_token_advance(TokenTypes.RPAREN):
            return None
        function_literal.body = self.parse_block_statement(
            not_consume_last=True)
        function_literal.parameters = Identifier_list

        return function_literal

    def parse_index(self, left):
        index_exp = IndexExpression(self.current_token)
        self.advance_token()
        index_exp.left = left
        if self.current_token.TokenType != TokenTypes.RBRACKET:
            index_exp.index = self.parse_expression(Priority.LOWEST)
            self.advance_token()
        else:
            index_exp.index = None
        if not self.cur_expect_token(TokenTypes.RBRACKET):
            return None
        return index_exp

    def parse_call(self, left):

        if not self.cur_expect_token_advance(TokenTypes.LPAREN):
            return None
        callexpression = CallExpression(self.current_token)
        # parse expressionList:
        Expression_list = []
        while self.current_token.TokenType != TokenTypes.RPAREN:

            Expression_list.append(self.parse_expression(Priority.LOWEST))
            self.advance_token()
            if self.current_token.TokenType != TokenTypes.RPAREN:
                if not self.cur_expect_token_advance(TokenTypes.COMMA):
                    return None
        callexpression.function = left
        callexpression.parameters = Expression_list
        return callexpression

    def parse_hash_literal(self):
        hash_literal = HashLiteral(self.current_token)
        key = []
        value = []
        self.advance_token()
        while self.current_token.TokenType != TokenTypes.RBRACE:
            k = self.parse_expression(Priority.LOWEST)
            self.advance_token()
            if not self.cur_expect_token_advance(TokenTypes.COLON):
                return None
            v = self.parse_expression(Priority.LOWEST)
            self.advance_token()
            key.append(k)
            value.append(v)
            if self.current_token.TokenType != TokenTypes.RBRACE:
                if not self.cur_expect_token_advance(TokenTypes.COMMA):
                    return None
        hash_literal.raw_keys = key
        hash_literal.raw_values = value
        if not self.cur_expect_token(TokenTypes.RBRACE):
            return None
        return hash_literal

    def just_pass(self):
        while self.current_token.TokenType != TokenTypes.SEMICOLON:
            self.advance_token()
        return EmptyExpression()
