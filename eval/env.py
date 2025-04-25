from typing import Any, Dict, List, Optional

from parser.node import Identifier


class Environment:
    def __init__(self) -> None:
        self.variables: Dict[Identifier, Any] = {}
        self.outer_env: Optional[Environment] = None

    def has_key(self, key):
        return key in self.variables.keys()

    def has_key_recursive(self, key):
        cur_env = self
        while cur_env is not None:
            if key in cur_env.variables.keys():
                return True
            else:
                cur_env = cur_env.outer_env

    def set_var(self, key, value):
        self.variables[key] = value

    def set_var_recursive(self, key, value):
        if key in self.variables.keys():
            self.variables[key] = value
        else:
            if self.outer_env is not None:
                self.outer_env.set_var_recursive(key, value)

    def get_var_recursive(self, key):
        if key in self.variables.keys():
            return self.variables[key]
        else:
            if self.outer_env is not None:
                return self.outer_env.get_var(key)

    def get_var(self, key):
        return self.variables[key]

    def extended_with(self, paras: Dict[Identifier, Any]):
        new_env = Environment()
        new_env.variables = paras
        new_env.outer_env = self
        return new_env
