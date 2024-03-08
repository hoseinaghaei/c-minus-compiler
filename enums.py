from enum import Enum


class TokenType(Enum):
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
    ANY = '.'

