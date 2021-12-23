import sys
import re


def main(my_file):
    with open(my_file) as f:
        line = f.read()
    print(sum(get_numbers(line)))


def get_numbers(line):
    result = re.findall(r"([-0-9]+)", line)
    result = list(map(int, result))
    return result


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "12_input.txt"
    main(filename)
