import sys
import re


def get_points(my_file):
    pattern = r"(-?\d+)"
    with open(my_file) as f:
        lines = f.readlines()
    points = list()
    for line in lines:
        data = re.findall(pattern, line)
        points.append(tuple(map(int, data)))
    return points


def find_vertical_min_distance(points, start, stop, jump=1):
    minimum = 10 ** 10
    idx = -1
    for i in range(start, stop, jump):
        vertical_distance = max(y + i * y_v for x, y, x_v, y_v in points) - \
                            min(y + i * y_v for x, y, x_v, y_v in points)
        if vertical_distance < minimum:
            minimum = vertical_distance
            idx = i
    return idx, minimum


def display_points(points, step):
    import numpy as np
    positions = list()
    for x, y, x_v, y_v in points:
        positions.append((x + step * x_v, y + step * y_v))
    min_x = min(x for x, y in positions)
    min_y = min(y for x, y in positions)
    max_x = max(x for x, y in positions)
    max_y = max(y for x, y in positions)
    range_y, range_x = max_y - min_y + 1, max_x - min_x + 1
    message = np.zeros((range_y, range_x))
    for x, y in positions:
        message[y - min_y, x - min_x] = 1
    for row in range(range_y):
        for column in range(range_x):
            if message[row, column] == 1:
                print("#", end="")
            else:
                print(".", end="")
        print()


def main(my_file):
    points = get_points(my_file)
    step = 10 ** 8
    for lvl in (8, 4, 2):
        step, min_d = find_vertical_min_distance(points, step - 10 ** lvl, step + 10 ** lvl, 10 ** (lvl // 2))
        print(step, min_d)
    step, min_d = find_vertical_min_distance(points, step - 10, step + 10)
    print(step, min_d)
    print("part 1:")
    display_points(points, step)
    print("part 2:", step)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "10_input.txt"
    main(filename)
