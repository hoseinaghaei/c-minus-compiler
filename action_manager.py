from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from code_generator import CodeGenerator
from utils import SymbolTable, TokenDTO, SymbolTableItem


class ActionManager:
    def __init__(self, code_generator: "CodeGenerator", symbol_table: SymbolTable):
        self.code_generator = code_generator
        self.symbol_table = symbol_table
        self.argument_counts = []
        self.current_declared_function_symbol_item = None
        self.current_id = None
        self.current_type = None
        self.called_functions = []
        self.no_push_flag = False
        self.check_declaration_flag = False
        self.function_scope_has_opened = False
        self.breaks = []
        self.has_reached_main = False
        self.current_id = ""
        self.void_flag = False

    def pid(self, previous_token: TokenDTO):
        self.current_id = previous_token.lexeme
        self.check_if_its_main(previous_token)
        if not self.no_push_flag:
            address = self.symbol_table.find_symbol_address(previous_token.lexeme)
            self.code_generator.ss.append(address)

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

    def push_operation(self, previous_token: TokenDTO):
        self.code_generator.ss.append(previous_token.token_type)

    def eval_operation(self, previous_token: TokenDTO):
        operand2 = self.code_generator.ss.pop()
        operation = self.code_generator.ss.pop()
        operand1 = self.code_generator.ss.pop()

        temp_address = self.code_generator.get_next_temp_address()
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

    def start_argument_list(self, previous_token: TokenDTO):
        self.argument_counts.append(0)
        self.called_functions.append(self.current_id)

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
        # code = f"(ASSIGN, {value}, {address}, {self.symbol_table.find_symbol_by_address(address).lexeme})"
        code = f"(ASSIGN, {value}, {address}, )"
        self.code_generator.add_code(code)
        self.code_generator.ss.append(value)  # todo: why?
        symbol = self.code_generator.symbol_table.find_symbol_by_address(address)
        if symbol:
            symbol.is_initialized = True

    # def declare_array(self, previous_token: TokenDTO,  ):
    #     # use [1:] to skip the '#'
    #     length = int(self.code_generator.ss.pop()[1:])
    #     symbol: Symbol = self.code_generator.symbol_table.scopes[-1][-1]
    #     symbol.is_array = True
    #     symbol.symbol_type = ARRAY
    #     size = length * WORD_SIZE
    #     array_start_address = self.code_generator.get_next_data_address(size=size)
    #     self.code_generator.push_instruction(Assign(f"#{array_start_address}", symbol.address))
    #     if len(self.code_generator.symbol_table.scopes) > 1:
    #         for address in range(array_start_address, array_start_address + size, WORD_SIZE):
    #             self.code_generator.push_instruction(
    #                 Assign("#0", address))

    # def array(self, previous_token: TokenDTO):
    #     offset = self.code_generator.ss.pop()
    #     temp = self.code_generator.get_next_temp_address()
    #     array_start = self.code_generator.ss.pop()
    #     instructions = [
    #         Mult(offset, f"#{WORD_SIZE}", temp),
    #         Add(temp, f"{array_start}", temp),
    #     ]
    #     self.code_generator.push_codes(instructions)
    #     self.code_generator.ss.append(f"@{temp}")
    #
    # def start_break_scope(self, previous_token: TokenDTO):
    #     self.breaks.append([])
    #
    # def add_break(self, previous_token: TokenDTO):
    #     self.breaks[-1].append(self.code_generator.i)
    #     self.code_generator.i += 1
    #
    # def handle_breaks(self, previous_token: TokenDTO):
    #     for destination in self.breaks[-1]:
    #         instruction = JP(f"#{self.code_generator.i}")
    #         self.code_generator.add_code(instruction, destination)
    #     self.breaks.pop()

    def pop(self, previous_token: TokenDTO):
        self.code_generator.ss.pop()

    def check_declaration(self, previous_token: TokenDTO, ):
        self.check_declaration_flag = True

    def uncheck_declaration(self, previous_token: TokenDTO, ):
        self.check_declaration_flag = False

    def set_function_scope_flag(self, previous_token: TokenDTO):
        self.function_scope_has_opened = True

    def open_scope(self, previous_token: TokenDTO):
        if not self.function_scope_has_opened:
            self.code_generator.symbol_table.add_new_scope()
        self.function_scope_has_opened = False
        self.code_generator.data_and_temp_stack.append(
            (self.code_generator.data_address, self.code_generator.temp_address))

    def close_scope(self, previous_token: TokenDTO):
        self.code_generator.symbol_table.close_scope()
        self.code_generator.data_address, self.code_generator.temp_address = self.code_generator.data_and_temp_stack.pop()

    def pop_param(self, previous_token: TokenDTO):
        address = self.code_generator.ss.pop()
        self.code_generator.runtime_stack.pop(address)
        symbol = self.code_generator.symbol_table.find_symbol_by_address(address)
        # symbol.symbol_type = self.current_type
        if previous_token and previous_token.lexeme == ']':
            # symbol.symbol_type = ARRAY
            symbol.is_array = True
        self.current_declared_function_symbol_item.param_symbols.append(symbol)
        if symbol:
            symbol.is_initialized = True
            self.current_declared_function_symbol_item.param_count += 1

    def declare_function(self, previous_token: TokenDTO):
        func_declaration_symbol_item: SymbolTableItem = self.code_generator.symbol_table.get_last_symbol()
        func_declaration_symbol_item.address = f"#{self.code_generator.get_current_code_stack_head()}"
        func_declaration_symbol_item.is_function = True
        # func_declaration_symbol_item.symbol_type = self.current_type
        func_declaration_symbol_item.param_count = 0
        self.current_declared_function_symbol_item = func_declaration_symbol_item
        # self.void_flag = False
        self.code_generator.function_data_start_pointer = self.code_generator.data_address
        self.code_generator.function_temp_start_pointer = self.code_generator.temp_address

    def call(self, previous_token: TokenDTO):
        self.store_data_and_temp()
        self.code_generator.register_file.push_registers()

        arg_count = self.argument_counts.pop()
        self.code_generator.register_file.save_return_address(arg_count)

        self.make_call(arg_count)

        self.code_generator.register_file.pop_registers()
        self.restore_data_and_temp()

        self.retrieve_return_value()

    def retrieve_return_value(self):
        temp = self.code_generator.get_next_temp_address()
        self.code_generator.ss.append(temp)
        code = f"(ASSIGN, {self.code_generator.register_file.return_value_register_address}, {temp}, )"
        self.code_generator.add_code(code)

    def restore_data_and_temp(self):
        for address in range(self.code_generator.temp_address, self.code_generator.function_temp_start_pointer, -4):
            self.code_generator.runtime_stack.pop(address - 4)
        for address in range(self.code_generator.data_address, self.code_generator.function_data_start_pointer, -4):
            symbol = self.code_generator.symbol_table.find_symbol_by_address(address - 4)
            if symbol and symbol.is_initialized:
                self.code_generator.runtime_stack.pop(address - 4)

    def make_call(self, arg_count):
        for i in range(arg_count):
            data = self.code_generator.ss.pop()
            self.code_generator.runtime_stack.push(data)
        address = self.code_generator.ss.pop()
        code = f"(JP, {address}, , )"
        self.code_generator.add_code(code)

    def store_data_and_temp(self):
        for address in range(self.code_generator.function_data_start_pointer, self.code_generator.data_address, 4):
            symbol = self.code_generator.symbol_table.find_symbol_by_address(address)
            if symbol and symbol.is_initialized:
                self.code_generator.runtime_stack.push(address)
        for address in range(self.code_generator.function_temp_start_pointer, self.code_generator.temp_address, 4):
            self.code_generator.runtime_stack.push(address)

    def set_return_value(self, previous_token: TokenDTO):
        value = self.code_generator.ss.pop()
        self.code_generator.register_file.save_return_value(value)

    def return_back(self, previous_token: TokenDTO):
        if not self.has_reached_main:
            code = f"(JP, @{self.code_generator.register_file.return_address_register_address}, , )"
            self.code_generator.add_code(code)

    def add_argument_count(self, previous_token: TokenDTO):
        self.argument_counts[-1] += 1

    def end_argument_count(self, previous_token: TokenDTO):
        pass
        # self.argument_counts[-1] += 1

    def init_zero(self, previous_token: TokenDTO):
        if len(self.code_generator.symbol_table.scopes) > 1:
            symbol = self.code_generator.symbol_table.scopes[-1][-1]
            # code = f"(ASSIGN, {symbol.address}, #0, {symbol.lexeme})"
            code = f"(ASSIGN, #0, {symbol.address}, )"
            self.code_generator.add_code(code)

    # def array_param(self, previous_token: TokenDTO,  ):
    #     symbol: Symbol = self.code_generator.symbol_table.scopes[-1][-1]
    #     symbol.is_array = True
    #     symbol.symbol_type = ARRAY


    def void_check(self, previous_token: TokenDTO, ):
        self.void_flag = True

    def save_type(self, previous_token: TokenDTO, ):
        self.current_type = previous_token.lexeme

    def pop(self, previous_token: TokenDTO):
        self.code_generator.ss.pop()
