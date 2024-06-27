class Program(object):
    def __init__(self):
        self.codes = ['']

    def add_code(self, code: str, address: int = None):
        if address is None:
            address = len(self.codes)
        self.increase_size(address)
        self.codes[address] = code

    def increase_size(self, new_size: int):
        while len(self.codes) <= new_size:
            self.codes.append('')

    def generate_output_file(self):
        output_file = open('output.txt', 'w')
        for lineno in range(len(self.codes)):
            output_file.write(f"{lineno}\t{self.codes[lineno]}\n")
        output_file.close()
