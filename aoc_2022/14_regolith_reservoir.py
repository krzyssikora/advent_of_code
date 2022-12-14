import sys
import os


def get_data_lines(my_file):
    with open(my_file) as f:
        lines = f.readlines()
    return [line.strip('\n').strip() for line in lines]


def add_line_segment(scan, vertex_1, vertex_2):
    x1, y1 = vertex_1
    x2, y2 = vertex_2

    if x1 == x2:
        if x1 not in scan:
            scan[x1] = set()
        for y in range(min(y1, y2), max(y1, y2) + 1):
            scan[x1].add(y)
    elif y1 == y2:
        for x in range(min(x1, x2), max(x1, x2) + 1):
            if x not in scan:
                scan[x] = set()
            scan[x].add(y1)

    return scan


def display_scan(scan, new_point=None, x_from=470):
    import numpy as np
    max_y = 1
    for k, v in scan.items():
        max_y = max(max_y, max(v) + 1)
    max_x = max(scan.keys()) + 1
    arr = np.zeros((max_y, max_x))
    for row in range(max_y):
        for column in range(max_x):
            if column in scan and row in scan[column]:
                arr[row, column] = 1

    if new_point:
        arr[new_point] = 2

    scan_string = ''
    for row in range(max_y):
        scan_string += str(row).ljust(3)
        for column in range(x_from, max_x):
            val = int(arr[row, column])
            if val == 2:
                scan_string += 'o'
            else:
                scan_string += '#' * val + '.' * (1 - val)
        scan_string += '\n'

    print(scan_string)


def get_polygonal_chain_from_line(line, scan):
    vertices = [tuple(map(int, v.split(','))) for v in line.split(' -> ')]
    for idx in range(len(vertices) - 1):
        vertex_1, vertex_2 = vertices[idx], vertices[idx + 1]
        scan = add_line_segment(scan, vertex_1, vertex_2)
    return scan


def get_scan(lines):
    scan = dict()
    for line in lines:
        scan = get_polygonal_chain_from_line(line, scan)
    return scan


def get_depth_of_fall(scan, sand_x, sand_y):
    if sand_x not in scan:
        return -1  # abyss
    if sand_y in scan[sand_x]:
        return False  # no space
    min_y = min({1000}.union({v for v in scan[sand_x] if v >= sand_y}))
    if min_y == 1000:
        return -1
    if min_y <= sand_y:
        return False
    return min_y - 1


def get_position_of_new_sand_unit(scan):
    sand_x = 500
    sand_y = 0
    while True:
        new_y = get_depth_of_fall(scan, sand_x, sand_y)
        if new_y == -1:
            return False
        if new_y is False:
            break
        sand_y = new_y
        # check left
        new_y = get_depth_of_fall(scan, sand_x - 1, sand_y + 1)
        if new_y == -1:
            return False
        if new_y is False:
            # check right
            new_y = get_depth_of_fall(scan, sand_x + 1, sand_y + 1)
            if new_y == -1:
                return False
            if new_y is False:
                break
            else:
                sand_x += 1
                sand_y = new_y
        else:
            sand_x -= 1
            sand_y = new_y
    return sand_x, sand_y


def pour_sand(scan, steps=0):
    while True:
        position = get_position_of_new_sand_unit(scan)
        if not position:
            break
        steps += 1
        if position == (500, 0):
            break
        column, row = position
        if column not in scan:
            scan[column] = set()
        scan[column].add(row)
    return scan, steps


def main(my_file):
    lines = get_data_lines(my_file)
    scan = get_scan(lines)

    scan, steps = pour_sand(scan)
    print("part 1:", steps)
    max_depth = max([max(scan[x]) for x in scan]) + 2

    for x in range(500 - max_depth - 2, 500 + max_depth + 3):
        if x not in scan:
            scan[x] = set()
        scan[x].add(max_depth)

    scan, steps = pour_sand(scan, steps)
    print("part 2:", steps)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = f'{os.path.basename(__file__)[:2]}_input.txt'
    main(filename)
