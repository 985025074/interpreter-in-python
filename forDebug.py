from eval.eval import ycEval
from lexer.lexer import Lexer, TokenTypes
from parser.parser import Parser

if __name__ == '__main__':
    code = [[
        """
            let map = function(arr, f) {
            let iter = function(arr, accumulated) {
            if (len(arr) == 0) {
            accumulated
            } else {
            iter(rest(arr), push(accumulated, f(first(arr))));
            }
            };
            iter(arr, []);
            };
            let reduce = function(arr, initial, f) {
            let iter = function(arr, result) {
            if (len(arr) == 0) {
            result
            } else {
            iter(rest(arr), f(result, first(arr)));
            }
            };
            iter(arr, initial);
            };
            let sum = function(arr) {
            reduce(arr, 0, function(initial, el) { initial + el });
            };
             sum([1, 2, 3, 4, 5]);

        """, 10
    ]]

    for test_code, result in code:
        lexer = Lexer(test_code)
        parser = Parser(lexer)
        program = parser.parse_program()
        program.print_whole_program_nicely()
        print(ycEval(program).inspect())
