import sys
import itertools

"""
A graph where vertices are names and edges will have assigned weights 
being sums of changes of happiness between two vertices.
A graph will be implemented as an adjacency list, or more precisely as a dictionary with:
* keys are names of vertices
* values are lists: [vertex, weight]

"""
# TODO: modify Dijkstra's algorithm?


def get_graph(my_file):
    aux_dict = dict()
    with open(my_file) as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip().strip(".").split()
            name_1, name_2 = line[0], line[-1]
            if name_2 < name_1:
                name_1, name_2 = name_2, name_1
            weight = int(line[3]) if line[2] == "gain" else -int(line[3])
            aux_dict[(name_1, name_2)] = aux_dict.get((name_1, name_2), 0) + weight
    graph = dict()
    for (name_1, name_2), weight in aux_dict.items():
        if name_1 in graph:
            graph[name_1].append([name_2, weight])
        else:
            graph[name_1] = [[name_2, weight]]
        if name_2 in graph:
            graph[name_2].append([name_1, weight])
        else:
            graph[name_2] = [[name_1, weight]]
        # graph[name_1] = graph.get(name_1, list()).append([name_2, weight])
        # graph[name_2] = graph.get(name_2, list()).append([name_1, weight])
    return graph


def copy_name(graph, name, alias):
    adj_list = graph[name]
    graph[alias] = list()
    for other_name, weight in adj_list:
        graph[alias].append([other_name, weight])
        graph[other_name].append([alias, weight])
    return graph


"""def change_costs(graph):
    new_graph = dict()
    minimum = maximum = graph[list(graph.keys())[0]][0][1]
    for vertex in graph:
        for other, weight in graph[vertex]:
            if weight > maximum:
                maximum = weight
            if weight < minimum:
                minimum = weight
    maximum += 1
    for vertex in graph:
        new_graph[vertex] = list()
        for other, weight in graph[vertex]:
            new_graph[vertex].append([other, maximum - weight])
    return new_graph, maximum


def dijkstra(graph):
    graph, maximum = change_costs(graph)
    names = list(graph.keys())
    no_names = len(names)
    print("Max:", maximum, maximum * no_names)
    maximum_happiness = maximum * no_names
    previous = dict()
    happiness = list()
    for n in range(no_names):
        single_name_list = list()
        for m in range(2 ** no_names):
            single_name_list.append(maximum_happiness)
        happiness.append(single_name_list)
    queue = list()
    for ind in range(no_names):
        queue.append((ind, 2 ** ind))
        happiness[ind][2 ** ind] = 0
    while True:
        if len(queue) == 0:
            break
        queue.sort(key=lambda x: happiness[x[0]][x[1]])
        current_id, current_mask = queue.pop()
        neighbours = graph[names[current_id]]
        neighbours.sort(key=lambda x: x[1])
        print(names[current_id].ljust(5), neighbours)
        print(" " * 5, end="")
        for q in queue:
            hap = " (" + str(happiness[q[0]][q[1]]) + ")"
            print(names[q[0]].rjust(5) + ":" + str(bin(q[1]))[2:].rjust(4) + hap.ljust(5), end=".")
        print()
        for other_name, weight in neighbours:
            other_id = names.index(other_name)
            if current_mask & 2 ** other_id == 0:
                if happiness[other_id][current_mask | 2 ** other_id] > happiness[current_id][current_mask] + weight:
                    previous[other_name] = names[current_id]
                    queue.append((other_id, current_mask | 2 ** other_id))
                    print(neighbours)
                    print(current_id, current_mask, other_name, happiness[current_id][current_mask], weight)
                    happiness[other_id][current_mask | 2 ** other_id] = happiness[current_id][current_mask] + weight
    answer = min(happiness[ind][2 ** no_names - 1] for ind in range(no_names))
    answer = (no_names - 1) * maximum - answer
    previous_list = list()
    for name in previous:
        previous_list.append((name, previous[name]))
    sitting_list = list()
    name = names[0]
    print("PREV:")
    for p in previous_list:
        print(p)
    while True:
        if len(previous_list) == 0:
            break
        if name not in sitting_list:
            sitting_list.append(name)
        found = False
        for pair in previous_list:
            if pair[0] == name:
                if pair[1] not in sitting_list:
                    name = pair[1]
                found = True
                break
        if found:
            if len(previous_list) == 1:
                sitting_list.append(name)
            previous_list.remove(pair)
        else:
            for pair in previous_list:
                if pair[1] == name:
                    name = pair[0]
                    found = True
                    break
            if found:
                if len(previous_list) == 1:
                    sitting_list.append(name)
                previous_list.remove(pair)
    print("SITTING:", sitting_list, previous_list)
    # time to add connection from last to first
    name = sitting_list[-1]
    other = sitting_list[0]
    adj_list = graph[name]
    for pair in adj_list:
        if pair[0] == other:
            answer += maximum - pair[1]
            break
    return answer, previous, happiness"""


def add_myself(graph):
    for name in graph:
        graph[name].append(["myself", 0])
    adj_list = list()
    for name in list(graph.keys()):
        adj_list.append([name, 0])
    graph["myself"] = adj_list
    return graph


def brut_force(graph):
    names = list(graph.keys())
    names.sort()
    num_names = len(names)
    perms = itertools.permutations(range(1, num_names))
    name = names[0]
    max_happiness = -1000
    for perm in perms:
        current_names = [name]
        happiness = 0
        for i in perm:
            current_names.append(names[i])
        current_names.append(name)
        for i in range(num_names):
            adj_list = graph[current_names[i]]
            for pair in adj_list:
                if pair[0] == current_names[i + 1]:
                    happiness += pair[1]
                    break
        if happiness > max_happiness:
            max_happiness = happiness
            print(current_names, max_happiness)


def main(my_file):
    graph = get_graph(my_file)
    graph = add_myself(graph)
    """for g in graph:
        print(g, ":", graph[g])"""
    brut_force(graph)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "13_input.txt"
    main(filename)
