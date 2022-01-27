import sys


def get_commands(my_file):
    commands = list()
    with open(my_file) as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip().split()
            if line[0] == "move":
                commands.append(("move", int(line[2]), int(line[5])))
            elif line[0] == "reverse":
                commands.append(("reverse", int(line[2]), int(line[4])))
            elif line[0] == "rotate":
                if line[1] == "based":
                    commands.append(("rotate pos", line[-1]))
                elif line[1] == "left":
                    commands.append(("rotate left", int(line[2])))
                elif line[1] == "right":
                    commands.append(("rotate right", int(line[2])))
            elif line[0] == "swap":
                if line[1] == "letter":
                    commands.append(("swap letter", line[2], line[5]))
                elif line[1] == "position":
                    commands.append(("swap position", int(line[2]), int(line[5])))
    return commands


def move(string, pos_from, pos_to):
    char = string[pos_from]
    string = string[:pos_from] + string[pos_from + 1:]
    string = string[:pos_to] + char + string[pos_to:]
    return string


def reverse(string, pos_from, pos_to):
    string = "*" + string
    string = string[:pos_from + 1] + string[pos_to + 1: pos_from:-1] + string[pos_to + 2:]
    return string[1:]


def rotate_pos(string, char):
    idx = string.index(char)
    pos = (1 + idx + 1 * (idx >= 4)) % len(string)
    return string[-pos:] + string[:-pos]


def rotate_left(string, pos):
    return string[pos:] + string[:pos]


def rotate_right(string, pos):
    return string[-pos:] + string[:-pos]


def swap_letters(string, char_1, char_2):
    string = string.replace(char_1, "*")
    string = string.replace(char_2, char_1)
    return string.replace("*", char_2)


def swap_positions(string, pos_1, pos_2):
    char = string[pos_1]
    string = string[:pos_1] + string[pos_2] + string[pos_1 + 1:]
    string = string[:pos_2] + char + string[pos_2 + 1:]
    return string


def read_commands(string, commands):
    for command in commands:
        if command[0] == "move":
            string = move(string, command[1], command[2])
        elif command[0] == "reverse":
            string = reverse(string, command[1], command[2])
        elif command[0] == "rotate pos":
            string = rotate_pos(string, command[1])
        elif command[0] == "rotate left":
            string = rotate_left(string, command[1])
        elif command[0] == "rotate right":
            string = rotate_right(string, command[1])
        elif command[0] == "swap letter":
            string = swap_letters(string, command[1], command[2])
        elif command[0] == "swap position":
            string = swap_positions(string, command[1], command[2])
    return string


def unscramble(string, commands):
    commands = commands[::-1]
    for command in commands:
        if command[0] == "move":
            # move back, i.e. swap positions
            string = move(string, command[2], command[1])
        elif command[0] == "reverse":
            # reverse is self-inverse
            string = reverse(string, command[1], command[2])
        elif command[0] == "rotate pos":
            # pos   shift   new_pos
            # 0     1       1
            # 1     2       3
            # 2     3       5
            # 3     4       7
            # 4     6       2
            # 5     7       4
            # 6     8       6
            # 7     9       0
            new_pos = string.index(command[1])
            shift = {1: 1, 3: 2, 5: 3, 7: 4, 2: 6, 4: 7, 6: 8, 0: 1}
            string = rotate_left(string, shift.get(new_pos))
        elif command[0] == "rotate left":
            # reverse: rotate right
            string = rotate_right(string, command[1])
        elif command[0] == "rotate right":
            # reverse: rotate left
            string = rotate_left(string, command[1])
        elif command[0] == "swap letter":
            # swapping is self-inverse
            string = swap_letters(string, command[1], command[2])
        elif command[0] == "swap position":
            # swapping is self-inverse
            string = swap_positions(string, command[1], command[2])
    return string


def main(my_file):
    string = "abcdefgh"
    # string = "abcde"
    commands = get_commands(my_file)
    print("part 1:", read_commands(string, commands))
    string = "fbgdceah"
    print("part 2:", unscramble(string, commands))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "21_input.txt"
    main(filename)
