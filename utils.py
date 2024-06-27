from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from code_generator import CodeGenerator

keywords = ['break', 'else', 'if', 'endif', 'int', 'for', 'return', 'void']


class Token(Enum):
    DIGIT = '[0-9]'
    LETTER = '[A-Za-z]'
    LETTER_DIGIT = '[A-Za-z0-9]'
    SYMBOL = r'[;:,\[\]\(\)\{\}\+\-\*<]'
    EQUAL = '='
    SLASH = '/'
    NOT_SLASH = '[^/]'
    STAR = r'\*'
    BLANK = r'[ \n\r\t\v\f]'
    DELIMITER = r'[ \n\r\t\v\f;:,\[\]\(\)\{\}\+\-\*<=/]'
    EOF = r'\Z'
    ANY = r'[.\d\D\s\S]'


class NonTerminal(Enum):
    Program = "PROGRAM"
    Declarationlist = "DECLARATIONLIST"
    Declaration = "DECLARATION"
    Declarationinitial = "DECLARATIONINITIAL"
    Declarationprime = "DECLARATIONPRIME"
    Vardeclarationprime = "VARDECLARATIONPRIME"
    Fundeclarationprime = "FUNDECLARATIONPRIME"
    Typespecifier = "TYPESPECIFIER"
    Params = "PARAMS"
    Paramlist = "PARAMLIST"
    Param = "PARAM"
    Paramprime = "PARAMPRIME"
    Compoundstmt = "COMPOUNDSTMT"
    Statementlist = "STATEMENTLIST"
    Statement = "STATEMENT"
    Expressionstmt = "EXPRESSIONSTMT"
    Selectionstmt = "SELECTIONSTMT"
    Elsestmt = "ELSESTMT"
    Iterationstmt = "ITERATIONSTMT"
    Returnstmt = "RETURNSTMT"
    Returnstmtprime = "RETURNSTMTPRIME"
    Expression = "EXPRESSION"
    B = "B"
    H = "H"
    Simpleexpressionzegond = "SIMPLEEXPRESSIONZEGOND"
    Simpleexpressionprime = "SIMPLEEXPRESSIONPRIME"
    C = "C"
    Relop = "RELOP"
    Additiveexpression = "ADDITIVEEXPRESSION"
    Additiveexpressionprime = "ADDITIVEEXPRESSIONPRIME"
    Additiveexpressionzegond = "ADDITIVEEXPRESSIONZEGOND"
    D = "D"
    Addop = "ADDOP"
    Term = "TERM"
    Termprime = "TERMPRIME"
    Termzegond = "TERMZEGOND"
    G = "G"
    Signedfactor = "SIGNEDFACTOR"
    Signedfactorprime = "SIGNEDFACTORPRIME"
    Signedfactorzegond = "SIGNEDFACTORZEGOND"
    Factor = "FACTOR"
    Varcallprime = "VARCALLPRIME"
    Varprime = "VARPRIME"
    Factorprime = "FACTORPRIME"
    Factorzegond = "FACTORZEGOND"
    Args = "ARGS"
    Arglist = "ARGLIST"
    Arglistprime = "ARGLISTPRIME"
    EPSILON = "EPSILON"


class Terminal(Enum):
    ID = "ID"
    SEMICOLON = ";"
    OPENBRACET = "["
    CLOSEBRACET = "]"
    NUM = "NUM"
    OPENPARENTHESIS = "("
    CLOSEPARENTHESIS = ")"
    VOID = "void"
    INT = "int"
    COMMA = ","
    OPENACOLAD = "{"
    CLOSEACOLAD = "}"
    BREAK = "break"
    IF = "if"
    ELSE = "else"
    ENDIF = "endif"
    FOR = "for"
    RETURN = "return"
    LESS = "<"
    DOUBLEEQUAL = "=="
    EQUAL = "="
    ADD = "+"
    SUB = "-"
    STAR = "*"
    DOLLAR = '$'


class ActionSymbol(Enum):
    PID = "pid"
    DECLAREID = "declare_id"
    INITZERO = "init_zero"
    PNUM = "pnum"
    RETURN = "return"
    BREAK = "break"
    IFSAVE = "if_save"
    STARTELSE = "start_else"
    IFSAVEEND = "if_save_end"
    ENDIF = "endif"
    ENDIFAFTERELSE = "endif_after_else"
    DECLAREFUNCTION = "declare_function"
    POPPARAM = "pop_param"
    OPENSCOPE = "open_scope"
    FUNCOPENSCOPEFLAG = "func_open_scope_flag"
    CLOSESCOP = "close_scope"
    RETURNVALUE = "return_value"
    ASSIGN = "assign"
    ARRAYINDEX = "array_index"
    EVALOPERATION = "eval_operation"
    POPERAND = "poperand"
    CALL = "call"
    START_ARGUMENT = "start_argument"
    ADD_ARGUMENT = "add_argument"
    END_ARGUMENT = "end_argument"


class TokenType(Enum):
    NUM = "NUM"
    ID = "ID"
    KEYWORD = "KEYWORD"
    SYMBOL = "SYMBOL"
    EOF = "$"


class SymbolTableItem:
    def __init__(self, lexeme: str, address=None, size=4):
        self.type = type
        self.lexeme = lexeme
        self.address = address
        self.size = size
        self.param_count = None
        self.param_symbols = []
        self.is_initialized = False
        self.is_function = False
        self.is_array = False


class SymbolTable(object):
    def __init__(self, code_generator: "CodeGenerator"):
        self.code_generator = code_generator
        self.scopes = [[]]

    def add_id_if_not_exist(self, lexeme):
        for item in self.scopes[-1]:
            if lexeme == item.lexeme:
                return
        self.scopes[-1].append(SymbolTableItem(lexeme=lexeme, address=self.code_generator.get_next_data_address()))

    def find_symbol_address(self, lexeme):
        return self.find_symbol(lexeme).address

    def find_symbol(self, lexeme):
        for scope in reversed(self.scopes):
            for symbol in scope:
                if symbol.lexeme == lexeme:
                    return symbol

    def find_symbol_by_address(self, address):
        for scope in reversed(self.scopes):
            for symbol in scope:
                if symbol.address == address:
                    return symbol

    def get_last_symbol(self):
        return self.scopes[-1][-1]

    def add_new_scope(self):
        self.scopes.append([])

    def close_scope(self):
        self.scopes.pop()

    def write(self):
        pass
        # with open('symbol_table.txt', 'w') as f:
        #     for item in self.items:
        #         f.write(f"{item.id}.\t{item.lexeme}\n")
        #     f.close()


class TokenDTO:
    def __init__(self, lineno=None, token_type=None, lexeme=None):
        self.lineno = lineno
        self.token_type = token_type
        self.lexeme = lexeme


def remove_node(node):
    node.parent.children = [child for child in node.parent.children if child != node]
    node.parent = None
