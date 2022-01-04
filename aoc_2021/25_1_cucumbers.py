import sys


def get_strings(my_file):
    strings = list()
    with open(my_file) as f:
        lines = f.readlines()
        for line in lines:
            strings.append(line.strip())
    return strings


def transpose(strings):
    many = len(strings[0])
    new_strings = ["" for _ in range(many)]
    for line in strings:
        for i in range(many):
            if line[i] == ".":
                char = "."
            elif line[i] == "v":
                char = ">"
            else:
                char = "v"
            new_strings[i] += char
    return new_strings


def display_strings(strings):
    for line in strings:
        print(line)
    print()


def one_direction(strings, vertical=False):
    if vertical:
        strings = transpose(strings)
    found = False
    new_strings = list()
    for line in strings:
        swap_ends = False
        if line[0] == "." and line[-1:] == ">":
            swap_ends = True
            found = True
        pos = -1
        while True:
            pos = line.find(">.", pos + 1)
            if pos >= 0:
                found = True
                line = line[:pos] + ".>" + line[pos + 2:]
                pos += 1
            if pos == -1:
                break
        if swap_ends:
            line = ">" + line[1:-1] + "."
        new_strings.append(line)
    if vertical:
        new_strings = transpose(new_strings)
    return new_strings, found


def main(my_file):
    strings = get_strings(my_file)
    # display_strings(strings)
    steps = 0
    while True:
        print(steps + 1)
        strings, found_h = one_direction(strings)
        # display_strings(strings)
        strings, found_v = one_direction(strings, True)
        steps += 1
        if not (found_h or found_v):
            break
        # display_strings(strings)
    print(steps)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "25_input.txt"
    main(filename)
