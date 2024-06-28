from anytree import Node, RenderTree

import utils
from code_generator import CodeGenerator
from grammar import Grammar
from utils import NonTerminal, Terminal, TokenType
from scanner import Scanner


class Parser(object):
    def __init__(self, code_generator: CodeGenerator, file='input.txt'):
        self.grammar = Grammar()
        self.code_generator = code_generator
        self.scanner = Scanner(self.code_generator.symbol_table)
        self.look_ahead = None
        self.previous_token = None
        self.current_token = None
        self._next_token()
        self.syntax_error_file = open('syntax_errors.txt', 'w')
        self.parse_tree_file = open('parse_tree.txt', 'w', encoding="utf-8")
        self.input_has_syntax_error = False
        self.current_non_terminal = self.grammar.statr_non_terminal
        self.root = Node(self.grammar.get_non_terminal_display_name(self.current_non_terminal))
        self.current_node = self.root
        self.end_of_file_ok = True

    def _next_token(self):
        if self.look_ahead == Terminal.DOLLAR.value:
            if self.current_non_terminal != NonTerminal.Program:
                self.syntax_error_file.write(f"#{self.scanner.lineno} : syntax error, Unexpected EOF")
                utils.remove_node(self.current_node)
                self.end_of_file_ok = False
            self._exit()
        self.previous_token = self.current_token
        token, token_type = self.scanner.get_next_token()
        self.look_ahead = token
        self.look_ahead_type = token_type
        self.current_token = utils.TokenDTO(token_type=token, lexeme=token_type)

    def _exit(self):
        if not self.input_has_syntax_error:
            self.syntax_error_file.write('There is no syntax error.')

        if self.end_of_file_ok:
            Node('$', parent=self.current_node)

        for pre, fill, node in RenderTree(self.root):
            print("%s%s" % (pre, node.name), file=self.parse_tree_file)

        self.syntax_error_file.close()
        self.parse_tree_file.close()
        exit(0)

    def get_terminal_pair_to_show(self) -> str:
        if self.look_ahead == Terminal.DOLLAR.value:
            return self.look_ahead

        if self.look_ahead in [TokenType.ID.value, TokenType.NUM.value]:
            return f"({self.look_ahead}, {self.look_ahead_type})"
        else:
            return f"({self.look_ahead_type}, {self.look_ahead})"

    def _match(self, param):
        node = Node(self.get_terminal_pair_to_show(), parent=self.current_node)
        if param == self.look_ahead:
            self._next_token()
        else:
            self.input_has_syntax_error = True
            self.syntax_error_file.write(f"#{self.scanner.lineno} : syntax error, missing {param}\n")
            utils.remove_node(node)

    def _do_parse(self, non_terminal: NonTerminal):
        self.current_non_terminal = non_terminal
        next_rules = [i for i in self.grammar.next if i[1] == non_terminal][0][2]
        selected_rule = None
        for rule in next_rules:
            if self.look_ahead in self.grammar.get_rhs_first(rule):
                selected_rule = rule
                break

        if selected_rule is None and self.grammar.is_look_ahead_in_follow(non_terminal, self.look_ahead):
            for rule in next_rules:
                if NonTerminal.EPSILON in rule:
                    continue
                if NonTerminal.EPSILON.value in self.grammar.get_rhs_first(rule):
                    selected_rule = rule
                    break

        if selected_rule is not None:
            for token in selected_rule:
                if isinstance(token, Terminal):
                    self._match(token.value)
                elif isinstance(token, utils.ActionSymbol):
                    self.code_generator.handle_action_symbol(token, self.previous_token)
                else:
                    current_node = self.current_node
                    self.current_node = Node(self.grammar.get_non_terminal_display_name(token), parent=current_node)
                    self._do_parse(token)
                    self.current_node = current_node
        else:
            is_look_ahead_in_follow = self.grammar.is_look_ahead_in_follow(non_terminal, self.look_ahead)
            if self.grammar.is_epsilon_in_first(non_terminal) and is_look_ahead_in_follow:
                Node('epsilon', parent=self.current_node)
                return

            self.input_has_syntax_error = True
            if is_look_ahead_in_follow:
                non_terminal_name = self.grammar.get_non_terminal_display_name(non_terminal)
                self.syntax_error_file.write(f"#{self.scanner.lineno} : syntax error, missing {non_terminal_name}\n")
                utils.remove_node(self.current_node)
                return
            else:
                if self.look_ahead != Terminal.DOLLAR.value:
                    self.syntax_error_file.write(f"#{self.scanner.lineno} : syntax error, illegal {self.look_ahead}\n")
                self._next_token()
                self._do_parse(non_terminal)

    def parse(self):
        self._do_parse(self.grammar.statr_non_terminal)
        self.code_generator.generate_output()
        self._exit()
