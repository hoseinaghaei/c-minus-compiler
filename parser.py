from grammar import Grammar
from utils import NonTerminal, Terminal
from scanner import Scanner


class Parser(object):
    def __init__(self):
        self.grammar = Grammar()
        self.scanner = Scanner()
        self._next_token()
        self.syntax_error_file = open('syntax_errors.txt', 'w')
        self.input_has_syntax_error = False

    def _next_token(self):
        token, token_info = self.scanner.get_next_token()
        self.look_ahead = token
        # if token is symbol or keyword -> token_info = SYMBOL or KEYWORD else -> token_info = token lexeme
        self.look_ahead_info = token_info

    def _match(self, param):
        if param == self.look_ahead:
            self._next_token()
        else:
            self.input_has_syntax_error = True
            self.syntax_error_file.write(f"#{self.scanner.lineno} syntax error, missing {self.param}")

    def _do_parse(self, non_terminal: NonTerminal):
        next_rules = [i for i in self.grammar.next if i[0] == non_terminal][0][1]
        selected_rule = None
        is_look_ahead_in_follow = self.grammar.is_look_ahead_in_follow(non_terminal, self.look_ahead)
        for rule in next_rules:
            rhs_first = self.grammar.get_rhs_first(rule)
            if (self.look_ahead in rhs_first) or \
                    (NonTerminal.EPSILON.value in rhs_first and is_look_ahead_in_follow):
                selected_rule = rule
                break

        if selected_rule is not None:
            for token in selected_rule:
                if token == NonTerminal.EPSILON:
                    continue
                if isinstance(token, Terminal):
                    self._match(token.value)
                else:
                    self._do_parse(token)
        else:
            self.input_has_syntax_error = True
            if is_look_ahead_in_follow:
                self.syntax_error_file.write(f"#{self.scanner.lineno} syntax error, missing "
                                             f"{self.grammar.simplest_string[non_terminal]}")
            else:
                self.syntax_error_file.write(f"#{self.scanner.lineno} syntax error, illegal {self.look_ahead}")
                self._next_token()
                self._do_parse(non_terminal)

    def parse(self):
        self._do_parse(self.grammar.start_non_terminal)
        if not self.input_has_syntax_error:
            self.syntax_error_file.write('There is no syntax error.')

        self.syntax_error_file.close()
        pass
