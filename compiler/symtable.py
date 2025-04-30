from enum import Enum


class Scope(Enum):
    GLOBAL = 1


class ycSymbol:
    def __init__(self, name: str, scope: Scope, index: int):
        self.name = name
        self.scope = scope
        self.index = index


class SymTable:
    def __init__(self):
        self.symbols = {}

    def add_symbol(self, name, scope):
        self.symbols[name] = ycSymbol(name, scope, len(self.symbols))
        return self.symbols[name]

    def resolve_symbol(self, name):
        if name in self.symbols:
            return self.symbols[name]
        else:
            return None
