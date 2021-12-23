import sys


def get_graph_from_data(my_file):
    # items are of the type:
    # city : [city_id, [[city2, dist2], [city3, dist3], ...]]
    graph = dict()
    many = 0
    with open(my_file) as f:
        lines = f.readlines()
        for line in lines:
            tmp = line.split(" = ")
            distance = int(tmp[1])
            city_1, city_2 = tmp[0].split(" to ")
            if city_1 not in graph:
                graph[city_1] = [many, list()]
                many += 1
            graph[city_1][1].append([city_2, distance])
            if city_2 not in graph:
                graph[city_2] = [many, list()]
                many += 1
            graph[city_2][1].append([city_1, distance])
    return graph


def get_dict_min(d):
    minimum = min(d.values())
    return list(d.keys())[list(d.values()).index(minimum)], minimum


def dijkstra(graph):
    # initialize
    max_distance = float("inf")
    names = list()
    distances = [[max_distance for _ in range(2 ** len(graph))] for _ in range(len(graph))]
    priority_queue = list()
    for i in range(len(graph)):
        names.append("")
        distances[i][2 ** i] = 0
        priority_queue.append([i, 2 ** i])
    for k, v in graph.items():
        names[v[0]] = k
    # do the job
    while True:
        if len(priority_queue) == 0:
            break
        popped = priority_queue.pop()
        current_node, mask = popped
        # get all neighbours of current node
        neighbours = graph.get(names[current_node], [0, []])[1]
        for neighbour in neighbours:
            add = neighbour[1]
            neighbour_id = names.index(neighbour[0])
            if distances[neighbour_id][mask | 2 ** neighbour_id] > distances[current_node][mask] + add:
                priority_queue = [[neighbour_id, mask | 2 ** neighbour_id]] + priority_queue
                distances[neighbour_id][mask | 2 ** neighbour_id] = distances[current_node][mask] + add
    answer = max_distance
    for i in range(len(graph)):
        answer = min(answer, distances[i][2 ** len(graph) - 1])
    return answer


def main(my_file):
    graph = get_graph_from_data(my_file)
    print(dijkstra(graph))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "09_input.txt"
    main(filename)
