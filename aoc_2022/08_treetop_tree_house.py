import sys
import os
import numpy as np


def get_data_lines(my_file):
    with open(my_file) as f:
        lines = f.readlines()
    return [line.strip('\n').strip() for line in lines]


def get_forrest_from_lines(lines):
    return np.array([list(map(int, list(line))) for line in lines])


def get_number_of_trees_seen(forrest):
    trees_seen = set()
    num_rows, num_cols = forrest.shape

    for row in range(num_rows):
        max_height = -1
        for column in range(num_rows):
            if forrest[row, column] > max_height:
                max_height = forrest[row, column]
                trees_seen.add((row, column))

    for row in range(num_rows):
        max_height = -1
        for column in reversed(range(num_rows)):
            if forrest[row, column] > max_height:
                max_height = forrest[row, column]
                trees_seen.add((row, column))

    for column in range(num_rows):
        max_height = -1
        for row in range(num_rows):
            if forrest[row, column] > max_height:
                max_height = forrest[row, column]
                trees_seen.add((row, column))

    for column in range(num_rows):
        max_height = -1
        for row in reversed(range(num_rows)):
            if forrest[row, column] > max_height:
                max_height = forrest[row, column]
                trees_seen.add((row, column))

    return len(trees_seen)


def get_highest_scenic_score(forrest):
    num_rows, num_cols = forrest.shape
    visibility = [np.zeros((num_rows, num_cols)) for _ in range(4)]

    # look left
    for row in range(num_rows):
        previous = {i: 0 for i in range(10)}
        for column in range(1, num_rows):
            tree_height = forrest[row, column]
            if tree_height > forrest[row, column - 1]:
                visibility[0][row, column] = column - previous[tree_height]
            else:
                visibility[0][row, column] = 1
            for h in range(tree_height + 1):
                previous[h] = column

    # look right
    for row in range(num_rows):
        previous = {i: num_rows - 1 for i in range(10)}
        for column in reversed(range(num_rows - 1)):
            tree_height = forrest[row, column]
            if tree_height > forrest[row, column + 1]:
                visibility[1][row, column] = previous[tree_height] - column
            else:
                visibility[1][row, column] = 1
            for h in range(tree_height + 1):
                previous[h] = column

    # look up
    for column in range(num_rows):
        previous = {i: 0 for i in range(10)}
        for row in range(1, num_rows):
            tree_height = forrest[row, column]
            if tree_height > forrest[row - 1, column]:
                visibility[2][row, column] = row - previous[tree_height]
            else:
                visibility[2][row, column] = 1
            for h in range(tree_height + 1):
                previous[h] = row

    # look down
    for column in range(num_rows):
        previous = {i: num_rows - 1 for i in range(10)}
        for row in reversed(range(num_rows - 1)):
            tree_height = forrest[row, column]
            if tree_height > forrest[row + 1, column]:
                visibility[3][row, column] = previous[tree_height] - row
            else:
                visibility[3][row, column] = 1
            for h in range(tree_height + 1):
                previous[h] = row

    scenic_score = np.zeros((num_rows, num_cols))
    for row in range(num_rows):
        for column in range(num_rows):
            scenic_score[row, column] = np.prod([visibility[i][row, column] for i in range(4)])

    return int(np.max(scenic_score))


def main(my_file):
    lines = get_data_lines(my_file)
    forrest = get_forrest_from_lines(lines)

    print("part 1:", get_number_of_trees_seen(forrest))
    print("part 2:", get_highest_scenic_score(forrest))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = f'{os.path.basename(__file__)[:2]}_input.txt'
    main(filename)
