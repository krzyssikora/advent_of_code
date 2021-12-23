import sys
import re


def get_numbers(line):
    p = re.compile("([-0-9]+)")
    positions = list()
    numbers = list()
    for m in p.finditer(line):
        positions.append(int(m.start()))
        numbers.append(int(m.group()))
    return numbers, positions


def find_brackets_around(line, position, opening="{", closing="}"):
    left = line.rfind(opening, position)
    right = line.find(closing, left)
    if right < position:
        return -1, -1
    else:
        return left, right


def main(my_file):
    with open(my_file) as f:
        line = f.read()
    numbers, positions = get_numbers(line)
    neglected = 0
    for number, position in zip(numbers, positions):
        left, right = find_brackets_around_red(line, position)
        left_square, right_square = find_brackets_around(line, position, "[", "]")
        if left_square < left < right < right_square:
            for nr, pos in zip(numbers, positions):
                if left < pos < right:
                    neglected += nr
    print(sum(numbers), neglected, sum(numbers) - neglected)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "12_input.txt"
    main(filename)
