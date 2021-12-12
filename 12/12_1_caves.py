import sys


def make_data_into_list(my_file):
    with open(my_file) as f:
        lines = f.readlines()
        ret_list = list()
        for line in lines:
            line = line.strip("\n")
            ret_list.append(line.split("-"))
    return ret_list


def make_connections_dictionary(data_list):
    # get list of nodes
    nodes = list()
    for line in data_list:
        for elt in line:
            if elt not in nodes:
                nodes.append(elt)
    # get dictionary {node: [connections]}
    connections = dict()
    for node in nodes:
        for line in data_list:
            if node in line:
                neighbours = line.copy()
                neighbours.remove(node)
                connections[node] = connections.get(node, []) + neighbours
    return connections


def make_paths(connections, small_caves, my_paths=None, my_path=None, first="start", last="end"):
    if not my_path:
        my_path = list()
    if not my_paths:
        my_paths = list()
    my_path.append(first)
    for cave in connections.get(first, []):
        if cave == last and my_path + [last] not in my_paths:
            my_paths.append(my_path + [last])
        elif cave not in small_caves or cave not in my_path:
            my_paths = make_paths(connections, small_caves, my_paths, my_path, cave, last)
    if my_path[len(my_path) - 1] != last:
        my_path.pop()
    return my_paths


def main(my_file):
    connections = make_connections_dictionary(make_data_into_list(my_file))
    # remove options of visiting 'start' and 'end' more than once
    connections.pop("end")
    for value in connections.values():
        if "start" in value:
            value.remove("start")

    small_caves = [elt for elt in connections if elt.lower() == elt]
    my_paths = make_paths(connections, small_caves)
    print(len(my_paths))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        input_file = "12_input.txt"
    main(input_file)
