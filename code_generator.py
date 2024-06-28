from program import Program
from machine_state import MachineState
from action_handler import ActionHandler
from call_stack import CallStack
from utils import SymbolTable, ActionSymbol, TokenDTO


class CodeGenerator:
    def __init__(self):
        self.data_ptr = 5000
        self.temp_ptr = 10000
        self.function_data_ptr = 0
        self.function_temp_ptr = 0

        self.ss = []
        self.ptr_stack = []

        self.program = Program()
        self.symbol_table = SymbolTable(self)
        self.machine_state = MachineState(self)
        self.call_stack = CallStack(self, self.machine_state)
        self.action_handler = ActionHandler(self, self.symbol_table)

        self.machine_state.initialize_machine_state(self.get_temp_address())

        self.main_address = self.get_current_code_stack_head()
        self.move_code_stack_head()

        self.action_symbol_mapper = {
            ActionSymbol.PID: self.action_handler.pid,
            ActionSymbol.DECLARE_ID: self.action_handler.declare_id,
            ActionSymbol.INIT_ZERO: self.action_handler.init_zero,
            ActionSymbol.PNUM: self.action_handler.pnum,
            ActionSymbol.POPERATION: self.action_handler.poperation,
            ActionSymbol.EVAL_OPERATION: self.action_handler.eval_operation,
            ActionSymbol.IF_SAVE: self.action_handler.save,
            ActionSymbol.START_ELSE: self.action_handler.start_else,
            ActionSymbol.ENDIF: self.action_handler.endif,
            ActionSymbol.ENDIF_AFTER_ELSE: self.action_handler.endif_after_else,
            ActionSymbol.DECLARE_FUNCTION: self.action_handler.declare_function,
            ActionSymbol.START_SCOPE_FLAG: self.action_handler.set_function_scope_flag,
            ActionSymbol.ADD_PARAM: self.action_handler.add_param,
            ActionSymbol.START_SCOPE: self.action_handler.start_scope,
            ActionSymbol.END_SCOPE: self.action_handler.end_scope,
            ActionSymbol.CALL: self.action_handler.call,
            ActionSymbol.RETURN: self.action_handler.return_back,
            ActionSymbol.ASSIGN: self.action_handler.assign,
            ActionSymbol.START_ARGS: self.action_handler.start_args,
            ActionSymbol.ADD_ARG: self.action_handler.add_arg,
            ActionSymbol.END_ARGS: self.action_handler.end_args,
            ActionSymbol.RETURN_VALUE: self.action_handler.set_return_value,
            ActionSymbol.POP: self.action_handler.pop,
            ActionSymbol.DECLARE_ARRAY: self.action_handler.declare_array,
            ActionSymbol.ARRAY_PARAM: self.action_handler.array_param,
            ActionSymbol.ARRAY_INDEX: self.action_handler.array_index,
            ActionSymbol.FOR_CHECK_CONDITION: self.action_handler.for_check_condition,
            ActionSymbol.FOR_JUMP_CHECK_CONDITION: self.action_handler.for_jump_check_condition,
            ActionSymbol.FOR_SAVE: self.action_handler.for_save,
            ActionSymbol.BREAK: self.action_handler.break_key,
            ActionSymbol.BREAK_SCOPE: self.action_handler.break_scope,
            ActionSymbol.BREAK_SAVE: self.action_handler.break_save,
            ActionSymbol.DEBUG: self.action_handler.debug,
            ActionSymbol.NEGATE: self.action_handler.negate,
        }
        self.add_output_function()

    def handle_action_symbol(self, action_symbol: ActionSymbol, *args):
        self.action_symbol_mapper[action_symbol](*args)

    def add_code(self, code, address=None):
        if type(address) == str and address[0] == '#':
            address = int(address[1:])

        self.program.add_code(code, address)

    def move_code_stack_head(self):
        self.program.increase_size(self.program.get_code_stack_head())

    def get_current_code_stack_head(self):
        return self.program.get_code_stack_head()

    def add_main_address(self, code: str):
        self.program.add_code(code, self.main_address)

    def get_data_address(self, size=4):
        address = self.data_ptr
        self.data_ptr += size
        return address

    def get_temp_address(self):
        address = self.temp_ptr
        self.temp_ptr += 4
        return address

    def add_output_function(self):
        self.symbol_table.add_id_if_not_exist('output')
        self.handle_action_symbol(ActionSymbol.PID, TokenDTO(lexeme='output'))
        self.handle_action_symbol(ActionSymbol.DECLARE_FUNCTION, None)
        self.handle_action_symbol(ActionSymbol.START_SCOPE, None)
        self.handle_action_symbol(ActionSymbol.START_SCOPE_FLAG, None)
        self.symbol_table.add_id_if_not_exist('a')
        self.handle_action_symbol(ActionSymbol.PID, TokenDTO(lexeme="a"))
        self.handle_action_symbol(ActionSymbol.ADD_PARAM, None)
        self.handle_action_symbol(ActionSymbol.PID, TokenDTO(lexeme="a"))
        self.handle_action_symbol(ActionSymbol.START_SCOPE, None)
        self.add_code(f"(PRINT, {self.ss.pop()}, , )")
        self.handle_action_symbol(ActionSymbol.END_SCOPE, None)
        self.handle_action_symbol(ActionSymbol.RETURN, None)

    def generate_output(self):
        self.program.generate_output_file()
