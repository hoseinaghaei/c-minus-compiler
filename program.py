class Program(object):
    def __init__(self):
        self.codes = []

    def add_code(self, code: str, address: int = None):
        if address is None:
            address = self.get_code_stack_head()
        self.increase_size(address)
        self.codes[address] = code

    def increase_size(self, new_size: int):
        while self.get_code_stack_head() <= new_size:
            self.codes.append('')

    def generate_output_file(self):
        output_file = open('output.txt', 'w')
        for lineno in range(self.get_code_stack_head()):
            output_file.write(f"{lineno}\t{self.codes[lineno]}\n")
        output_file.close()

    def get_code_stack_head(self):
        return len(self.codes)
