import sys
import numpy as np


def get_commands(my_file):
    commands = list()
    with open(my_file) as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip().split()
            if len(line) == 2:
                coordinates = list(map(int, line[1].split("x")))
                commands.append(["rect", coordinates[0], coordinates[1]])
            else:
                row_column = int(line[2].split("=")[1])
                shift = int(line[4])
                commands.append([line[1], row_column, shift])
    return commands


def rotate_row(grid, row, shift):
    columns = grid.shape[1]
    the_row = list(grid[row])
    the_row = the_row[columns - shift:] + the_row[:columns - shift]
    grid[row] = np.array(the_row)
    return grid


def rotate_column(grid, column, shift):
    rows = grid.shape[0]
    the_column = list(grid[:, column])
    the_column = the_column[rows - shift:] + the_column[:rows - shift]
    grid[:, column] = np.array(the_column)
    return grid


def apply_command(grid, command):
    if command[0] == "rect":
        for row in range(command[2]):
            for column in range(command[1]):
                grid[row, column] = 1
    elif command[0] == "row":
        grid = rotate_row(grid, command[1], command[2])
    elif command[0] == "column":
        grid = rotate_column(grid, command[1], command[2])
    else:
        print("ZONK")
        quit()
    return grid


def apply_commands(grid, commands):
    for command in commands:
        grid = apply_command(grid, command)
    return grid


def display_grid(grid):
    for row in grid:
        for i, elt in enumerate(row):
            if elt == 1:
                print("#", end="")
            else:
                print(" ", end="")
            if (i + 1) % 5 == 0:
                print(" ", end="")
        print()


def main(my_file):
    commands = get_commands(my_file)
    print(commands)
    grid = np.zeros([6, 50])
    grid = apply_commands(grid, commands)
    print(sum(sum(grid)))
    display_grid(grid)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "08_input.txt"
    main(filename)
