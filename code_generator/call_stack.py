from typing import TYPE_CHECKING

from code_generator.machine_state import MachineState

if TYPE_CHECKING:
    from code_generator import CodeGenerator


class CallStack:
    def __init__(self, code_generator: "CodeGenerator", machine_state: MachineState):
        self.code_generator = code_generator
        self.machine_state = machine_state

    def push(self, data):
        self.code_generator.add_code(f"(SUB, {self.machine_state.top_sp_ptr}, #4, {self.machine_state.top_sp_ptr})")
        self.code_generator.add_code(f"(ASSIGN, {data}, @{self.machine_state.top_sp_ptr}, )")

    def pop(self, address):
        self.code_generator.add_code(f"(ASSIGN, @{self.machine_state.top_sp_ptr}, {address}, )")
        self.code_generator.add_code(f"(ADD, {self.machine_state.top_sp_ptr}, #4, {self.machine_state.top_sp_ptr})")
