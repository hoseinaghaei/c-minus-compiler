from dataclasses import dataclass
from enum import Enum
from typing import Union, List

keywords = ['break', 'else', 'if', 'endif', 'int', 'for', 'return', 'void']


class Token(Enum):
    DIGIT = '[0-9]'
    LETTER = '[A-Za-z]'
    LETTER_DIGIT = '[A-Za-z0-9]'
    KEYWORD = '(if|else|void|int|for|break|return|endif)'
    SYMBOL = '[;:,\[\]\(\)\{\}\+\-\*<]'
    EQUAL = '='
    SLASH = '/'
    STAR = '\*'
    BLANK = r'[ \n\r\t\v\f]'
    DELIMITER = r'[ \n\r\t\v\f;:,\[\]\(\)\{\}\+\-\*<=(==)]'
    EOF = '\Z'
    ANY = '[.\d\D\s\S]'


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
                f.write(f"{item.id}\t{item.lexeme}\n")
            f.close()
