from Program import Program
from RegisterFile import RegisterFile
from action_manager import ActionManager
from runtime_stack import RuntimeStack
from utils import SymbolTable, ActionSymbol, TokenDTO


class CodeGenerator:
    def __init__(self):
        # self.i = 0
        self.data_address = 100
        # self.data_address = 100000
        self.temp_address = 500
        # self.temp_address = 500004
        self.ss = []
        self.data_and_temp_stack = []

        self.function_data_start_pointer = 0
        self.function_temp_start_pointer = 0

        self.program = Program()

        self.symbol_table = SymbolTable(self)
        self.register_file = RegisterFile(self)
        self.runtime_stack = RuntimeStack(self, self.register_file)
        self.action_manager = ActionManager(self, self.symbol_table)

        self.actions = {
            ActionSymbol.PID: self.action_manager.pid,
            ActionSymbol.DECLAREID: self.action_manager.declare_id,
            ActionSymbol.INITZERO: self.action_manager.init_zero,
            ActionSymbol.PNUM: self.action_manager.pnum,
            ActionSymbol.POPERAND: self.action_manager.push_operation,
            ActionSymbol.EVALOPERATION: self.action_manager.eval_operation,
            ActionSymbol.IFSAVE: self.action_manager.save,
            ActionSymbol.STARTELSE: self.action_manager.start_else,
            ActionSymbol.ENDIF: self.action_manager.endif,
            ActionSymbol.ENDIFAFTERELSE: self.action_manager.endif_after_else,
            ActionSymbol.DECLAREFUNCTION: self.action_manager.declare_function,
            ActionSymbol.FUNCOPENSCOPEFLAG: self.action_manager.set_function_scope_flag,
            ActionSymbol.POPPARAM: self.action_manager.pop_param,
            ActionSymbol.OPENSCOPE: self.action_manager.open_scope,
            ActionSymbol.CLOSESCOP: self.action_manager.close_scope,
            ActionSymbol.CALL: self.action_manager.call,
            ActionSymbol.RETURN: self.action_manager.return_back,
            ActionSymbol.ASSIGN: self.action_manager.assign,
            ActionSymbol.START_ARGUMENT: self.action_manager.start_argument_list,
            ActionSymbol.ADD_ARGUMENT: self.action_manager.add_argument_count,
            ActionSymbol.END_ARGUMENT: self.action_manager.end_argument_count,
            ActionSymbol.RETURNVALUE: self.action_manager.set_return_value,
            ActionSymbol.POP: self.action_manager.pop,
            ActionSymbol.DECLARE_ARRAY: self.action_manager.declare_array,
            ActionSymbol.ARRAY_PARAM: self.action_manager.array_param,
            ActionSymbol.ARRAYINDEX: self.action_manager.array_index,
            ActionSymbol.FORCHECKCONDITION: self.action_manager.for_check_condition,
            ActionSymbol.FORJUMPCHECKCONDITION: self.action_manager.for_jump_check_condition,
            ActionSymbol.FORSAVE: self.action_manager.for_save,
            ActionSymbol.BREAK: self.action_manager.break_key,
            ActionSymbol.BREAKSCOPE: self.action_manager.break_scope,
            ActionSymbol.BREAKSAVE: self.action_manager.break_save,
            ActionSymbol.DEBUG: self.action_manager.debug,
            ActionSymbol.NEGATE: self.action_manager.negate,
        }

        self.add_code(f"(ASSIGN, #{self.temp_address}, {self.register_file.stack_pointer_register_address}, )")
        self.add_code(f"(ASSIGN, #0, {self.register_file.return_address_register_address}, )")
        self.add_code(f"(ASSIGN, #0, {self.register_file.return_value_register_address}, )")

        self.main_address = self.get_current_code_stack_head()
        self.move_code_stack_head()
        self.add_output_function()




    def act(self, action, *args):
        self.actions[action](*args)


    def add_code(self, code, address=None):
        if type(address) == str and address[0] == '#':
            address = int(address[1:])

        self.program.add_code(code, address)


    def move_code_stack_head(self):
        self.program.increase_size(len(self.program.codes))


    def get_current_code_stack_head(self):
        return len(self.program.codes)


    def add_main_address(self, code: str):
        self.program.add_code(code, self.main_address)


    def get_next_data_address(self, size=4):
        address = self.data_address
        self.data_address += size
        return address


    def get_next_temp_address(self):
        address = self.temp_address
        self.temp_address += 4
        return address


    def add_output_function(self):
        self.symbol_table.add_id_if_not_exist('output')
        self.act(ActionSymbol.PID, TokenDTO(lexeme='output'))
        self.act(ActionSymbol.DECLAREFUNCTION, None)
        self.act(ActionSymbol.OPENSCOPE, None)
        self.act(ActionSymbol.FUNCOPENSCOPEFLAG, None)
        self.symbol_table.add_id_if_not_exist('a')
        self.act(ActionSymbol.PID, TokenDTO(lexeme="a"))
        self.act(ActionSymbol.POPPARAM, None)
        self.act(ActionSymbol.PID, TokenDTO(lexeme="a"))
        self.act(ActionSymbol.OPENSCOPE, None)
        self.add_code(f"(PRINT, {self.ss.pop()}, , )")
        self.act(ActionSymbol.CLOSESCOP, None)
        self.act(ActionSymbol.RETURN, None)

    def generate_output(self):
        self.program.generate_output_file()
