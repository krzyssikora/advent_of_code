import sys
import re


def get_reboot_steps(my_file):
    with open(my_file) as f:
        lines = f.readlines()
        reboot_steps = list()
        for line in lines:
            line = line.strip()
            pattern = r"([a-z]+) x=([-0-9]+)..([-0-9]+),y=([-0-9]+)..([-0-9]+),z=([-0-9]+)..([-0-9]+)"
            row = re.findall(pattern, line)[0]
            row = list(map(int, row[1:])) + [row[0]]
            for i in {1, 3, 5}:
                row[i] += 1
            reboot_steps.append(row)
    return reboot_steps


def intersect_ranges(a1, b1, a2, b2):
    return a2 < b1 and a1 < b2


def intersect_steps(step_1, step_2):
    return intersect_ranges(step_1[0], step_1[1], step_2[0], step_2[1]) and \
           intersect_ranges(step_1[2], step_1[3], step_2[2], step_2[3]) and \
           intersect_ranges(step_1[4], step_1[5], step_2[4], step_2[5])


def is_empty(step):
    x1, x2, y1, y2, z1, z2, op = step
    return x1 == x2 or y1 == y2 or z1 == z2


def subtract_steps(step_1, step_2):
    if not intersect_steps(step_1, step_2):
        return [step_1]
    x11, x12, y11, y12, z11, z12, op1 = step_1
    x21, x22, y21, y22, z21, z22, op2 = step_2
    # cut step_2 to boundaries of step_1
    x21, y21, z21 = max(x11, x21), max(y11, y21), max(z11, z21)
    x22, y22, z22 = min(x12, x22), min(y12, y22), min(z12, z22)
    steps = [
        [x11, x12, y11, y12, z11, z21, op1],
        [x11, x12, y11, y12, z22, z12, op1],
        [x11, x22, y11, y21, z21, z22, op1],
        [x22, x12, y11, y22, z21, z22, op1],
        [x21, x12, y22, y12, z21, z22, op1],
        [x11, x21, y21, y12, z21, z22, op1]
    ]
    return_steps = [step for step in steps if not is_empty(step)]
    return return_steps


def arrange_steps(steps):
    arranged_steps = list()
    which = 0
    for step in steps:
        which += 1
        print("step:", which, "/", len(steps))
        if len(arranged_steps) == 0:
            arranged_steps.append(step)
        else:
            new_steps = [step]
            new_differences = list()
            for ok_step in arranged_steps:
                for tmp_step in new_steps:
                    step_diff = subtract_steps(tmp_step, ok_step)
                    if step_diff not in new_differences:
                        new_differences += step_diff
                new_steps = list()
                for elt in new_differences:
                    if elt not in new_steps:
                        new_steps.append(elt)
                if len(new_differences) == 0:
                    break
                new_differences = list()
            for elt in new_steps:
                if elt not in arranged_steps:
                    arranged_steps.append(elt)
    return arranged_steps


def size(step):
    return (step[1] - step[0]) * (step[3] - step[2]) * (step[5] - step[4])


def total_size(steps):
    total = 0
    for step in steps:
        if step[6] == "on":
            total += size(step)
    return total


def main(my_file):
    reboot_steps = get_reboot_steps(my_file)
    reboot_steps.reverse()
    arranged = arrange_steps(reboot_steps)
    print(total_size(arranged))


if __name__ == "__main__":
    if len(sys.argv) == 2:
        filename = sys.argv[1]
    elif len(sys.argv) == 3:
        filename = ""
    else:
        filename = "22_input.txt"
    main(filename)
