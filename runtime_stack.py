from typing import TYPE_CHECKING

from RegisterFile import RegisterFile

if TYPE_CHECKING:
    from code_generator import CodeGenerator

class RuntimeStack:
    def __init__(self, code_generator: "CodeGenerator", register_file: RegisterFile):
        self.code_generator = code_generator
        self.register_file = register_file

    def push(self, data):
        code = f"(SUB, {self.register_file.stack_pointer_register_address}, #4, {self.register_file.stack_pointer_register_address})"
        self.code_generator.add_code(code)
        code = f"(ASSIGN, {data}, @{self.register_file.stack_pointer_register_address}, )"
        self.code_generator.add_code(code)

    def pop(self, address):
        self.code_generator.add_code(f"(ASSIGN, @{self.register_file.stack_pointer_register_address}, {address}, )")
        self.code_generator.add_code(f"(ADD, {self.register_file.stack_pointer_register_address}, #4, {self.register_file.stack_pointer_register_address})")
