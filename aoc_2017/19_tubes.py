import sys
import numpy as np


def get_grid(my_file):
    lists = list()
    with open(my_file) as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip("\n")
            if len(line) > 0:
                lists.append([ch for ch in line])
    grid = np.array(lists)
    return grid


def make_step(grid, position, direction):
    step = 1
    directions = {"-": np.array((0, 1)),
                  "|": np.array((1, 0)),
                  "+": None,
                  " ": (0, 0)}
    letter = None
    rows, columns = grid.shape
    row, column = position + direction
    new_value = grid[row, column]
    new_direction = directions.get(new_value, (7, 7))
    if new_direction is None:
        step += 1
        # change direction
        new_direction = "-" if direction[1] == 0 else "|"
        c, r = [None, None], [None, None]
        c[0], r[0] = direction
        c[1], r[1] = -direction
        turn_index = -1
        turn_directions = [None, None]
        for i in [0, 1]:
            if 0 <= row + r[i] < rows and 0 <= column + c[i] < columns:
                turn_directions[i] = grid[row + r[i], column + c[i]]
        # after a turn options are (to be checked in this order):
        # 1. line (new_direction) and whatever: then follow line
        # 2. letter and whatever: then follow letter
        #    the 'whatever' cannot be "|", "-", "+", it can be " " or None
        if new_direction in turn_directions:
            turn_index = turn_directions.index(new_direction)
        elif " " in turn_directions:
            turn_index = 1 - turn_directions.index(" ")
            letter = turn_directions[turn_index]
        elif None in turn_directions:
            turn_index = 1 - turn_directions.index(None)
            letter = turn_directions[turn_index]
        return np.array((row + r[turn_index], column + c[turn_index])), \
               np.array((r[turn_index], c[turn_index])), letter, step
    elif sum(new_direction) > 10:
        letter = new_value
        new_direction = direction
    elif sum(new_direction) == 0:
        return None, None, None, step  # end of route
    else:
        new_direction = direction
    return np.array((row, column)), new_direction, letter, step


def main(my_file):
    # all positions and directions: (row, column)
    grid = get_grid(my_file)
    position = np.array((0, list(grid[0]).index("|")))
    direction = np.array((1, 0))
    answer = ""
    steps = 0
    while True:
        position, direction, letter, step = make_step(grid, position, direction)
        steps += step
        if letter:
            answer += letter
        elif position is None:
            break
    print("part 1:", answer)
    print("part 2:", steps)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "19_input.txt"
    main(filename)
