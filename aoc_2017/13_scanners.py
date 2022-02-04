import sys


def get_layers(my_file):
    layers = dict()
    with open(my_file) as f:
        lines = f.readlines()
        for line in lines:
            layer_depth, layer_range = list(map(int, line.strip().split(": ")))
            layers[layer_depth] = layer_range
    return layers


def make_step(step, layers, scanners, directions):
    caught = False
    for layer_depth, layer_range in layers.items():
        if step == layer_depth and scanners[layer_depth] == 0:
            caught = True
        scanners[layer_depth] += directions[layer_depth]
        if scanners[layer_depth] in {0, layer_range - 1}:
            directions[layer_depth] *= -1
    return caught, layers, scanners, directions


def display_scanners(layers, scanners):
    max_depth = max(layers.keys())
    max_range = max(layers.values())
    for d in range(max_depth + 1):
        print(" " + str(d).ljust(3), end="")
    print()
    for r in range(max_range):
        for d in range(max_depth + 1):
            if d not in layers:
                if r == 0:
                    print("... ", end="")
                else:
                    print("    ", end="")
            elif scanners[d] == r:
                print("[S] ", end="")
            elif r < layers[d]:
                print("[ ] ", end="")
            else:
                print("    ", end="")
        print()


def main(my_file):
    layers = get_layers(my_file)
    scanners = dict()
    directions = dict()
    for layer in layers:
        scanners[layer] = 0
        directions[layer] = 1
    max_depth = max(layers.keys())
    severity = 0
    for step in range(max_depth + 1):
        caught, layers, scanners, directions = make_step(step, layers, scanners, directions)
        if caught:
            severity += step * layers[step]
    print("part 1:", severity)
    for layer in layers:
        scanners[layer] = 0
        directions[layer] = 1
    delay = 0
    while True:
        caught = False
        for layer_depth, layer_range in layers.items():
            journey = 2 * (layer_range - 1)
            if (delay + layer_depth) % journey == 0:
                caught = True
                break
        if not caught:
            break
        delay += 1
    print("part 2:", delay)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "13_input.txt"
    main(filename)
