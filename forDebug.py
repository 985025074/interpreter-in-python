from eval import env
from eval.eval import ycEval
from eval.macro import expand_macro, handle_macro
from lexer.lexer import Lexer, TokenTypes
from parser.parser import Parser

if __name__ == '__main__':
    code = [[
        """
           let unless = macro(condition, consequence, alternative) {
             quote(if (!(unquote(condition))) {
            unquote(consequence);
            } else {
            unquote(alternative);
            });
            };
            unless(10 > 5, print("not greater"), print("greater"));

        """, 10
    ]]

    for test_code, result in code:
        env = env.Environment()
        lexer = Lexer(test_code)
        parser = Parser(lexer)
        program = parser.parse_program()
        handle_macro(program, env)
        program = expand_macro(program, env)
        result = ycEval(program, env)
        print(result)
