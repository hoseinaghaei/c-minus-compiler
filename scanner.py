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
    COMMENT_ENDING_STAR = 11
    STAR_SLASH = 12
    STAR = 13


class DFA:
    current_state = STATE.INIT
    next = [
        # init
        (STATE.INIT, Token.DIGIT, STATE.DIGIT),
        (STATE.INIT, Token.LETTER, STATE.LETTER_DIGIT),
        (STATE.INIT, Token.EQUAL, STATE.EQUAL),
        (STATE.INIT, Token.STAR, STATE.STAR),
        (STATE.INIT, Token.SYMBOL, STATE.SYMBOL),
        (STATE.INIT, Token.SLASH, STATE.SLASH),
        (STATE.INIT, Token.BLANK, STATE.INIT),

        # digit
        (STATE.DIGIT, Token.DIGIT, STATE.DIGIT),
        (STATE.DIGIT, Token.DELIMITER, STATE.INIT),
        # (STATE.DIGIT, Token.INVALID, STATE.INIT),

        # id, keyword
        (STATE.LETTER_DIGIT, Token.LETTER_DIGIT, STATE.LETTER_DIGIT),
        (STATE.LETTER_DIGIT, Token.DELIMITER, STATE.INIT),
        # (STATE.LETTER_DIGIT, Token.INVALID, STATE.INIT),

        # equal
        (STATE.EQUAL, Token.EQUAL, STATE.EQUAL_EQUAL),
        (STATE.EQUAL, Token.ANY, STATE.INIT),

        # equal equal
        (STATE.EQUAL_EQUAL, Token.ANY, STATE.INIT),

        # star
        (STATE.STAR, Token.SLASH, STATE.STAR_SLASH),
        (STATE.STAR, Token.DELIMITER, STATE.INIT),
        (STATE.STAR, Token.LETTER_DIGIT, STATE.INIT),

        # symbol
        (STATE.SYMBOL, Token.ANY, STATE.INIT),

        # slash
        (STATE.SLASH, Token.STAR, STATE.SLASH_STAR),

        # slash star
        (STATE.SLASH_STAR, Token.STAR, STATE.COMMENT_ENDING_STAR),
        (STATE.SLASH_STAR, Token.ANY, STATE.SLASH_STAR),

        # comment ending star
        (STATE.COMMENT_ENDING_STAR, Token.STAR, STATE.COMMENT_ENDING_STAR),
        (STATE.COMMENT_ENDING_STAR, Token.SLASH, STATE.STAR_SLASH),
        (STATE.COMMENT_ENDING_STAR, Token.ANY, STATE.SLASH_STAR),

        # star slash
        (STATE.STAR_SLASH, Token.ANY, STATE.INIT)
    ]


dfa = DFA()
symbol_table = SymbolTable()
file = open('input.txt')
token_file = open('tokens.txt', 'w')
lexical_error_file = open('lexical_errors.txt', 'w')

lineno = 1
first_token_of_line = True
previous_token = None
last_lexical_error_line = 0
look_ahead = False
look_ahead_char = None
eof = False
input_has_lexical_error = False


def eval_token_type(token: str, state: STATE):
    if state == STATE.DIGIT:
        return TokenType.NUM.value, int(token)
    if state == STATE.LETTER_DIGIT:
        if token in keywords:
            return TokenType.KEYWORD.value, token
        else:
            symbol_table.add_id_if_not_exist(token)
            return TokenType.ID.value, token

    if state in [STATE.SYMBOL, STATE.EQUAL_EQUAL, STATE.EQUAL, STATE.STAR]:
        return TokenType.SYMBOL.value, token

    return False, None


def read_next_token():
    global lineno, look_ahead, look_ahead_char, eof, input_has_lexical_error, first_token_of_line, last_lexical_error_line
    token = ''

    while True:
        token_has_lexical_error = False
        current_state = dfa.current_state
        next_states = [i for i in dfa.next if i[0] == current_state]

        if look_ahead:
            c = look_ahead_char
        else:
            c = file.read(1)

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
                if dfa.current_state in [STATE.SLASH, STATE.SLASH_STAR, STATE.COMMENT_ENDING_STAR]:
                    input_has_lexical_error = True
                    token_has_lexical_error = True
                    token += c
                    if len(token) > 7:
                        token = token[:7] + "..."
                    if lineno == last_lexical_error_line:
                        lexical_error_file.write("(" + token + ", " + "Unclosed comment" + ") ")
                    else:
                        if last_lexical_error_line != 0:
                            lexical_error_file.write("\n")
                        lexical_error_file.write(str(lineno) + ".\t" + "(" + token + ", " + "Unclosed comment" + ") ")
                        last_lexical_error_line = lineno
            else:
                input_has_lexical_error = True
                token_has_lexical_error = True
                token += c
                error_message = "Invalid input"
                if dfa.current_state == STATE.INIT:
                    error_message = "Invalid input"
                elif dfa.current_state == STATE.STAR and eof:
                    error_message = "Unmatched comment"
                elif dfa.current_state == STATE.DIGIT:
                    error_message = "Invalid number"

                if lineno == last_lexical_error_line:
                    lexical_error_file.write("(" + token + ", " + error_message + ") ")
                else:
                    if last_lexical_error_line != 0:
                        lexical_error_file.write("\n")
                    lexical_error_file.write(str(lineno) + ".\t" + "(" + token + ", " + error_message + ") ")
                    last_lexical_error_line = lineno

                look_ahead = False
                token = ''
            next_state = STATE.INIT

        token_type, token_identified = False, None
        if next_state == STATE.INIT and not token_has_lexical_error:
            token_type, token_identified = eval_token_type(token, dfa.current_state)
            if token_identified is None:
                token = ''

        if dfa.current_state == STATE.INIT:
            look_ahead = False
            if c == '\n':
                lineno += 1
                first_token_of_line = True

        dfa.current_state = next_state

        if token_identified is not None:
            return token_type, token_identified
        if eof:
            return 'eof', ''


def write_new_line():
    global lineno, previous_token
    line = ''
    if previous_token is not None:
        line = '\n'
    token_file.write(f"{line}{lineno}.\t")


def get_next_token():
    global eof, lineno, first_token_of_line, previous_token
    while True:
        token_type, token_identified = read_next_token()
        if token_type != 'eof':
            token_tuple = "(" + token_type + ", " + str(token_identified) + ")"
            if first_token_of_line:
                write_new_line()
                first_token_of_line = False
            token_file.write(token_tuple + ' ')
            previous_token = token_identified

        if eof:
            print("EOF")
            symbol_table.write()
            if not input_has_lexical_error:
                lexical_error_file.write("There is no lexical error.")
            token_file.close()
            lexical_error_file.close()
            file.close()
            exit(0)
