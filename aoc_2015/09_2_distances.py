import sys
import itertools


def get_graph_from_data(my_file):
    # items are of the type:
    # city : [{city2: dist2}, {city3: dist3}, ...]
    graph = dict()
    with open(my_file) as f:
        lines = f.readlines()
        for line in lines:
            tmp = line.split(" = ")
            distance = int(tmp[1])
            city_1, city_2 = tmp[0].split(" to ")
            if city_1 not in graph:
                graph[city_1] = dict()
            graph[city_1][city_2] = distance
            if city_2 not in graph:
                graph[city_2] = dict()
            graph[city_2][city_1] = distance
    return graph


def all_paths(graph):
    cities = list(graph.keys())
    n = len(cities)
    all_options = list(itertools.permutations(cities))
    distances = dict()
    for ind, permutation in enumerate(all_options):
        distance = 0
        found = False
        for i in range(n - 1):
            found = False
            current_city = permutation[i]
            neighbours = graph.get(current_city)
            next_city = permutation[i + 1]
            if next_city in neighbours:
                distance += neighbours.get(next_city)
                found = True
            else:
                break
        if found:
            distances[ind] = distance
    return distances, all_options


def main(my_file):
    graph = get_graph_from_data(my_file)
    paths, options = all_paths(graph)
    routes = list(paths.keys())
    distances = list(paths.values())
    min_d = min(distances)
    max_d = max(distances)
    print("min:", min_d, options[routes[distances.index(min_d)]])
    print("max:", max_d, options[routes[distances.index(max_d)]])


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "09_input.txt"
    main(filename)
