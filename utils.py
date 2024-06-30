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
    DECLARE_ID = "declare_id"
    INIT_ZERO = "init_zero"
    PNUM = "pnum"
    RETURN = "return"
    BREAK = "break"
    BREAK_SCOPE = "break_scope"
    BREAK_SAVE = "save_break"
    IF_SAVE = "if_save"
    START_ELSE = "start_else"
    IF_SAVE_END = "if_save_end"
    ENDIF = "endif"
    ENDIF_AFTER_ELSE = "endif_after_else"
    DECLARE_FUNCTION = "declare_function"
    ADD_PARAM = "add_param"
    START_SCOPE = "start_scope"
    START_FUNC_SCOPE_FLAG = "start_scope_flag"
    END_SCOPE = "end_scope"
    RETURN_VALUE = "return_value"
    ASSIGN = "assign"
    ARRAY_INDEX = "array_index"
    EVAL_OPERATION = "eval_operation"
    POPERATION = "poperand"
    CALL = "call"
    START_ARGS = "start_argument"
    ADD_ARG = "add_argument"
    END_ARGS = "end_argument"
    POP = "pop"
    FOR_CHECK_CONDITION = "for_check_condition"
    FOR_JUMP_CHECK_CONDITION = "for_jump_check_condition"
    FOR_SAVE = "save_for"
    DEBUG = "debug"
    ARRAY_PARAM = "array_param"
    DECLARE_ARRAY = "declare_array"
    NEGATE = "negate"
    CHECK_VOID = "check_void"
    SET_TYPE = "set_type"


class TokenType(Enum):
    NUM = "NUM"
    ID = "ID"
    KEYWORD = "KEYWORD"
    SYMBOL = "SYMBOL"
    EOF = "$"


class SymbolTableItem:
    def __init__(self, lexeme: str, address=None, size=4):
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
        self.scopes[-1].append(SymbolTableItem(lexeme=lexeme, address=self.code_generator.get_data_address()))

    def find_symbol(self, lexeme):
        for scope in reversed(self.scopes):
            for symbol in scope:
                if symbol.lexeme == lexeme:
                    return symbol
        return None

    def find_symbol_by_address(self, address):
        for scope in reversed(self.scopes):
            for symbol in scope:
                if symbol.address == address:
                    return symbol

    def get_type_by_address(self, address):
        if type(address) == str and address[0] == '#':
            return 'int'
        symbol = self.find_symbol_by_address(address)
        if symbol is None:
            return 'int'
        if symbol.is_array:
            return 'array'
        return 'int'

    def get_last_symbol(self):
        return self.scopes[-1][-1]

    def add_new_scope(self):
        self.scopes.append([])

    def close_scope(self):
        self.scopes.pop()


class TokenDTO:
    def __init__(self, lineno=None, token_type=None, lexeme=None):
        self.lineno = lineno
        self.token_type = token_type
        self.lexeme = lexeme


def remove_node(node):
    node.parent.children = [child for child in node.parent.children if child != node]
    node.parent = None
