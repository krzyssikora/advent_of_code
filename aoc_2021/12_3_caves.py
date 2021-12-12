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


def cyclic_paths_dict(connections, small_caves):
    global my_paths
    cyclic = dict()
    for node in connections.keys():
        if node != "start" and node in small_caves:
            my_paths = list()
            make_paths(connections, small_caves, first=node, last=node)
            cyclic[node] = len(my_paths)
    return cyclic


def duplicate_paths(paths, cyclic_dict):
    return_value = 0
    for path in paths:
        return_value += 1
        print("path:", path)
        for node, cycles in cyclic_dict.items():
            if node in path:
                return_value += cycles
                print(str(node) + ": " + str(cycles) + ", ret_value: " + str(return_value))
    return return_value


def main(my_file):
    global my_paths
    connections = make_connections_dictionary(make_data_into_list(my_file))
    # remove options of visiting 'start' and 'end' more than once
    connections.pop("end")
    for value in connections.values():
        if "start" in value:
            value.remove("start")

    small_caves = [elt for elt in connections.keys() if elt.lower() == elt]
    my_cycles = cyclic_paths_dict(connections, small_caves)
    my_paths = []
    make_paths(connections, small_caves)
    print(len(my_paths))
    print(duplicate_paths(my_paths, my_cycles))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        input_file = "12_inp3.txt"
    my_paths = []
    main(input_file)
