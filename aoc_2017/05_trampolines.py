import sys


def get_data(my_file):
    jumps = list()
    with open(my_file) as f:
        lines = f.readlines()
        for line in lines:
            jumps.append(int(line.strip()))
    return jumps


def jump(jumps, part):
    counts = 0
    idx = 0
    length = len(jumps)
    while True:
        offset = jumps[idx]
        if part == 2 and offset >= 3:
            jumps[idx] -= 1
        else:
            jumps[idx] += 1
        idx += offset
        counts += 1
        if idx >= length:
            break
    return counts


def main(my_file):
    for part in [1, 2]:
        jumps = get_data(my_file)
        print(f"part {part}:", jump(jumps, part))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "05_input.txt"
    main(filename)
