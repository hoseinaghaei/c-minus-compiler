from enum import Enum
from collections import namedtuple
from enums import TokenType


class STATE(Enum):
    INIT = 0
    DIGIT = 1
    LETTER_DIGIT = 3
    EQUAL = 5
    EQUAL_EQUAL = 6
    SYMBOL = 8
    SLASH = 9
    SLASH_STAR = 10
    STAR = 11
    STAR_SLASH = 12
    # BLANK = 15


class DFA:
    current_state = STATE.INIT
    next = [
        # init
        (STATE.INIT, TokenType.DIGIT, STATE.DIGIT),
        (STATE.INIT, TokenType.LETTER, STATE.LETTER_DIGIT),
        (STATE.INIT, TokenType.EQUAL, STATE.EQUAL),
        (STATE.INIT, TokenType.SYMBOL, STATE.SYMBOL),
        (STATE.INIT, TokenType.SLASH, STATE.SLASH),
        (STATE.INIT, TokenType.BLANK, STATE.INIT),

        # digit
        (STATE.DIGIT, TokenType.DIGIT, STATE.DIGIT),
        (STATE.DIGIT, TokenType.DELIMITER, STATE.INIT),

        # id, keyword
        (STATE.LETTER_DIGIT, TokenType.LETTER_DIGIT, STATE.LETTER_DIGIT),
        (STATE.LETTER_DIGIT, TokenType.DIGIT, STATE.INIT),

        # equal
        (STATE.EQUAL, TokenType.EQUAL, STATE.EQUAL_EQUAL),
        (STATE.EQUAL, TokenType.DELIMITER, STATE.INIT),

        # equal equal
        (STATE.EQUAL_EQUAL, TokenType.ANY, STATE.INIT),

        # symbol
        (STATE.SYMBOL, TokenType.ANY, STATE.INIT),

        # slash
        (STATE.SLASH, TokenType.STAR, STATE.SLASH_STAR),

        # slash star
        (STATE.SLASH_STAR, TokenType.STAR, STATE.STAR),
        (STATE.SLASH_STAR, TokenType.ANY, STATE.SLASH_STAR),

        # star
        (STATE.STAR, TokenType.STAR, STATE.STAR),
        (STATE.STAR, TokenType.STAR, STATE.STAR_SLASH),

        # star slash
        (STATE.STAR, TokenType.STAR, STATE.INIT)
    ]


dfa = DFA()
lineno = 0
file = open('input.txt')
buffer = ''

import re


def read_next_token():
    print("start")
    while 1:
        c = file.read(1)
        print("\n\n")
        print(c)
        if re.match(TokenType.DIGIT.value, c):
            print("digit")

        if re.match(TokenType.LETTER.value, c):
            print("letter")

        if re.match(TokenType.LETTER.value, c):
            print("letter digit")
        if re.match(TokenType.SYMBOL.value, c):
            print("symbol")

        if re.match(TokenType.EQUAL.value, c):
            print("equal")

        if re.match(TokenType.SLASH.value, c):
            print("slash")

        if re.match(TokenType.STAR.value, c):
            print("star")

        if re.match(TokenType.BLANK.value, c):
            print("blank")

        if re.match(TokenType.DELIMITER.value, c):
            print("delimiter")

        if re.match(TokenType.EOF.value, c):
            print("end of file")

        if re.match(TokenType.ANY.value, c):
            print("Any")

        if c == '':
            print("done reading")
            exit(0)


def get_next_token():
    read_next_token()
