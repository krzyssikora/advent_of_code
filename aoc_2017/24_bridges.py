import sys


def get_components(my_file):
    components = set()
    with open(my_file) as f:
        lines = f.readlines()
    for line in lines:
        components.add(tuple(map(int, line.strip().split("/"))))
    return components


def get_neighbours(components, value):
    neighbours = set()
    for component in components:
        if value in component:
            neighbours.add(component)
    return neighbours


def make_bridges(bridges, current_bridge, current_value, components_left):
    neighbours = get_neighbours(components_left.copy(), current_value)
    if len(neighbours) == 0:
        bridges.append(current_bridge)
    else:
        for neighbour in neighbours:
            new_bridge = current_bridge.copy()
            new_bridge.append(neighbour)
            bridges = make_bridges(bridges, new_bridge, sum(neighbour) - current_value,
                                   components_left.difference({neighbour}))
    return bridges


def main(my_file):
    components = get_components(my_file)
    bridges = make_bridges(list(), list(), 0, components)
    maximum_strength = 0
    max_length = len(max(bridges, key=len))
    part_two_choices = list()
    for bridge in bridges:
        new_sum = sum([sum(x) for x in bridge])
        if new_sum > maximum_strength:
            maximum_strength = new_sum
        if len(bridge) == max_length:
            part_two_choices.append((bridge, new_sum))
    print("part 1:", maximum_strength)
    print("part 2:", max(part_two_choices, key=lambda x: x[1])[1])


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "24_input.txt"
    main(filename)
