import sys


def get_list_from_file(my_file):
    # returns a list of elements:
    # [command, start, end], where:
    # command = toggle / on / off
    # start = [x, y]
    # end = [x,y]
    ret_list = list()
    with open(my_file) as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip("\n")
            line_list = list()
            if line.startswith("toggle"):
                line_list.append("toggle")
                remains = line[7:]
            elif line.startswith("turn off"):
                line_list.append("off")
                remains = line[9:]
            elif line.startswith("turn on"):
                line_list.append("on")
                remains = line[8:]
            points = remains.split(" through ")
            line_list += [list(map(int, point.split(","))) for point in points]
            ret_list.append(line_list)
    return ret_list


def turn_on_off(grid, start, end, value):
    # start = [x, y], end = [x, y], value = 0 for off / 1 for on
    for column in range(start[0], end[0] + 1):
        for row in range(start[1], end[1] + 1):
            grid[row][column] = value
    return grid


def toggle(grid, start, end):
    # start = [x, y], end = [x, y]
    for column in range(start[0], end[0] + 1):
        for row in range(start[1], end[1] + 1):
            grid[row][column] = 1 - grid[row][column]
    return grid


def how_many_lit(grid):
    return sum([sum(elt) for elt in grid])


def change_lightness(grid, start, end, value):
    # start = [x, y], end = [x, y], value = -1, 1 or 2
    for column in range(start[0], end[0] + 1):
        for row in range(start[1], end[1] + 1):
            grid[row][column] = max(0, grid[row][column] + value)
    return grid


def main(my_file):
    grid = [[0 for _ in range(1000)] for _ in range(1000)]
    lines = get_list_from_file(my_file)
    for line in lines:
        if line[0] == "toggle":
            grid = change_lightness(grid, line[1], line[2], 2)
        elif line[0] == "on":
            grid = change_lightness(grid, line[1], line[2], 1)
        elif line[0] == "off":
            grid = change_lightness(grid, line[1], line[2], -1)
        else:
            raise ValueError("incorrect data")
    print(how_many_lit(grid))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "06_input.txt"
    main(filename)
