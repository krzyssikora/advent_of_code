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


def get_row(row, string):
    steps = list()
    inp = string + "-" + str(row)
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
    ret_string = ""
    for char in knot_hash:
        ret_string += bin(int(char, 16))[2:].rjust(4)
    ret_string = ret_string.replace(" ", "0")
    return ret_string


def walk_region(rows, visited, x, y):
    max_x = len(rows[0])
    max_y = len(rows)
    if (x, y) in visited:
        return visited
    if rows[y][x] == "0":
        return visited
    visited.add((x, y))
    if x > 0:
        visited = walk_region(rows, visited, x - 1, y)
    if y > 0:
        visited = walk_region(rows, visited, x, y - 1)
    if x < max_x - 1:
        visited = walk_region(rows, visited, x + 1, y)
    if y < max_y - 1:
        visited = walk_region(rows, visited, x, y + 1)
    return visited


def walk_through(rows):
    visited = set()
    n = 0
    for y in range(len(rows)):
        for x in range(len(rows[0])):
            if (x, y) in visited or rows[y][x] == "0":
                continue
            visited = walk_region(rows, visited, x, y)
            n += 1
    return n


def main():
    total = 0
    string = "oundnydw"
    rows = list()
    for row in range(128):
        row_string = get_row(row, string)
        rows.append(row_string)
        total += sum(list(map(int, row_string)))
    print("part 1:", total)
    print("part 2:", walk_through(rows))


if __name__ == "__main__":
    main()
