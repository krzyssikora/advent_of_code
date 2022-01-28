import sys
import numpy as np
import itertools


def get_map(my_file):
    global many
    tmp_map = list()
    with open(my_file) as f:
        lines = f.readlines()
        for line in lines:
            tmp_map.append(list(line.strip()))
    my_map = np.array(tmp_map)
    nodes = list()
    for node in range(many):
        pos = np.where(my_map == str(node))
        nodes.append((pos[0][0], pos[1][0]))
    return my_map, nodes


def bfs(my_map, initial, final):
    rows, columns = my_map.shape
    distances = {initial: 0}
    queue = [initial]
    while True:
        if len(queue) == 0:
            break
        current = queue.pop(0)
        if current == final:
            break
        row, column = current
        neighbours = set()
        if row - 1 > 0 and my_map[row - 1, column] != "#":
            neighbours.add((row - 1, column))
        if row + 1 < rows and my_map[row + 1, column] != "#":
            neighbours.add((row + 1, column))
        if column - 1 > 0 and my_map[row, column - 1] != "#":
            neighbours.add((row, column - 1))
        if column + 1 < columns and my_map[row, column + 1] != "#":
            neighbours.add((row, column + 1))
        for neighbour in neighbours:
            if neighbour not in distances or distances[neighbour] > distances[current] + 1:
                distances[neighbour] = distances[current] + 1
                queue.append(neighbour)
    return distances[final]


def find_nodes_distances(my_map, nodes):
    global many
    best_routes = [[None for _ in range(many)] for _ in range(many)]
    for node_1 in range(many):
        for node_2 in range(node_1, many):
            dist = bfs(my_map, nodes[node_1], nodes[node_2])
            best_routes[node_1][node_2] = dist
            best_routes[node_2][node_1] = dist
    return best_routes


def shortest_path_1(distances):
    global many
    perms = itertools.permutations(list(range(1, many)))
    options = list()
    for perm in perms:
        total = 0
        previous = 0
        idx = 0
        while True:
            if idx == many - 1:
                break
            following = perm[idx]
            total += distances[previous][following]
            idx += 1
            previous = following
        options.append((perm, total))
    return min(options, key=lambda x: x[1])


def shortest_path_2(distances):
    global many
    perms = itertools.permutations(list(range(1, many)))
    options = list()
    for perm in perms:
        total = 0
        previous = 0
        idx = 0
        while True:
            if idx == many - 1:
                break
            following = perm[idx]
            total += distances[previous][following]
            idx += 1
            previous = following
        total += distances[previous][0]
        options.append((perm, total))
    return min(options, key=lambda x: x[1])


def main(my_file):
    my_map, nodes = get_map(my_file)
    distances = find_nodes_distances(my_map, nodes)
    shortest_paths = [shortest_path_1, shortest_path_2]
    for part, shortest_path in zip([1, 2], shortest_paths):
        print(f"part {part}: shortest path is {shortest_path(distances)[0]}, distance is {shortest_path(distances)[1]}")


if __name__ == "__main__":
    many = 8  # number of nodes
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "24_input.txt"
    main(filename)
