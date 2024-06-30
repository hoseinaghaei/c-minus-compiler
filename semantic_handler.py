import scanner


class SemanticErrorHandler:
    def __init__(self):
        self.errors = []

    def has_error(self):
        return len(self.errors) != 0

    def not_defined(self, lexeme):
        self.errors.append((scanner.line_number, f"'{lexeme}' is not defined."))

    def arg_num_mismatch(self, func_name):
        self.errors.append((scanner.line_number, f"Mismatch in numbers of arguments of '{func_name}'."))

    def illegal_break(self):
        self.errors.append((scanner.line_number, "No 'for' found for 'break'."))

    def illegal_void(self, lexeme):
        self.errors.append((scanner.line_number, f"Illegal type of void for '{lexeme}'."))

    def operand_type_mismatch(self, expected, given):
        self.errors.append((scanner.line_number, f"Type mismatch in operands, Got {given} instead of {expected}."))

    def arg_type_mismatch(self, expected, given, index, func_name):
        self.errors.append((scanner.line_number, f"Mismatch in type of argument {index + 1} of '{func_name}'. Expected '{expected}' but got '{given}' instead."))

    def generate_error_file(self):
        if self.has_error():
            semantic_error_file = open('semantic_errors.txt', 'w')
            for line_number, error in self.errors:
                semantic_error_file.write(f"#{line_number} : Semantic Error! {error}\n")
            semantic_error_file.close()

