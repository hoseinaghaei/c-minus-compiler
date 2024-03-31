import sys

from scanner import get_next_token


def compare(file1, file2):
    with open(file1, "r") as file:
        # Read all lines from the file into a list
        lines = file.readlines()

        # Trim each line and store in a new list
        trimmed_lines = [line.strip() for line in lines]
        f1_data = "\n".join(trimmed_lines)

    with open(file2, "r") as file:
        # Read all lines from the file into a list
        lines = file.readlines()

        # Trim each line and store in a new list
        trimmed_lines = [line.strip() for line in lines]
        f2_data = "\n".join(trimmed_lines)

    if f2_data == f1_data:
        print("Files match")
    else:
        print("fuck", file1, file2)


if __name__ == "__main__":
    dir = sys.argv[1]
    input = f"{dir}/input.txt"
    print(input)
    get_next_token(input)
    compare(f"{dir}/lexical_errors.txt", "lexical_errors.txt")
    compare(f"{dir}/tokens.txt", "tokens.txt")