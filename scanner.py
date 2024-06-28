from enum import Enum
from utils import Token, TokenType, keywords, SymbolTable
import re


class STATE(Enum):
    INIT = 0
    DIGIT = 1
    LETTER_DIGIT = 2
    EQUAL = 3
    EQUAL_EQUAL = 4
    SYMBOL = 5
    SLASH = 6
    SLASH_STAR = 7
    COMMENT_ENDING_STAR = 8
    STAR_SLASH = 9
    STAR = 10


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

        # id, keyword
        (STATE.LETTER_DIGIT, Token.LETTER_DIGIT, STATE.LETTER_DIGIT),
        (STATE.LETTER_DIGIT, Token.DELIMITER, STATE.INIT),

        # equal
        (STATE.EQUAL, Token.EQUAL, STATE.EQUAL_EQUAL),
        (STATE.EQUAL, Token.ANY, STATE.INIT),

        # equal equal
        (STATE.EQUAL_EQUAL, Token.ANY, STATE.INIT),

        # star
        (STATE.STAR, Token.SLASH, STATE.STAR_SLASH),
        (STATE.STAR, Token.ANY, STATE.INIT),

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


class Scanner(object):
    def __init__(self, symbol_table: SymbolTable,  input_file='input.txt'):
        self.input_file = input_file
        self.file = open(input_file, 'r')
        self.dfa = DFA()
        self.symbol_table = symbol_table
        self.token_file = open('tokens.txt', 'w')
        self.lexical_error_file = open('lexical_errors.txt', 'w')
        self.lineno = 1
        self.comment_start_line = 1
        self.comment = False
        self.first_token_of_line = True
        self.previous_token = None
        self.last_lexical_error_line = 0
        self.look_ahead = False
        self.look_ahead_char = None
        self.eof = False
        self.input_has_lexical_error = False

    @staticmethod
    def _eval_token_type(token: str, state: STATE):
        if state == STATE.DIGIT:
            return TokenType.NUM.value, int(token)
        if state == STATE.LETTER_DIGIT:
            if token in keywords:
                return TokenType.KEYWORD.value, token
            else:
                return TokenType.ID.value, token

        if state in [STATE.SYMBOL, STATE.EQUAL_EQUAL, STATE.EQUAL, STATE.STAR]:
            return TokenType.SYMBOL.value, token

        return False, None

    def _write_lexical_error(self, token, message, line):
        if line == self.last_lexical_error_line:
            self.lexical_error_file.write(f"({token}, {message}) ")
        else:
            if self.last_lexical_error_line != 0:
                self.lexical_error_file.write("\n")
            self.lexical_error_file.write(f"{str(line)}.\t({token}, {message}) ")

        self.input_has_lexical_error = True
        self.last_lexical_error_line = line

    def _read_next_token(self):
        token = ''

        while True:
            token_has_lexical_error = False
            current_state = self.dfa.current_state
            next_states = [i for i in self.dfa.next if i[0] == current_state]

            if self.look_ahead:
                c = self.look_ahead_char
            else:
                c = self.file.read(1)

            for state in next_states:
                if re.match(state[1].value, c):
                    next_state = state[2]
                    if next_state == STATE.STAR_SLASH and not self.comment:
                        self._write_lexical_error("*/", "Unmatched comment", self.lineno)

                    if next_state != STATE.INIT:
                        token += c
                    else:
                        self.look_ahead = True
                        self.look_ahead_char = c
                    break
            else:
                if re.match(Token.EOF.value, c):
                    self.eof = True
                    if self.dfa.current_state in [STATE.SLASH_STAR, STATE.COMMENT_ENDING_STAR]:
                        token_has_lexical_error = True
                        token += c
                        if len(token) > 7:
                            token = token[:7] + "..."
                        self._write_lexical_error(token, "Unclosed comment", self.comment_start_line)
                    else:
                        if self.dfa.current_state == STATE.SLASH:
                            self._write_lexical_error(Token.SLASH.value, "Invalid input", self.lineno)

                else:
                    token_has_lexical_error = True
                    token += c
                    error_message = "Invalid input"
                    if self.dfa.current_state == STATE.DIGIT:
                        error_message = "Invalid number"

                    self._write_lexical_error(token, error_message, self.lineno)
                    self.look_ahead = False
                    token = ''

                next_state = STATE.INIT

            token_type, token_identified = False, None
            if next_state == STATE.INIT and not token_has_lexical_error:
                token_type, token_identified = self._eval_token_type(token, self.dfa.current_state)
                if token_identified is None:
                    token = ''

            if self.dfa.current_state in [STATE.INIT, STATE.SLASH_STAR, STATE.COMMENT_ENDING_STAR]:
                self.look_ahead = False
                if c == '\n':
                    self.lineno += 1
                    self.first_token_of_line = True

            self.dfa.current_state = next_state
            if not self.comment and self.dfa.current_state == STATE.SLASH_STAR:
                self.comment = True
                self.comment_start_line = self.lineno

            if self.dfa.current_state not in [STATE.SLASH_STAR, STATE.COMMENT_ENDING_STAR]:
                self.comment = False

            if token_identified is not None:
                return token_type, token_identified
            if self.eof:
                return TokenType.EOF.value, TokenType.EOF.value

    def _write_new_line(self):
        line = ''
        if self.previous_token is not None:
            line = '\n'
        self.token_file.write(f"{line}{self.lineno}.\t")

    def get_next_token(self):
        token_type, token_identified = self._read_next_token()
        if token_type != TokenType.EOF.value:
            token_tuple = "(" + token_type + ", " + str(token_identified) + ")"
            if self.first_token_of_line:
                self._write_new_line()
                self.first_token_of_line = False
            self.token_file.write(token_tuple + ' ')
            self.previous_token = token_identified
        else:
            if not self.input_has_lexical_error:
                self.lexical_error_file.write("There is no lexical error.")
            self.token_file.close()
            self.lexical_error_file.close()
            self.file.close()

        if token_type in [TokenType.SYMBOL.value, TokenType.KEYWORD.value]:
            return token_identified, token_type
        else:
            return token_type, token_identified

        # ;, SYMBOL
        # if, KEYWORD
        # NUM, 3
        # ID, a
        # $, $
