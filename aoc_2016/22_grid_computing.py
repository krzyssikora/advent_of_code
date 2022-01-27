import sys
import re


def get_grid(my_file):
    grid = dict()
    max_x, max_y = 0, 0
    with open(my_file) as f:
        lines = f.readlines()
        for line in lines:
            if "dev/grid" not in line:
                continue
            # x y   Size  Used  Avail  Use%
            values = list(map(int,
                              re.findall(r"x([0-9]+)-y([0-9]+)[ ]+([0-9]+)T[ ]+([0-9]+)T[ ]+([0-9]+)T[ ]+([0-9]+)%",
                                         line)[0]))
            x, y = values[:2]
            if x > max_x:
                max_x = x
            if y > max_y:
                max_y = y
            grid[(values[0], values[1])] = {"size": values[2],
                                            "used": values[3],
                                            "avail": values[4],
                                            "use_perc": values[5]}
    return grid, max_x, max_y


def print_grid(grid, dim_x, dim_y):
    # pat 2 of the puzzle solved by hand with use of the diagram
    # move empty slot 2 in direction x-
    # move empty 22 in direction y-
    # move empty 7 in direction x+
    # move the desired 30 more up, for each 5 moves needed (empty must go up around with each step
    # total = 2 + 22 + 7 + 30 * 5 = 181
    for x in range(dim_x + 1):
        for y in range(dim_y + 1):
            elt = grid[(x, y)]
            elt_str = str(elt["used"]) + "/" + str(elt["size"])
            print(elt_str.rjust(7), end="")
        print()


def viable_pair(node_a, node_b):
    """
    Node A is not empty (its Used is not zero).
    Nodes A and B are not the same node.
    The data on node A (its Used) would fit on node B (its Avail).

    node is a tuple: ((x, y), properties_dict) """
    if node_a[0] == node_b[0]:
        return False
    if node_a[1]["used"] == 0:
        return False
    if node_a[1]["used"] > node_b[1]["avail"]:
        return False
    return True


def viable_pairs(grid, dim_x, dim_y):
    count = 0
    for x in range(dim_x + 1):
        for y in range(dim_y + 1):
            for xx in range(dim_x + 1):
                for yy in range(dim_y + 1):
                    if viable_pair(((x, y), grid[(x, y)]), ((xx, yy), grid[(xx, yy)])):
                        count += 1
    return count


def shortest_path(grid, initial, final):
    pass


def main(my_file):
    grid, dim_x, dim_y = get_grid(my_file)
    print("part 1:", viable_pairs(grid, dim_x, dim_y))
    print("part 2: 181 (see comments in print_grid function)")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "22_input.txt"
    main(filename)
