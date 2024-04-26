
# Hossein Aghaei - 98105619


from parser import Parser

parser = Parser()
parser.parse()
#
# # get_next_token()
#
#
# file = open('follow-set.txt', 'r')
#
# columns = file.readline().split()
#
# first_set = {}
# row = file.readline().split()
# while row:
#     firsts = [columns[i-1] if columns[i-1] != '┤' else '$' for i in range(len(columns) + 1) if row[i] == '+']
#     first_set[row[0]] = firsts
#     print(f"NonTerminal.{row[0]}:", firsts, ",")
#     row = file.readline().split()