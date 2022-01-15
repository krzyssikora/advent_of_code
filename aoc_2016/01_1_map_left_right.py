import sys


def get_commands(my_file):
    commands = list()
    with open(my_file) as f:
        data = f.read().strip().split(", ")
        for elt in data:
            commands.append([elt[0], int(elt[1:])])
    return commands


def make_step(position, command, direction):
    x, y = position
    turn, many = command
    x_dir, y_dir = direction
    if turn == "L":
        x_dir, y_dir = -y_dir, x_dir
    elif turn == "R":
        x_dir, y_dir = y_dir, -x_dir
    x += many * x_dir
    y += many * y_dir
    return [x, y], [x_dir, y_dir]


def main(my_file):
    commands = get_commands(my_file)
    position = [0, 0]
    direction = [0, 1]
    for command in commands:
        position, direction = make_step(position, command, direction)
    print(abs(position[0]) + abs(position[1]))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "01_input.txt"
    main(filename)
