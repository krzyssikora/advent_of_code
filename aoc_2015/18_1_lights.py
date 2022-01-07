import sys
import numpy as np


def get_grid(my_file):
    with open(my_file) as f:
        lines = f.readlines()
        rows = len(lines)
        columns = len(lines[0].strip())
        grid = np.zeros([rows, columns])
        for row in range(len(lines)):
            line = lines[row].strip()
            for column in range(len(line)):
                if line[column] == "#":
                    grid[row, column] = 1
    return grid


def make_step(grid):
    lights = get_lights(grid)
    rows, columns = grid.shape
    for r in range(rows):
        for c in range(columns):
            if grid[r, c] == 1:
                if lights[r, c] in {2, 3}:
                    pass
                else:
                    grid[r, c] = 0
            else:
                if lights[r, c] == 3:
                    grid[r, c] = 1
    return grid


def make_steps(grid, steps):
    for i in range(steps):
        grid = make_step(grid)
    return grid


def lights_on(grid):
    return sum(sum(grid))


def lights_in_neighbourhood(grid, row, column):
    lights = 0
    rows, columns = grid.shape
    for r in range(row - 1, row + 2):
        if r < 0 or r >= rows:
            continue
        for c in range(column - 1, column + 2):
            if c < 0 or c >= columns:
                continue
            if r == row and c == column:
                continue
            lights += grid[r, c]
    return lights


def get_lights(grid):
    rows, columns = grid.shape
    lights = np.zeros([rows, columns])
    for r in range(rows):
        for c in range(columns):
            lights[r, c] = lights_in_neighbourhood(grid, r, c)
    return lights


def main(my_file):
    grid = get_grid(my_file)
    print(int(lights_on(make_steps(grid, 100))))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "18_input.txt"
    main(filename)
