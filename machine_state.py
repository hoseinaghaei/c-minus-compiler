from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from code_generator import CodeGenerator


class MachineState:
    def __init__(self, code_generator: "CodeGenerator"):
        self.code_generator = code_generator
        self.return_address_ptr = self.code_generator.get_data_address()
        self.return_value_ptr = self.code_generator.get_data_address()
        self.top_sp_ptr = self.code_generator.get_data_address()

    def initialize_machine_state(self, top_sp_ptr):
        self.code_generator.add_code(f"(ASSIGN, #{top_sp_ptr}, {self.top_sp_ptr}, )")
        self.code_generator.add_code(f"(ASSIGN, #0, {self.return_address_ptr}, )")
        self.code_generator.add_code(f"(ASSIGN, #0, {self.return_value_ptr}, )")

    def save_return_address(self, args_len):
        code = f"(ASSIGN, #{self.code_generator.get_current_code_stack_head() + args_len * 2 + 2}, {self.return_address_ptr}, )"
        self.code_generator.add_code(code)

    def save_return_value(self, value):
        code = f"(ASSIGN, {value}, {self.return_value_ptr}, )"
        self.code_generator.add_code(code)

    def save_machine_state(self):
        self.code_generator.call_stack.push(self.return_address_ptr)
        self.code_generator.call_stack.push(self.top_sp_ptr)

    def restore_machine_state(self):
        self.code_generator.call_stack.pop(self.top_sp_ptr)
        self.code_generator.call_stack.pop(self.return_address_ptr)

