import sys
import os


def get_data_lines(my_file: str) -> list:
    with open(my_file) as f:
        lines = f.readlines()
    return [line.strip('\n').strip() for line in lines]


def get_cubes(lines: list):
    return [tuple(map(int, line.split(','))) for line in lines]


def get_number_of_connections(values: list):
    """
    Args:
        values: sorted list of coordinates like 1, 2, 3, 7, 8, 11, 14, 15, 16, 17, 20

    Returns:
        number of connections, in the above example it would be 6:
        1-2-3 (2)
        7-8 (1)
        14-15-16-17 (3)
    """
    return sum((1 if values[idx + 1] - values[idx] == 1 else 0) for idx in range(len(values) - 1))


def get_inner_values(values: list):
    """
    Args:
        values: sorted list of coordinates like 1, 2, 3, 7, 8, 11, 14, 15, 16, 17, 20

    Returns:
        values between, in the above example these would be: 4, 5, 6, 9, 10, 12, 13, 18, 19
    """
    ret_values = list()
    for idx in range(len(values) - 1):
        if values[idx + 1] - values[idx] > 1:
            ret_values += [i for i in range(values[idx] + 1, values[idx + 1])]
    return ret_values


def get_number_of_connections_along_coordinate(cubes: list, coordinate: int):
    c1, c2 = {0, 1, 2}.difference({coordinate})
    values1 = set(x[c1] for x in cubes)
    values2 = set(x[c2] for x in cubes)
    connections = 0
    for v1 in values1:
        for v2 in values2:
            values3 = list(x[coordinate] for x in cubes if x[c1] == v1 and x[c2] == v2)
            connections += get_number_of_connections(sorted(values3))
    return connections


def get_total_number_of_faces(cubes: list):
    n = len(cubes) * 6
    for i in range(3):
        n -= 2 * get_number_of_connections_along_coordinate(cubes, i)
    return n


def get_potentially_inner_cubes(cubes: list):
    values1 = set(x[1] for x in cubes)
    values2 = set(x[2] for x in cubes)
    potentially_inner_cubes = set()
    for v1 in values1:
        for v2 in values2:
            values0 = list(x[0] for x in cubes if x[1] == v1 and x[2] == v2)
            inner_values0 = get_inner_values(sorted(values0))
            potentially_inner_cubes.update({(v0, v1, v2) for v0 in inner_values0})
    return potentially_inner_cubes


def get_neighbours(current_cube: tuple, cubes: list, visited: set):
    x, y, z = current_cube
    neighbours = {
        (x + 1, y, z),
        (x - 1, y, z),
        (x, y + 1, z),
        (x, y - 1, z),
        (x, y, z + 1),
        (x, y, z - 1),
    }.difference(cubes).difference(visited)
    return list(neighbours)


def get_component(initial_cube: tuple, cubes: list):
    upper_limit = max(max(c[i] for c in cubes) for i in range(3))
    lower_limit = min(min(c[i] for c in cubes) for i in range(3))
    stack = [initial_cube]
    component = set()
    visited = set()
    while True:
        if len(stack) == 0:
            break
        current_cube = stack.pop()
        if any(current_cube[i] <= lower_limit for i in range(3)) or \
                any(current_cube[i] >= upper_limit for i in range(3)):
            # not bounded, so not inner
            return set()
        component.add(current_cube)
        visited.add(current_cube)
        neighbours = get_neighbours(current_cube, cubes, visited)
        for neighbour in neighbours:
            if neighbour not in visited:
                visited.add(neighbour)
                stack.append(neighbour)

    return sorted(list(component))


def get_number_of_visible_faces(cubes: list, total: int):
    potentially_inner_cubes = get_potentially_inner_cubes(cubes)
    components_with_inner_cubes = list()
    while True:
        if len(potentially_inner_cubes) == 0:
            break
        current_cube = tuple(potentially_inner_cubes.pop())
        current_component = get_component(current_cube, cubes)
        if current_component:
            potentially_inner_cubes.difference_update(current_component)
            components_with_inner_cubes.append(current_component)

    for component in components_with_inner_cubes:
        total -= get_total_number_of_faces(component)
    return total


def main(my_file: str) -> None:
    lines = get_data_lines(my_file)
    cubes = get_cubes(lines)

    total = get_total_number_of_faces(cubes)
    print("part 1:", total)

    visible = get_number_of_visible_faces(cubes, total)
    print("part 2:", visible)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = f'{os.path.basename(__file__)[:2]}_input.txt'
    main(filename)
