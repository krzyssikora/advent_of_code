import sys
import os


def get_data_lines(my_file):
    with open(my_file) as f:
        lines = f.readlines()
    return [line.strip('\n').strip() for line in lines]


def add_b_to_a_k_times(a, b, k):
    return [aa + k * bb for aa, bb in zip(a, b)]


def get_moves_from_lines(lines, part):
    moves = list()
    for line in lines:
        direction, number_of_steps = line.split()
        step = {
            'R': [1, 0],
            'D': [0, -1],
            'L': [-1, 0],
            'U': [0, 1]
        }.get(direction)
        if part == 1:
            moves.append(add_b_to_a_k_times([0, 0], step, int(number_of_steps)))
        elif part == 2:
            for i in range(int(number_of_steps)):
                moves.append(step)
    return moves


def move_head(starting_position, move):
    return [starting_position[i] + move[i] for i in range(2)]


def get_steps(delta):
    sgn = delta // abs(delta)
    return [_ for _ in range(sgn, delta, sgn)]


def move_knot_and_mark_visited(current, previous):
    visited = set()
    dx = previous[0] - current[0]
    dy = previous[1] - current[1]

    if abs(dx) <= 1 and abs(dy) <= 1:
        return current, visited

    if abs(dx) == 1:
        current = add_b_to_a_k_times(current, [dx, 0], 1)
    elif abs(dy) == 1:
        current = add_b_to_a_k_times(current, [0, dy], 1)

    if abs(dx) <= 1 and dy != 0:
        visited = {tuple(add_b_to_a_k_times(current, [0, 1], k)) for k in get_steps(dy)}
        current = add_b_to_a_k_times(current, [0, 1], dy - dy // abs(dy))
    elif abs(dy) <= 1 and dx != 0:
        visited = {tuple(add_b_to_a_k_times(current, [1, 0], k)) for k in get_steps(dx)}
        current = add_b_to_a_k_times(current, [1, 0], dx - dx // abs(dx))

    return current, visited


def move_knot_by_one(current, previous, return_visited=True):
    visited = set() if return_visited else None
    dx = previous[0] - current[0]
    dy = previous[1] - current[1]
    if current == [1, 1] and previous == [2, 3]:
        print(f'dx: {dx}, dy: {dy}')

    if abs(dx) <= 1 and abs(dy) <= 1:
        return current, visited

    if dx != 0 and dy != 0:
        if return_visited:
            visited = {(current[0] + dx // abs(dx), current[1] + dy // abs(dy))}
        current = add_b_to_a_k_times(current, [dx // abs(dx), dy // abs(dy)], 1)
    elif dy != 0:
        if return_visited:
            visited = {tuple(add_b_to_a_k_times(current, [0, 1], k)) for k in get_steps(dy)}
        current = add_b_to_a_k_times(current, [0, 1], dy // abs(dy))
    elif dx != 0:
        if return_visited:
            visited = {tuple(add_b_to_a_k_times(current, [1, 0], k)) for k in get_steps(dx)}
        current = add_b_to_a_k_times(current, [1, 0], dx // abs(dx))

    return current, visited


def make_moves(moves, part):
    head = [0, 0]
    tail = [0, 0]
    visited = {(0, 0)}

    if part == 1:
        for move in moves:
            head = move_head(head, move)
            tail, visited_in_the_move = move_knot_and_mark_visited(tail, head)
            visited = visited.union(visited_in_the_move)

    if part == 2:
        rope = {i: [0, 0] for i in range(0, 10)}
        for move_idx, move in enumerate(moves):

            rope[0] = move_head(rope[0], move)
            for i in range(1, 9):
                position, thrash = move_knot_by_one(rope[i], rope[i - 1], False)
                rope[i] = position
            rope[9], visited_in_the_move = move_knot_by_one(rope[9], rope[8])
            visited = visited.union(visited_in_the_move)

    return len(visited)


def display_rope(rope, visited):
    x_min, x_max, y_min, y_max = -11, 15, -5, 16
    knots_seen = dict()
    for i in range(9, -1, -1):
        knots_seen[tuple(rope[i])] = str(i)
    disp_list = [['.' for _ in range(x_min, x_max)] for _ in range(y_min, y_max)]
    for x, y in visited:
        disp_list[y - y_min][x - x_min] = '#'
    for x, y in knots_seen:
        disp_list[y - y_min][x - x_min] = knots_seen[(x, y)]

    disp_string = '    ' + ''.join([str(i)[-1] for i in range(x_min, x_max)]) + '\n'
    for i in range(len(disp_list)):
        row = disp_list[len(disp_list) - i - 1]
        disp_string += str(len(disp_list) - i - 1 + y_min).ljust(3) + ' ' + ''.join(c for c in row) + '\n'

    print(disp_string)


def main(my_file):
    lines = get_data_lines(my_file)

    moves = get_moves_from_lines(lines, 1)
    print("part 1:", make_moves(moves, 1))

    moves = get_moves_from_lines(lines, 2)
    print("part 2:", make_moves(moves, 2))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = f'{os.path.basename(__file__)[:2]}_input.txt'
    main(filename)
