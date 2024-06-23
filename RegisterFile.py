from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from code_generator import CodeGenerator


class RegisterFile:
    def __init__(self, code_generator: "CodeGenerator"):
        self.code_generator = code_generator
        self.return_address_register_address = self.code_generator.get_next_data_address()
        self.return_value_register_address = self.code_generator.get_next_data_address()
        self.stack_pointer_register_address = self.code_generator.get_next_data_address()

    def save_return_address(self, arg_count):
        code = f"(ASSIGN, #{self.code_generator.move_code_stack_head() + arg_count * 2 + 2}, {self.return_address_register_address}, )"
        self.code_generator.add_code(code)

    def save_return_value(self, value):
        code = f"(ASSIGN, {value}, {self.return_value_register_address}, )"
        self.code_generator.add_code(code)

    def push_registers(self):
        self.code_generator.runtime_stack.push(self.return_address_register_address)
        # self.codegen.runtime_stack.push(self.return_value_register_address)
        self.code_generator.runtime_stack.push(self.stack_pointer_register_address)

    def pop_registers(self):
        self.code_generator.runtime_stack.pop(self.stack_pointer_register_address)
        # self.codegen.runtime_stack.pop(self.return_value_register_address)
        self.code_generator.runtime_stack.pop(self.return_address_register_address)
