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


def line_segment(position_1, position_2):
    # excludes position_1, includes position_2
    ret_path = list()
    vec_x, vec_y = position_2[0] - position_1[0], position_2[1] - position_1[1]
    steps = abs(vec_x) + abs(vec_y)
    vec_x //= steps
    vec_y //= steps
    for step in range(1, steps + 1):
        ret_path.append([position_1[0] + vec_x * step, position_1[1] + vec_y * step])
    return ret_path


def block_visited_twice(commands):
    position = [0, 0]
    direction = [0, 1]
    my_path = [position]
    for command in commands:
        position, direction = make_step(position, command, direction)
        previous = my_path[len(my_path) - 1]
        segment = line_segment(previous, position)
        for point in segment:
            if point in my_path:
                return abs(point[0]) + abs(point[1])
            else:
                my_path.append(point)
    return None


def main(my_file):
    commands = get_commands(my_file)
    print(block_visited_twice(commands))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "01_input.txt"
    main(filename)
