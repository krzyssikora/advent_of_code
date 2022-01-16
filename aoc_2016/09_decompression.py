import sys
import re


def get_markers(my_file):
    with open(my_file) as f:
        line = f.readline()
        line = line.strip()
        pattern = r"\(([0-9]+)x([0-9]+)\)"
        matches = re.finditer(pattern, line)
        markers = list()
        previous_end = -1
        previous_shift = 0
        for m in matches:
            position = m.span()
            value = tuple(map(int, (m.group(1), m.group(2))))
            if position[0] < previous_end + previous_shift:
                continue
            previous_end = position[1]
            previous_shift = value[0]
            markers.append([position, value])
    return line, markers


def single_decompression(string, marker):
    (start, end), (chars_num, many) = marker
    fragment = string[end: end + chars_num]
    string = string[:start] + fragment * many + string[end + chars_num:]
    return string


def decompress(string):
    ret = 0
    while "(" in string:
        position = string.find("(")
        ret += position
        string = string[position + 1:]
        position = string.find(")")
        chars_num, many = tuple(map(int, string[: position].split("x")))
        # ret += chars_num * many  # this would work for part 1
        ret += decompress(string[position + 1: position + 1 + chars_num]) * many
        string = string[position + chars_num + 1:]

    ret += len(string)
    return ret


def main(my_file):
    initial_string, markers = get_markers(my_file)
    print("part 1")
    string = initial_string
    while True:
        if len(markers) == 0:
            break
        marker = markers.pop()
        string = single_decompression(string, marker)
    print(len(string) - string.count(" "))
    print("part 2")
    print(decompress(string))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "09_input.txt"
    main(filename)
