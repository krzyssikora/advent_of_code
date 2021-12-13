import sys


def result_from_line(my_line, floor):
    char_number = 0
    my_line = my_line.strip("\n")
    for character in my_line:
        char_number += 1
        if character == "(":
            floor += 1
        elif character == ")":
            floor -= 1
            if floor < 0:
                return char_number, floor
        else:
            raise ValueError("incorrect character in data")
    return None, floor


def get_char_number(my_file):
    floor_number = 0
    with open(my_file) as f:
        lines = f.readlines()
        for line in lines:
            char_no, floor_no = result_from_line(line, floor_number)
            if char_no:
                return char_no
            else:
                floor_number += floor_no
    return char_no


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "01_input.txt"
    answer = get_char_number(filename)
    print(answer)
