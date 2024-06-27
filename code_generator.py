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
        self.main_address = 0

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
            # ActionSymbol.ARRAYINDEX: self.action_manager.assign,
            # '#startArgumentList': self.action_manager.start_argument_list,
            # '#endArgumentList': self.action_manager.end_argument_list,
            # '#jpfFromSaved': self.action_manager.jpf_from_saved,
            # '#jpFromSaved': self.action_manager.jp_from_saved,
            # '#saveAndJpfFromLastSave': self.action_manager.save_and_jpf_from_last_save,
            # '#assign': self.action_manager.assign,
            # '#startNoPush': self.action_manager.start_no_push,
            # '#endNoPush': self.action_manager.end_no_push,
            # '#declareArray': self.action_manager.declare_array,
            # '#array': self.action_manager.array,
            # '#until': self.action_manager.until,
            # '#handleBreaks': self.action_manager.handle_breaks,
            # '#break': self.action_manager.add_break,
            # '#pop': self.action_manager.pop,
            # '#checkDeclaration': self.action_manager.check_declaration,
            # '#uncheckDeclaration': self.action_manager.uncheck_declaration,
            # '#declareFunction': self.action_manager.declare_function,
            # '#openScope': self.action_manager.open_scope,
            # '#closeScope': self.action_manager.close_scope,
            # '#setFunctionScopeFlag': self.action_manager.set_function_scope_flag,
            # '#popParam': self.action_manager.pop_param,
            # '#call': self.action_manager.call,
            # '#setReturnValue': self.action_manager.set_return_value,
            # '#jumpBack': self.action_manager.jump_back,
            # '#addArgumentCount': self.action_manager.add_argument_count,
            # '#zeroInitialize': self.action_manager.zero_initialize,
            # '#arrayParam': self.action_manager.array_param,
            # '#startBreakScope': self.action_manager.start_break_scope,
            # '#setForceDeclarationFlag': self.action_manager.set_force_declaration_flag,
            # '#unsetForceDeclarationFlag': self.action_manager.unset_force_declaration_flag,
            # '#saveType': self.action_manager.save_type,
            # '#checkType': self.action_manager.check_type,
            # '#startRHS': self.action_manager.start_rhs,
            # '#endRHS': self.action_manager.end_rhs,
        }

        # initialization_instructions = [
        #     Assign(f"#{STACK_START_ADDRESS}", self.register_file.stack_pointer_register_address),
        #     Assign("#0", self.register_file.return_address_register_address),
        #     Assign("#0", self.register_file.return_value_register_address),
        # ]
        #
        # self.push_instructions(initialization_instructions)

        # self.i += 1

        self.add_output_function()




    def act(self, action, *args):
        self.actions[action](*args)


    def add_code(self, code, address=None):
        if type(address) == str and address[0] == '#':
            address = int(address[1:])

        self.program.add_code(code, address)


    def move_code_stack_head(self):
        self.program.increase_size(len(self.program.codes) + 1)


    def get_current_code_stack_head(self):
        return len(self.program.codes)


    def add_main_address(self, code: str):
        self.program.add_code(code, self.main_address)


    def get_next_data_address(self):
        address = self.data_address
        self.data_address += 4
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
