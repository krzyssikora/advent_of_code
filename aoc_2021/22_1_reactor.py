import sys
import re
import numpy as np


def get_reboot_steps(my_file):
    with open(my_file) as f:
        lines = f.readlines()
        reboot_steps = list()
        for line in lines:
            line = line.strip()
            pattern = r"([a-z]+) x=([-0-9]+)..([-0-9]+),y=([-0-9]+)..([-0-9]+),z=([-0-9]+)..([-0-9]+)"
            row = re.findall(pattern, line)[0]
            row = [row[0]] + list(map(int, row[1:]))
            reboot_steps.append(row)
    return reboot_steps


def filter_initial(steps):
    filtered = list()
    for step in steps:
        if any([abs(step[i]) > 50 for i in range(1, 7)]):
            pass
        else:
            filtered.append(step)
    return filtered


def main(my_file):
    reboot_steps = get_reboot_steps(my_file)
    reboot_steps = filter_initial(reboot_steps)
    # -50..50
    #   0..100
    # range(101)
    grid = np.zeros((101, 101, 101))
    for step in reboot_steps:
        operation = 1 if step[0] == "on" else 0
        x_range = range(step[1], step[2] + 1)
        y_range = range(step[3], step[4] + 1)
        z_range = range(step[5], step[6] + 1)
        for x in x_range:
            for y in y_range:
                for z in z_range:
                    grid[x, y, z] = operation
    print(np.sum(grid))


if __name__ == "__main__":
    if len(sys.argv) == 2:
        filename = sys.argv[1]
    elif len(sys.argv) == 3:
        filename = ""
    else:
        filename = "22_input.txt"
    main(filename)
