import sys


def make_step(step, x, y, maximum=0):
    distances = {"n": (0, 1),
                 "ne": (0.5, 0.5),
                 "se": (0.5, -0.5),
                 "s": (0, -1),
                 "sw": (-0.5, -0.5),
                 "nw": (-0.5, 0.5)}
    dx, dy = distances[step]
    x += dx
    y += dy
    distance = abs(x) + abs(y)
    if distance > maximum:
        maximum = distance
    return x, y, maximum


def main(my_file):
    with open(my_file) as f:
        data = f.read().strip().split(",")
    x, y, maximum = 0, 0, 0
    for step in data:
        x, y, maximum = make_step(step, x, y, maximum)
    print("part 1:", abs(x) + abs(y))
    print("part 2:", maximum)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "11_input.txt"
    main(filename)
