from enum import Enum
from utils import Token, TokenType, keywords, SymbolTable
import re


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


class DFA:
    current_state = STATE.INIT
    next = [
        # init
        (STATE.INIT, Token.DIGIT, STATE.DIGIT),
        (STATE.INIT, Token.LETTER, STATE.LETTER_DIGIT),
        (STATE.INIT, Token.EQUAL, STATE.EQUAL),
        (STATE.INIT, Token.SYMBOL, STATE.SYMBOL),
        (STATE.INIT, Token.SLASH, STATE.SLASH),
        (STATE.INIT, Token.BLANK, STATE.INIT),
        (STATE.INIT, Token.EOF, STATE.INIT),

        # digit
        (STATE.DIGIT, Token.DIGIT, STATE.DIGIT),
        (STATE.DIGIT, Token.DELIMITER, STATE.INIT),

        # id, keyword
        (STATE.LETTER_DIGIT, Token.LETTER_DIGIT, STATE.LETTER_DIGIT),
        (STATE.LETTER_DIGIT, Token.DELIMITER, STATE.INIT),

        # equal
        (STATE.EQUAL, Token.EQUAL, STATE.EQUAL_EQUAL),
        (STATE.EQUAL, Token.DELIMITER, STATE.INIT),

        # equal equal
        (STATE.EQUAL_EQUAL, Token.ANY, STATE.INIT),

        # symbol
        (STATE.SYMBOL, Token.ANY, STATE.INIT),

        # slash
        (STATE.SLASH, Token.STAR, STATE.SLASH_STAR),

        # slash star
        (STATE.SLASH_STAR, Token.STAR, STATE.STAR),
        (STATE.SLASH_STAR, Token.ANY, STATE.SLASH_STAR),

        # star
        (STATE.STAR, Token.STAR, STATE.STAR),
        (STATE.STAR, Token.SLASH, STATE.STAR_SLASH),

        # star slash
        (STATE.STAR_SLASH, Token.ANY, STATE.INIT)
    ]


dfa = DFA()
symbol_table = SymbolTable()
file = open('input.txt')
token_file = open('tokens.txt', 'w')
token_file.write("1\t")

lineno = 1
look_ahead = False
look_ahead_char = None
eof = False


def eval_token_type(token: str, state: STATE):
    if state == STATE.DIGIT:
        return TokenType.NUM.value, int(token)
    if state == STATE.LETTER_DIGIT:
        if token in keywords:
            return TokenType.KEYWORD.value, token
        else:
            symbol_table.add_id_if_not_exist(token)
            return TokenType.ID.value, token

    if state in [STATE.SYMBOL, STATE.EQUAL_EQUAL, STATE.EQUAL]:
        return TokenType.SYMBOL.value, token

    return False, False


def read_next_token():
    global lineno, look_ahead, look_ahead_char, eof
    token = ''

    while True:
        current_state = dfa.current_state
        next_states = [i for i in dfa.next if i[0] == current_state]

        if look_ahead:
            c = look_ahead_char
        else:
            c = file.read(1)

        next_state = current_state
        for state in next_states:
            if re.match(state[1].value, c):
                next_state = state[2]
                if next_state != STATE.INIT:
                    token += c
                else:
                    look_ahead = True
                    look_ahead_char = c
                break
        else:
            if re.match(Token.EOF.value, c):
                eof = True
            else:
                # todo: error handling
                print("Invalid data - shit compiler" + str(current_state) + str(next_state) + c)
            next_state = STATE.INIT

        token_type, token_identified = False, False
        if next_state == STATE.INIT:
            token_type, token_identified = eval_token_type(token, dfa.current_state)
            if not token_identified:
                token = ''

        if dfa.current_state == STATE.INIT:
            look_ahead = False
            if c == '\n':
                lineno += 1
                token_file.write("\n" + str(lineno) + "\t")

        dfa.current_state = next_state

        if token_identified:
            return token_type, token_identified


def get_next_token():
    global eof
    while True:
        token_type, token_identified = read_next_token()
        token_tuple = "(" + token_type + ", " + str(token_identified) + ")"
        print(token_tuple + " in line " + str(lineno))
        token_file.write(token_tuple + ' ')

        if eof:
            print("EOF")
            exit(0)
