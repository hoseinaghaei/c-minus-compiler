from code_generator import CodeGenerator
from semantic_handler import SemanticErrorHandler
from utils import TokenDTO, ActionSymbol


class SemanticAnalyzer(object):
    def __init__(self, code_generator: CodeGenerator):
        self.code_generator = code_generator
        self.semantic_error_handler = SemanticErrorHandler()

        self.action_symbol_mapper = {
            ActionSymbol.PID: self.pid,
            ActionSymbol.EVAL_OPERATION: self.eval_operation,
            ActionSymbol.CALL: self.call,
            ActionSymbol.ASSIGN: self.assign,
            ActionSymbol.END_ARGS: self.end_args,
            ActionSymbol.BREAK: self.break_key,
            ActionSymbol.CHECK_VOID: self.check_void,
        }

    def handle_action_symbol(self, action_symbol: ActionSymbol, previous_token: TokenDTO):
        if action_symbol in self.action_symbol_mapper:
            self.action_symbol_mapper[action_symbol](previous_token)

    def pid(self, previous_token: TokenDTO):
        symbol = self.code_generator.symbol_table.find_symbol(previous_token.lexeme)
        if symbol is None:
            self.semantic_error_handler.not_defined(previous_token.lexeme)
            self.code_generator.ss.append("0")  # to avoid ss empty error

    def eval_operation(self, previous_token: TokenDTO):
        operand2 = self.code_generator.ss[-1]
        operand1 = self.code_generator.ss[-3]
        # type checking
        operand1_type = self.code_generator.symbol_table.get_type_by_address(operand1)
        operand2_type = self.code_generator.symbol_table.get_type_by_address(operand2)
        if operand1_type != operand2_type:
            self.semantic_error_handler.operand_type_mismatch(operand2_type, operand1_type)

    def assign(self, previous_token: TokenDTO):
        value = self.code_generator.ss[-1]
        address = self.code_generator.ss[-2]
        # type checking
        value_type = self.code_generator.symbol_table.get_type_by_address(value)
        symbol_type = self.code_generator.symbol_table.get_type_by_address(address)
        if value_type != symbol_type:
            self.semantic_error_handler.operand_type_mismatch(value_type, symbol_type)

    def break_key(self, previous_token: TokenDTO):
        if len(self.code_generator.action_handler.breaks) == 0:
            self.semantic_error_handler.illegal_break()

    def call(self, previous_token: TokenDTO):
        arg_count = self.code_generator.action_handler.argument_counts[-1]
        arg_types = []
        for i in range(-arg_count, 0):
            arg_address = self.code_generator.ss[i]
            arg_types.append(self.code_generator.symbol_table.get_type_by_address(arg_address))
        function_address = self.code_generator.ss[-arg_count - 1]
        # type checking
        function_symbol = self.code_generator.symbol_table.find_symbol_by_address(function_address)
        param_types = [param.get_type() for param in function_symbol.param_symbols]
        for i in range(arg_count):
            if arg_types[i] != param_types[i]:
                self.semantic_error_handler.arg_type_mismatch(param_types[i], arg_types[i], i, function_symbol.lexeme)

    def end_args(self, previous_token: TokenDTO):
        function_name = self.code_generator.action_handler.called_functions.pop()
        arg_count = self.code_generator.action_handler.argument_counts[-1]
        function = self.code_generator.symbol_table.find_symbol(function_name)
        if function:
            param_count = function.param_count
            self.code_generator.action_handler.argument_counts[-1] = param_count
            if param_count != arg_count:
                self.semantic_error_handler.arg_num_mismatch(function.lexeme)
                if param_count > arg_count:
                    for _ in range(param_count - arg_count):
                        self.code_generator.ss.append("#0")
                else:
                    for _ in range(arg_count - param_count):
                        self.code_generator.ss.pop()

    def check_void(self, previous_token: TokenDTO):
        var = self.code_generator.symbol_table.get_last_symbol()
        if self.code_generator.action_handler.last_type == 'void':
            self.semantic_error_handler.illegal_void(var.lexeme)
