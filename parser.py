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
        token, token_type = self.scanner.get_next_token()
        self.look_ahead = token
        self.look_ahead_type = token_type


    def _match(self, param):
        if param == self.look_ahead:
            self._next_token()
        else:
            self.input_has_syntax_error = True
            # todo: error ‘missing b on line N'
            pass

    def _do_parse(self, non_terminal: NonTerminal):
        next_rules = [i for i in self.grammar.next if i[0] == non_terminal][0][1]
        selected_rule = None
        for rule in next_rules:
            if self.look_ahead in self.grammar.get_rhs_first(rule):
                selected_rule = rule
                break

        if selected_rule is not None:
            for token in selected_rule:
                if isinstance(token, Terminal):
                    self._match(token.value)
                else:
                    self._do_parse(token)
        else:
            is_look_ahead_in_follow = self.grammar.is_look_ahead_in_follow(non_terminal, self.look_ahead)
            if self.grammar.is_epsilon_in_first(non_terminal) and is_look_ahead_in_follow:
                return

            self.input_has_syntax_error = True
            if is_look_ahead_in_follow:
                # todo: error ‘missing A1 on line N’
                return
            else:
                self.syntax_error_file.write(f"#{self.scanner.lineno} syntax error, illegal {self.look_ahead}")
                self._next_token()
                self._do_parse(non_terminal)

    def parse(self):
        self._do_parse(self.grammar.statr_non_terminal)
        if not self.input_has_syntax_error:
            self.syntax_error_file.write('There is no syntax error.')

        self.syntax_error_file.close()
        pass
