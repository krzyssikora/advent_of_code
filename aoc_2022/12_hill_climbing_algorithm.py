import sys
import os
import numpy as np


def get_data_lines(my_file):
    with open(my_file) as f:
        lines = f.readlines()
    return [line.strip('\n').strip() for line in lines]


def get_grid_from_lines(lines):
    def char_to_int(ch):
        return ord(ch) - ord('a')

    list_for_grid = list()
    for line in lines:
        list_for_grid.append(list(map(char_to_int, list(line))))

    grid = np.array(list_for_grid)

    pos_s = np.where(grid == ord('S') - ord('a'))
    r_s = pos_s[0][0]
    c_s = pos_s[1][0]
    grid[r_s][c_s] = 0

    pos_e = np.where(grid == ord('E') - ord('a'))
    r_e = pos_e[0][0]
    c_e = pos_e[1][0]
    grid[r_e][c_e] = ord('z') - ord('a')

    return grid, (r_s, c_s), (r_e, c_e)


def can_go(vertex_from, vertex_to, grid):
    return grid[vertex_from] - 1 <= grid[vertex_to]


def get_neighbours(vertex, grid):
    rows, columns = grid.shape
    r, c = vertex
    neighbours = set()
    if c > 0 and can_go(vertex, (r, c - 1), grid):
        neighbours.add((r, c - 1))
    if c < columns - 1 and can_go(vertex, (r, c + 1), grid):
        neighbours.add((r, c + 1))
    if r > 0 and can_go(vertex, (r - 1, c), grid):
        neighbours.add((r - 1, c))
    if r < rows - 1 and can_go(vertex, (r + 1, c), grid):
        neighbours.add((r + 1, c))

    return neighbours


def dijkstra(grid, start):
    rows, columns = grid.shape
    distances = {(r, c): rows * columns for r in range(rows) for c in range(columns)}
    distances[start] = 0
    previous = {(r, c): None for r in range(rows) for c in range(columns)}
    sorted_queue = sorted(distances, key=distances.get)

    while True:
        queue = {v: distances[v] for v in sorted_queue}
        if not queue:
            break
        sorted_queue = sorted(queue, key=queue.get)
        u = sorted_queue[0]
        sorted_queue = sorted_queue[1:]

        neighbours = get_neighbours(u, grid)
        for neighbour in neighbours:
            alternative = distances[u] + 1
            if alternative < distances[neighbour]:
                distances[neighbour] = alternative
                previous[neighbour] = u

    return distances, previous


def display_distances(distances, grid):
    rows, columns = grid.shape
    ret_string = ''
    for row in range(rows):
        for column in range(columns):
            ret_string += str(distances[(row, column)]).rjust(3)
        ret_string += '\n'
    print(ret_string)


def get_level_a_spots(grid):
    level_a_spots = set()
    rows, columns = grid.shape
    for row in range(rows):
        for column in range(columns):
            if grid[(row, column)] == 0:
                level_a_spots.add((row, column))
    return level_a_spots


def get_level_a_distances(grid, distances):
    level_a_spots = get_level_a_spots(grid)
    level_a_distances = dict()
    for spot in level_a_spots:
        level_a_distances[spot] = distances[spot]
    return level_a_distances.get(min(level_a_distances, key=level_a_distances.get))


def main(my_file):
    lines = get_data_lines(my_file)
    grid, start, end = get_grid_from_lines(lines)
    distances, previous = dijkstra(grid, end)
    print("part 1:", distances[start])
    print("part 2:", get_level_a_distances(grid, distances))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = f'{os.path.basename(__file__)[:2]}_input.txt'
    main(filename)
