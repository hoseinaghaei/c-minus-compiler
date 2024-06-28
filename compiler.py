# Hossein Aghaei - 98105619
# Zahra Azar - 99109744

from code_generator import CodeGenerator
from parser import Parser

if __name__ == "__main__":
    code_generator = CodeGenerator()
    parser = Parser(code_generator)
    parser.parse()
