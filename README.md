# C-mnius Compiler

**a Python3 based one-pass compiler for a very simplified C-minus**

## Token Types and Grammar

The tokens in the below table can be recognized by the compiler:
**Token Type** | **Description**
:-------------:|:--------------:
NUM | Any string matching [0-9]+
ID | Any string matching: [A-Za-z][A-Za-z0-9]*
KEYWORD | if, endif, else, void, int, for, break, return
SYMBOL | ; : , [ ] ( ) { } + - * = < ==
COMMENT | Any string between a /* and a */ OR any string after a // and before a \n or EOF
WHITESPACE | blank (ASCII 32), \n (ASCII 10), \r (ASCII 13), \t (ASCII 9), \v (ASCII 11), \f (ASCII 12)

The grammar that this compiler uses is in [grammar.txt](https://github.com/hoseinaghaei/c-minus-compiler/blob/master/grammar/grammar.txt).

You can also find the modified version of the grammar after adding action symbols (starting with #) in [grammar_action_symbols.txt](https://github.com/hoseinaghaei/c-minus-compiler/blob/master/grammar/grammar_action_symbols.txt).

## First Phase : Scanner
Scanner is the part of the compiler that reads the input file character by character and recognizes tokens.
In this project, the preassumption is that a file called "input.txt" contains the code and is in the same directory as [compiler.py](https://github.com/hoseinaghaei/c-minus-compiler/blob/master/compiler.py). 

We use a predefined DFA to traverse and find tokens and errors.

You can also see this [branch](https://github.com/hoseinaghaei/c-minus-compiler/tree/phase01-scanner) for more data and dedicated test cases.
## Second Phase : Parser
Parser is the part of the compiler that recognizes the grammar used by the input.
This project implements a Predictive Recursive Descent parser. Additional information and how to use can be viewed in [README of Parser](https://github.com/hoseinaghaei/c-minus-compiler/blob/master/parser/README.md).

## Test
You can run the file [test.sh](https://github.com/hoseinaghaei/c-minus-compiler/blob/master/test.sh). It goes through Testcases folder and run all tests starting with T. You can also run test by yourself; Just create file `input.txt` in the root of the project and then run `compiler.py`.

It will generate files like `output.txt` which is intermediate codes, `lexical_error.txt` containing any lexical errors, `syntax_eror.txt` containing any syntax error found by parser, `parse_tree.txt` which is the output of parser etc.