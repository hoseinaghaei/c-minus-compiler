# Hossein Aghaei - 98105619
# Zahra Azar - 99109744
from code_generator import CodeGenerator
from parser import Parser


if __name__ == "__main__":
    code_generator = CodeGenerator()
    parser = Parser(code_generator, file='input_v2.txt')
    parser.parse()

# #
# # get_next_token()
#
#
# file = open('grammar/first-set.txt', 'r')
#
# columns = file.readline().split()
#
# first_set = {}
# row = file.readline().split()
# while row:
#     firsts = [columns[i-1] if columns[i-1] != '┤' else '$' for i in range(len(columns) + 1) if row[i] == '+']
#     first_set[row[0]] = firsts
#     s = []
#     for first in firsts:
#         for e in Terminal:
#             if first == e.value:
#                 s.append(f"Terminal.{e.name}")
#                 break
#         if first == 'ε':
#             s.append(f"NonTerminal.EPSILON")
#     print(f"NonTerminal.{row[0]}:", s, ",")
#     row = file.readline().split()