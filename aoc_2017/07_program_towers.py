import sys


def get_data(my_file):
    paths = dict()
    children = list()
    with open(my_file) as f:
        while True:
            line = f.readline().strip()
            if len(line) == 0:
                break
            if "->" in line:
                line, kids = line.split(" -> ")
                kids = kids.split(", ")
                children += kids
            else:
                kids = []
            program, weight = line.split()
            weight = int(weight[1:-1])
            paths[program] = (weight, kids)
    for program in paths:
        if program not in children:
            break
    return paths, program


def append_kids(node, nodes, nodes_left):
    nodes_left.remove(node)
    kids = dict()
    weight = nodes[node][0]
    for kid in nodes[node][1]:
        (kids_weight, descendants), nodes_left = append_kids(kid, nodes, nodes_left)
        weight += kids_weight
        kids[kid] = (kids_weight, descendants)
    return (weight, kids), nodes_left


def make_tree(nodes, bottom):
    # {node: (weight, dict_of_nodes)}
    # where weight is the sum of node's weight and weight of all descendants,
    # and dict_of_nodes contains elements of the same structure
    tree = dict()
    current = bottom
    nodes_left = set(nodes.keys()).copy()
    while True:
        tree[current], nodes_left = append_kids(current, nodes, nodes_left)
        if len(nodes_left) == 0:
            break
    return tree


def display_tree(tree, depth=0):
    for node in tree:
        print(" " * depth, end="")
        w, dct = tree[node]
        print(node + "(" + str(w) + ") ")
        if len(dct) == 0:
            print()
        else:
            display_tree(dct, depth + len(node + str(w)) + 3)


def get_kids_weights(tree, node):
    # returns list of tuples (node_name, its_weight)
    weights = list()
    subtree = tree[node][1]
    for kid in subtree:
        weights.append((kid, subtree[kid][0]))
    return weights


def find_odd_one(tree, node):
    weights = get_kids_weights(tree, node)
    if len(weights) == 0:
        return node, None
    weight = (node, 0)
    if weights[0][1] == weights[1][1]:
        common = weights[0][1]
        for weight in weights:
            if weight[1] != common:
                break
    else:
        if weights[2][1] == weights[0][1]:
            common = weights[0][1]
            weight = weights[1]
        else:
            common = weights[1][1]
            weight = weights[0]
    if common == weight[1]:
        return node, None
    return weight[0], common - weight[1]


def find_wrong_node(tree, node):
    difference = 0
    while True:
        kid, weight_difference = find_odd_one(tree, node)
        if weight_difference is None:
            return node, difference
        tree = {kid: tree[node][1][kid]}
        node, difference = kid, weight_difference


def main(my_file):
    nodes, bottom = get_data(my_file)
    print("part 1:", bottom)
    tree = make_tree(nodes, bottom)
    node, difference = find_wrong_node(tree, bottom)
    print("part 2:", nodes[node][0] + difference)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "07_input.txt"
    main(filename)
