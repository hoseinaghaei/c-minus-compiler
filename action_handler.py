from typing import TYPE_CHECKING

from semantic_handler import SemanticHandler

if TYPE_CHECKING:
    from code_generator import CodeGenerator
from utils import SymbolTable, TokenDTO, SymbolTableItem


class ActionHandler:
    def __init__(self, code_generator: "CodeGenerator", symbol_table: SymbolTable, semantic_handler: SemanticHandler):
        self.code_generator = code_generator
        self.symbol_table = symbol_table
        self.semantic_handler = semantic_handler
        self.argument_counts = []
        self.current_function = None
        self.current_id = None
        self.current_type = None
        self.called_functions = []
        self.check_declaration_flag = False
        self.function_scope_has_opened = False
        self.breaks = []
        self.has_reached_main = False
        self.current_id = ""
        self.void_flag = False
        self.last_type = None

    def pid(self, previous_token: TokenDTO):
        self.current_id = previous_token.lexeme
        self.check_if_its_main(previous_token)
        symbol = self.symbol_table.find_symbol(previous_token.lexeme)
        if symbol is not None:
            self.code_generator.ss.append(symbol.address)
        else:
            self.semantic_handler.not_defined(previous_token.lexeme)
            self.code_generator.ss.append("#0")  # to avoid ss empty error

    def declare_id(self, previous_token: TokenDTO):
        self.current_id = previous_token.lexeme
        self.symbol_table.add_id_if_not_exist(lexeme=self.current_id)
        self.check_if_its_main(previous_token)

    def check_if_its_main(self, previous_token):
        if previous_token.lexeme == 'main':
            code = f"(JP, {self.code_generator.get_current_code_stack_head()}, , )"
            self.code_generator.add_main_address(code)
            if not self.has_reached_main:
                self._initialize_global_variable()
            self.has_reached_main = True

    def _initialize_global_variable(self):
        for symbol in self.code_generator.symbol_table.scopes[0]:
            if not symbol.is_function and symbol.lexeme != 'main':  # todo: fix
                self.code_generator.add_code(f"(ASSIGN, #0, {symbol.address}, )")
                # self.code_generator.add_code(f"(ASSIGN, #0, {symbol.address}, {symbol.lexeme})")

    def pnum(self, previous_token: TokenDTO):
        self.code_generator.ss.append(f"#{previous_token.lexeme}")

    def label(self, previous_token: TokenDTO):
        self.code_generator.ss.append(f"#{self.code_generator.i}")

    def save(self, previous_token: TokenDTO):
        self.code_generator.ss.append(f"#{self.code_generator.get_current_code_stack_head()}")
        self.code_generator.move_code_stack_head()

    def poperation(self, previous_token: TokenDTO):
        self.code_generator.ss.append(previous_token.token_type)

    def eval_operation(self, previous_token: TokenDTO):
        operand2 = self.code_generator.ss.pop()
        operation = self.code_generator.ss.pop()
        operand1 = self.code_generator.ss.pop()

        temp_address = self.code_generator.get_temp_address()
        self.code_generator.ss.append(temp_address)
        operation_to_func_name = {
            '+': 'ADD',
            '-': 'SUB',
            '<': 'LT',
            '==': 'EQ',
            '*': 'MULT',
        }
        code = f"({operation_to_func_name[operation]}, {operand1}, {operand2}, {temp_address})"
        self.code_generator.add_code(code)

    def start_else(self, previous_token: TokenDTO):
        code_stack_index = self.code_generator.ss.pop()
        condition = self.code_generator.ss.pop()
        i = self.code_generator.get_current_code_stack_head()
        code = f"(JPF, {condition}, {i + 1}, )"
        self.code_generator.add_code(code, code_stack_index)

        self.code_generator.ss.append(i)
        self.code_generator.move_code_stack_head()

    def endif_after_else(self, previous_token: TokenDTO):
        code = f"(JP, {self.code_generator.get_current_code_stack_head()}, , )"
        code_stack_index = self.code_generator.ss.pop()
        self.code_generator.add_code(code, code_stack_index)

    def endif(self, previous_token: TokenDTO):
        code_stack_index = self.code_generator.ss.pop()
        condition = self.code_generator.ss.pop()
        i = self.code_generator.get_current_code_stack_head()
        code = f"(JPF, {condition}, {i}, )"
        self.code_generator.add_code(code, code_stack_index)

    def assign(self, previous_token: TokenDTO):
        value = self.code_generator.ss.pop()
        address = self.code_generator.ss.pop()
        code = f"(ASSIGN, {value}, {address}, )"
        self.code_generator.add_code(code)
        self.code_generator.ss.append(value)
        symbol = self.code_generator.symbol_table.find_symbol_by_address(address)
        if symbol:
            symbol.is_initialized = True

        # type checking
        value_type = self.symbol_table.get_type_by_address(value)
        symbol_type = self.symbol_table.get_type_by_address(address)
        if value_type != symbol_type:
            self.semantic_handler.operand_type_mismatch(value_type, symbol_type)

    def declare_array(self, previous_token: TokenDTO):
        length = int(self.code_generator.ss.pop()[1:])
        symbol = self.code_generator.symbol_table.get_last_symbol()
        symbol.is_array = True
        size = length * 4
        array_start_address = self.code_generator.get_data_address(size=size)
        code = f"(ASSIGN, #{array_start_address}, {symbol.address}, )"
        self.code_generator.add_code(code)
        if len(self.code_generator.symbol_table.scopes) > 1:
            for address in range(array_start_address, array_start_address + size, 4):
                code = f"(ASSIGN, #0, {address}, )"
                self.code_generator.add_code(code)

    def array_index(self, previous_token: TokenDTO):
        offset = self.code_generator.ss.pop()
        temp = self.code_generator.get_temp_address()
        array_start = self.code_generator.ss.pop()
        self.code_generator.add_code(f"(MULT, {offset}, #4, {temp})")
        self.code_generator.add_code(f"(ADD, {temp}, {array_start}, {temp})")
        self.code_generator.ss.append(f"@{temp}")

    def pop(self, previous_token: TokenDTO):
        self.code_generator.ss.pop()

    def for_check_condition(self, previous_token: TokenDTO):
        self.code_generator.ss.append(f"#{self.code_generator.get_current_code_stack_head()}")

    def for_jump_check_condition(self, previous_token: TokenDTO):
        self.code_generator.add_code(f"(JP, {self.code_generator.ss[-5]}, , )")
        self.code_generator.add_code(f"(JP, {self.code_generator.get_current_code_stack_head()}, , )",
                                     self.code_generator.ss[-2])
        self.code_generator.add_code(f"(ASSIGN, #0, {self.code_generator.temp_ptr - 4}, )")

    def for_save(self, previous_token: TokenDTO):
        cond_result = self.code_generator.ss.pop()
        jp_index = self.code_generator.ss.pop()
        check_saved_index = self.code_generator.ss.pop()
        check_result = self.code_generator.ss.pop()
        check_statement_index = self.code_generator.ss.pop()
        check_statement_index = self.code_generator.ss.pop()

        jpf_code = f"(JPF, {check_result}, #{self.code_generator.get_current_code_stack_head() + 1}, )"
        self.code_generator.add_code(jpf_code, check_saved_index)

        add = str(jp_index)
        if add[0] == '#':
            add = int(add[1:])
        else:
            add = int(add)
        jp_code = f"(JP, {str(add + 1)}, , )"
        self.code_generator.add_code(jp_code)

    def break_scope(self, previous_token: TokenDTO):
        self.breaks.append([])

    def break_key(self, previous_token: TokenDTO):
        if len(self.breaks) > 0:
            self.breaks[-1].append(self.code_generator.get_current_code_stack_head())
            self.code_generator.move_code_stack_head()
        else:
            self.semantic_handler.illegal_break()

    def break_save(self, previous_token: TokenDTO):
        for i in self.breaks[-1]:
            self.code_generator.add_code(f"(JP, {self.code_generator.get_current_code_stack_head()}, , )", i)
        self.breaks.pop()

    def debug(self, previous_token: TokenDTO):
        print(self.code_generator.get_current_code_stack_head())

    def check_declaration(self, previous_token: TokenDTO, ):
        self.check_declaration_flag = True

    def uncheck_declaration(self, previous_token: TokenDTO, ):
        self.check_declaration_flag = False

    def set_function_scope_flag(self, previous_token: TokenDTO):
        self.function_scope_has_opened = True

    def start_scope(self, previous_token: TokenDTO):
        if not self.function_scope_has_opened:
            self.code_generator.symbol_table.add_new_scope()
        self.function_scope_has_opened = False
        self.code_generator.ptr_stack.append(
            (self.code_generator.data_ptr, self.code_generator.temp_ptr))

    def end_scope(self, previous_token: TokenDTO):
        self.code_generator.symbol_table.close_scope()
        self.code_generator.data_ptr, self.code_generator.temp_ptr = self.code_generator.ptr_stack.pop()

    def add_param(self, previous_token: TokenDTO):
        self.current_id = previous_token.lexeme
        symbol = self.symbol_table.get_last_symbol()
        self.code_generator.call_stack.pop(symbol.address)
        self.current_function.param_symbols.append(symbol)
        symbol.is_initialized = True
        self.current_function.param_count += 1

    def declare_function(self, previous_token: TokenDTO):
        func_declared: SymbolTableItem = self.code_generator.symbol_table.get_last_symbol()
        func_declared.address = f"#{self.code_generator.get_current_code_stack_head()}"
        func_declared.is_function = True
        func_declared.param_count = 0
        self.current_function = func_declared
        self.code_generator.function_data_ptr = self.code_generator.data_ptr
        self.code_generator.function_temp_ptr = self.code_generator.temp_ptr

    def call(self, previous_token: TokenDTO):
        self.store_data_and_temp()
        self.code_generator.machine_state.save_machine_state()

        arg_count = self.argument_counts.pop()
        self.code_generator.machine_state.save_return_address(arg_count)

        self.make_call(arg_count)

        self.code_generator.machine_state.restore_machine_state()
        self.restore_data_and_temp()

        self.retrieve_return_value()

    def retrieve_return_value(self):
        temp = self.code_generator.get_temp_address()
        self.code_generator.ss.append(temp)
        code = f"(ASSIGN, {self.code_generator.machine_state.return_value_ptr}, {temp}, )"
        self.code_generator.add_code(code)

    def restore_data_and_temp(self):
        for address in range(self.code_generator.temp_ptr, self.code_generator.function_temp_ptr, -4):
            self.code_generator.call_stack.pop(address - 4)
        for address in range(self.code_generator.data_ptr, self.code_generator.function_data_ptr, -4):
            symbol = self.code_generator.symbol_table.find_symbol_by_address(address - 4)
            if symbol and symbol.is_initialized:
                self.code_generator.call_stack.pop(address - 4)

    def make_call(self, arg_count):
        arg_types = []
        for i in range(arg_count):
            data = self.code_generator.ss.pop()
            self.code_generator.call_stack.push(data)
            arg_types.append(self.symbol_table.get_type_by_address(data))
        function_address = self.code_generator.ss.pop()
        code = f"(JP, {function_address}, , )"
        self.code_generator.add_code(code)

        # type checking
        arg_types.reverse()
        function_symbol = self.symbol_table.find_symbol_by_address(function_address)
        param_types = [param.get_type() for param in function_symbol.param_symbols]
        for i in range(arg_count):
            if arg_types[i] != param_types[i]:
                self.semantic_handler.arg_type_mismatch(param_types[i], arg_types[i], i, function_symbol.lexeme)


    def store_data_and_temp(self):
        for address in range(self.code_generator.function_data_ptr, self.code_generator.data_ptr, 4):
            symbol = self.code_generator.symbol_table.find_symbol_by_address(address)
            if symbol and symbol.is_initialized:
                self.code_generator.call_stack.push(address)
        for address in range(self.code_generator.function_temp_ptr, self.code_generator.temp_ptr, 4):
            self.code_generator.call_stack.push(address)

    def set_return_value(self, previous_token: TokenDTO):
        value = self.code_generator.ss.pop()
        self.code_generator.machine_state.save_return_value(value)

    def return_back(self, previous_token: TokenDTO):
        if not self.has_reached_main:
            code = f"(JP, @{self.code_generator.machine_state.return_address_ptr}, , )"
            self.code_generator.add_code(code)

    def start_args(self, previous_token: TokenDTO):
        self.argument_counts.append(0)
        self.called_functions.append(self.current_id)

    def add_arg(self, previous_token: TokenDTO):
        self.argument_counts[-1] += 1

    def end_args(self, previous_token: TokenDTO):
        function_name = self.called_functions.pop()
        arg_count = self.argument_counts[-1]
        function = self.symbol_table.find_symbol(function_name)
        if function:
            param_count = function.param_count
            self.argument_counts[-1] = param_count
            if param_count != arg_count:
                self.semantic_handler.arg_num_mismatch(function.lexeme)
                if param_count > arg_count:
                    for _ in range(param_count - arg_count):
                        self.code_generator.ss.append("#0")
                else:
                    for _ in range(arg_count - param_count):
                        self.code_generator.ss.pop()

    def init_zero(self, previous_token: TokenDTO):
        if len(self.code_generator.symbol_table.scopes) > 1:
            symbol = self.code_generator.symbol_table.get_last_symbol()
            code = f"(ASSIGN, #0, {symbol.address}, )"
            self.code_generator.add_code(code)

    def array_param(self, previous_token: TokenDTO):
        symbol = self.code_generator.symbol_table.get_last_symbol()
        symbol.is_array = True

    def void_check(self, previous_token: TokenDTO, ):
        self.void_flag = True

    def save_type(self, previous_token: TokenDTO, ):
        self.current_type = previous_token.lexeme

    def negate(self, previous_token: TokenDTO):
        operand = self.code_generator.ss.pop()
        temp = self.code_generator.get_temp_address()
        self.code_generator.ss.append(temp)
        code = f"(SUB, #0, {operand}, {temp})"
        self.code_generator.add_code(code)

    def check_void(self, previous_token: TokenDTO):
        var = self.symbol_table.get_last_symbol()
        if self.last_type == 'void':
            self.semantic_handler.illegal_void(var.lexeme)

    def set_type(self, previous_token: TokenDTO):
        self.last_type = previous_token.token_type

