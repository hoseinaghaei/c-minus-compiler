from dataclasses import dataclass
from enum import Enum

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

class TokenType(Enum):
    NUM = "NUM"
    ID = "ID"
    KEYWORD = "KEYWORD"
    SYMBOL = "SYMBOL"


@dataclass
class SymbolTableItem:
    id: int
    lexeme: str


class SymbolTable(object):
    def __init__(self):
        self.items = []
        self.ids = set()
        self._initialize()

    def _initialize(self):
        for i, keyword in enumerate(keywords):
            self.items.append(SymbolTableItem(id=i + 1, lexeme=keyword))

    def add_id_if_not_exist(self, lexeme):
        if lexeme not in self.ids:
            self.ids.add(lexeme)
            self.items.append(SymbolTableItem(id=len(self.items) + 1, lexeme=lexeme))

    def write(self):
        with open('symbol_table.txt', 'w') as f:
            for item in self.items:
                f.write(f"{item.id}.\t{item.lexeme}\n")
            f.close()
