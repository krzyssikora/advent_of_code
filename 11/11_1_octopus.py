def increase_by_1(grid, chosen=None):
    if chosen is None:
        for row in range(len(grid)):
            for column in range(len(grid[0])):
                grid[row][column] = min(grid[row][column] + 1, 10)
    else:
        for [row, column] in chosen:
            grid[row][column] = min(grid[row][column] + 1, 10)
    return grid


def get_grid_from_data(my_file):
    with open(my_file) as f:
        lines = f.readlines()
        return_grid = list()
        for line in lines:
            return_line = list()
            line = line.strip("\n")
            for elt in line:
                return_line.append(int(elt))
            if len(return_line) > 0:
                return_grid.append(return_line)
    return return_grid


def display_grid(grid):
    print()
    for row in range(len(grid)):
        for column in range(len(grid[0])):
            print(str(grid[row][column]).ljust(3), end="")
        print()


def get_adjacent(grid, new_flashes):
    rows = len(grid)
    columns = len(grid[0])
    adjacent = list()
    for [row, column] in new_flashes:
        for r in range(max(0, row - 1), min(rows - 1, row + 1) + 1):
            for c in range(max(0, column - 1), min(columns - 1, column + 1) + 1):
                adjacent.append([r, c])
    return adjacent


def get_flashes(grid, new_flashes):
    rows = len(grid)
    columns = len(grid[0])
    flashes_list = list()
    for row in range(rows):
        for column in range(columns):
            if [row, column] not in new_flashes and grid[row][column] > 9:
                flashes_list.append([row, column])
    return flashes_list


def main():
    octopus_grid = get_grid_from_data("11_input.txt")
    flashes_count = 0
    for step in range(100):
        used_flashes = list()
        octopus_grid = increase_by_1(octopus_grid)
        while True:
            new_flashes = get_flashes(octopus_grid, used_flashes)
            nothing_new = True
            for flash in new_flashes:
                nothing_new = nothing_new and (flash in used_flashes)
            if nothing_new:
                break
            for flash in new_flashes:
                if flash not in used_flashes:
                    used_flashes.append(flash)
                else:
                    new_flashes.remove(flash)
            adjacent_octopuses = get_adjacent(octopus_grid, new_flashes)
            octopus_grid = increase_by_1(octopus_grid, adjacent_octopuses)
        flashes_count += len(used_flashes)
        for [row, column] in used_flashes:
            octopus_grid[row][column] = 0
    print(flashes_count)


if __name__ == "__main__":
    main()
