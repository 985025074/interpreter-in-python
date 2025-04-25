from .token import IsDigit, LiteralToTokenMap, IsLetter, Token, TokenTypes, lookup_ident, whitespaces, special_chars


class Lexer(object):
    def __init__(self, text):
        self.text = text
        self.position = -1
        self.read_position = 0
        self.character = None
        self.read_char()

    def skip_whitespace(self):

        while self.character in whitespaces:
            self.read_char()

    def read_char(self):
        if self.read_position >= len(self.text):
            self.character = None
            return
        ch = self.text[self.read_position]
        self.position = self.read_position
        self.read_position += 1
        self.character = ch

    def read_identifier(self):
        token_literal = ""
        while self.character is not None and IsLetter(self.character):
            token_literal += self.character
            self.read_char()
        return token_literal

    def read_number(self):
        token_literal = ""
        while self.character is not None and IsDigit(self.character):
            token_literal += self.character
            self.read_char()
        return token_literal

    def read_string(self):
        token_literal = ""
        # read_first_quote "
        self.read_char()
        while self.character is not None and self.character != '"':
            token_literal += self.character
            self.read_char()
        if self.character == '"':
            self.read_char()  # read last "
        return token_literal

    def peek_char(self):
        if self.read_position >= len(self.text):
            return None
        return self.text[self.read_position]

    def next_token(self):
        # we use map to replace switch statement
        self.skip_whitespace()
        try:
            # handle special cases tokens structed by two char like "!="
            if self.character in special_chars:
                next_char = self.peek_char()
                if lookup_ident(self.character+next_char) != TokenTypes.IDENT:
                    token_ret = LiteralToTokenMap[self.character+next_char]
                    self.read_char()
                    self.read_char()
                    return token_ret
            token_ret = LiteralToTokenMap[self.character]
        except Exception:
            # check if it is a letter
            # caution! the order matters! especailly the first two stmt
            if IsDigit(self.character):
                token_ret = Token(TokenTypes.INT, self.read_number())
            elif IsLetter(self.character):
                may_be_ident = self.read_identifier()
                token_ret = Token(lookup_ident(may_be_ident), may_be_ident)
            elif self.character == '"':
                token_ret = Token(TokenTypes.STRING, self.read_string())
            else:
                token_ret = Token(TokenTypes.ILLEGAL, self.character)
                self.read_char()
            return token_ret
        self.read_char()
        return token_ret
