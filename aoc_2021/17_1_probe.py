import sys
import math


def get_data(my_file):
    with open(my_file) as f:
        line = f.read()
        matches = list(map(int, re.findall(r"([-0-9]+)", line)))
    return matches


def get_max_height(y_target):
    n_max = max(abs(y_target[0]), abs(y_target[1]))
    n_min = min(abs(y_target[0]), abs(y_target[1]))
    y_max = 0
    n = 0
    while True:
        y_lower = math.ceil(n / 2 - n_max / (n + 1))
        y_upper = math.floor(n / 2 - n_min / (n + 1))
        if y_upper >= y_lower and y_upper > y_max:
            y_max = y_upper
        if y_lower > n_max:
            break
        n += 1
    return y_max * (y_max + 1) // 2


def main(my_file):
    target = get_data(my_file)
    # x_target = target[0:2]
    y_target = target[2:]
    print(get_max_height(y_target))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "17_input.txt"
    main(filename)
