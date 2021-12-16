import sys


def get_grid_from_data(my_file):
    grid = list()
    with open(my_file) as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip("\n")
            grid.append(list(map(int, list(line))))
    return grid


def get_dict_min(d):
    minimum = min(d.values())
    return list(d.keys())[list(d.values()).index(minimum)], minimum


def get_path(grid, predecessors, start_row=0, start_column=0, end_row=None, end_column=None):
    size = len(grid)
    if end_row is None:
        end_row = size - 1
    if end_column is None:
        end_column = size - 1
    current_node = (end_row, end_column)
    path = list()
    while True:
        path.append(current_node)
        if current_node == (start_row, start_column):
            break
        current_node = predecessors.get(current_node)
    return path


def dijkstra(grid, start_row=0, start_column=0, end_row=None, end_column=None):
    # initialize
    size = len(grid)
    if end_row is None:
        end_row = size - 1
    if end_column is None:
        end_column = size - 1
    max_distance = size * size * 10
    distances = dict()
    unvisited = dict()
    predecessors = dict()
    for i in range(size):
        for j in range(size):
            distances[(i, j)] = max_distance
            unvisited[(i, j)] = max_distance
    distances[(start_row, start_column)] = 0
    unvisited[(start_row, start_column)] = 0
    # do the job
    while True:
        if len(unvisited) == 0:
            break
        current_node, min_distance = get_dict_min(unvisited)
        if min_distance == max_distance:
            break
        row, column = current_node[0], current_node[1]
        # get all neighbours of current node
        neighbours = list()
        if current_node[0] - 1 >= 0:
            neighbours.append((row - 1, column))
        if current_node[0] + 1 < size:
            neighbours.append((row + 1, column))
        if current_node[1] - 1 >= 0:
            neighbours.append((row, column - 1))
        if current_node[1] + 1 < size:
            neighbours.append((row, column + 1))
        for neighbour in neighbours:
            if neighbour in unvisited:
                if grid[neighbour[0]][neighbour[1]] + distances[current_node] < distances[neighbour]:
                    distances[neighbour] = grid[neighbour[0]][neighbour[1]] + distances[current_node]
                    unvisited[neighbour] = distances[neighbour]
                    predecessors[neighbour] = current_node
        del unvisited[current_node]
        if current_node == [end_row, end_column]:
            break
    return distances, predecessors


def display_grid(grid, path):
    size = len(grid)
    return_list = list()
    for row in range(size):
        row_string = ""
        for column in range(size):
            if (row, column) in path:
                row_string += "X "
            else:
                row_string += ". "
        return_list.append(row_string + "\n")
    return return_list


def main(my_file):
    grid = get_grid_from_data(my_file)
    size = len(grid) - 1
    distances, predecessors = dijkstra(grid)
    path = get_path(grid, predecessors)
    grid_displayed = display_grid(grid, path)
    with open("15_path.txt", "w") as f:
        for row in grid_displayed:
            f.write(row)
    print(distances[(size, size)])


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "15_input.txt"
    main(filename)
