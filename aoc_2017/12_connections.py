import sys


def get_data(my_file):
    connections = dict()
    with open(my_file) as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip().split("<->")
            connections[int(line[0])] = set(map(int, line[1].split(",")))
    return connections


def get_group(connections, program):
    my_connections = {program}
    queue = [program]
    while True:
        if len(queue) == 0:
            break
        current = queue.pop()
        neighbours = connections[current]
        for neighbour in neighbours:
            if neighbour not in my_connections:
                queue.append(neighbour)
                my_connections.add(neighbour)
    return my_connections


def main(my_file):
    connections = get_data(my_file)
    my_connections = get_group(connections, 0)
    print("part 1:", len(my_connections))
    programs = set(connections.keys()).copy()
    groups = 1
    while True:
        programs = programs.difference(my_connections)
        if len(programs) == 0:
            break
        program = programs.pop()
        my_connections = get_group(connections, program)
        groups += 1
    print("part 2:", groups)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "12_input.txt"
    main(filename)
