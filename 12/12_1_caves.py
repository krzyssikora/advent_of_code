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


def make_paths(connections, small_caves, my_path=None, first="start", last="end"):
    global my_paths
    if not my_path:
        my_path = list()
    my_path.append(first)
    for cave in connections.get(first, []):
        if cave == last and my_path + [last] not in my_paths:
            my_paths.append(my_path + [last])
        elif cave not in small_caves or cave not in my_path:
            make_paths(connections, small_caves, my_path, cave, last)
    if my_path[len(my_path) - 1] != last:
        my_path.pop()
    return my_path


def main():
    global my_paths
    my_file = "12_input.txt"
    connections = make_connections_dictionary(make_data_into_list(my_file))
    small_caves = [elt for elt in connections.keys() if elt.lower() == elt]
    make_paths(connections, small_caves)
    print(len(my_paths))


if __name__ == "__main__":
    my_paths = []
    main()
