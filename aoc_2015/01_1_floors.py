import sys


def result_from_line(my_line):
    floor = 0
    my_line = my_line.strip("\n")
    for character in my_line:
        if character == "(":
            floor += 1
        elif character == ")":
            floor -= 1
        else:
            raise ValueError("incorrect character in data")
    return floor


def get_floor_number(my_file):
    floor_number = 0
    with open(my_file) as f:
        lines = f.readlines()
        for line in lines:
            floor_number += result_from_line(line)
    return floor_number


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "01_input.txt"
    answer = get_floor_number(filename)
    print(answer)
