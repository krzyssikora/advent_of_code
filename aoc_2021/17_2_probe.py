import sys
import math
import re


def get_data(my_file):
    with open(my_file) as f:
        line = f.read()
        matches = list(map(int, re.findall(r"([-0-9]+)", line)))
    return matches


def get_number(x_target, y_target):
    y_max = max(abs(y_target[0]), abs(y_target[1]))
    y_min = min(abs(y_target[0]), abs(y_target[1]))
    x_max = max(abs(x_target[0]), abs(x_target[1]))
    x_min = min(abs(x_target[0]), abs(x_target[1]))
    a_number = 0
    n = 0
    velocities = list()
    while True:
        n_number = 1
        y_lower = math.ceil(n / 2 - y_max / (n + 1))
        y_upper = math.floor(n / 2 - y_min / (n + 1))
        x_lower = math.ceil(x_min / (n + 1) + n / 2)
        x_upper = math.floor(x_max / (n + 1) + n / 2)
        if n >= x_upper:
            x_lower, x_upper = 16, 17
        if y_upper >= y_lower:
            n_number *= (y_upper - y_lower + 1)
        else:
            n_number = 0
        if x_upper >= x_lower:
            n_number *= (x_upper - x_lower + 1)
        if n_number > 0:
            for x in range(x_lower, x_upper + 1):
                for y in range(y_lower, y_upper + 1):
                    if (x, y) not in velocities:
                        velocities.append((x, y))
        a_number += n_number
        if y_lower > y_max:
            break
        n += 1
    return a_number, velocities


def main(my_file):
    target = get_data(my_file)
    x_target = target[0:2]
    y_target = target[2:]
    a_number, velocities = get_number(x_target, y_target)
    print(len(velocities))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "17_input.txt"
    main(filename)
