import sys


def make_step(circular_list, step, initial_pos, skip_size):
    """
    initial_pos (int): indicates the position of initial element, as the current is placed at 0
    """
    # reverse the part from current (0), of length = length
    if step > 1:
        circular_list = circular_list[step - 1::-1] + circular_list[step:]
    # shift current to 0; current = initial_pos + skip_size
    cut_pos = (step + skip_size) % len(circular_list)
    circular_list = circular_list[cut_pos:] + circular_list[:cut_pos]
    initial_pos = (initial_pos - cut_pos) % len(circular_list)
    return circular_list, initial_pos


def part_1(my_file):
    with open(my_file) as f:
        steps = list(map(int, f.read().strip().split(",")))
    if "input" in my_file:
        length = 256
    else:
        length = 5
    circular_list = [_ for _ in range(length)]
    initial_pos = 0
    skip = 0
    for step in steps:
        circular_list, initial_pos = make_step(circular_list, step, initial_pos, skip)
        skip += 1
    circular_list = circular_list[initial_pos:] + circular_list[:initial_pos]
    return circular_list[0] * circular_list[1]


def part_2(my_file):
    steps = list()
    with open(my_file) as f:
        inp = f.read().strip()
    # inp = my_file
    for char in inp:
        steps.append(ord(char))
    steps += [17, 31, 73, 47, 23]
    circular_list = [_ for _ in range(256)]
    initial_pos = 0
    skip = 0
    for _ in range(64):
        for step in steps:
            circular_list, initial_pos = make_step(circular_list, step, initial_pos, skip)
            skip += 1
    circular_list = circular_list[initial_pos:] + circular_list[:initial_pos]
    bits = list()
    for i in range(16):
        bit = circular_list[16 * i]
        for j in range(1, 16):
            bit = bit ^ circular_list[16 * i + j]
        bits.append(bit)
    knot_hash = ""
    for bit in bits:
        hx = hex(bit)[2:]
        if len(hx) == 1:
            hx = "0" + hx
        knot_hash += hx
    return knot_hash


def main(my_file):
    print("part 1:", part_1(my_file))
    print("part 2:", part_2(my_file))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "10_input.txt"
    main(filename)
