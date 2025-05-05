from enum import Enum

from compiler.builtin_funcs import ret_index_builtin_func


class Scope(Enum):
    GLOBAL = 1
    LOCAL = 2
    BUILTIN = 3
    FREE = 4


class ycSymbol:
    def __init__(self, name: str, scope: Scope, index: int):
        self.name = name
        self.scope = scope
        self.index = index


class SymTable:
    def __init__(self):
        self.symbols = {}
        self.outer = None
        self.builtin_symbols = {}

    def add_symbol(self, name):
        try_resolve = self.resolve_symbol(name)
        if self.outer is None:
            self.symbols[name] = ycSymbol(
                name, Scope.GLOBAL, len(self.symbols))
        elif try_resolve is not None:
            raise Exception(
                f"Symbol {name} already exists in the global scope")
        else:
            self.symbols[name] = ycSymbol(name, Scope.LOCAL, len(self.symbols))

        return self.symbols[name]

    def add_builtin_symbol(self, name):
        self.builtin_symbols[name] = ycSymbol(
            name, Scope.BUILTIN, len(self.builtin_symbols))
        return self.builtin_symbols[name]

    def add_free_symbol(self, name):
        self.symbols[name] = ycSymbol(name, Scope.FREE, len(self.symbols))
        return self.symbols[name]

    def resolve_symbol(self, name):
        # users symbols have higher priority than built-in symbols
        if name in self.symbols:
            return self.symbols[name]
        elif name in self.builtin_symbols:
            return self.builtin_symbols[name]
        elif self.outer is None:
            return None
        else:
            try_resolve = self.outer.resolve_symbol(name)
            # try to
            if try_resolve is not None and try_resolve.scope == Scope.LOCAL:
                return self.add_free_symbol(name)
            return try_resolve

    def generate_child(self):
        child = SymTable()
        child.outer = self
        return child
