import sys


class Tree:
    def __init__(self, children_number, metadata_number):
        self.children_number = children_number
        self.metadata_number = metadata_number
        self.children = list()
        self.metadata = list()

    def __str__(self):
        ret = f"children: {self.children_number}, metadata: "
        for d in self.metadata:
            ret += str(d) + "/ "
        ret += "\n"
        for ch in self.children:
            ret += " " + ch.__str__()
        return ret

    def sum_metadata(self):
        total = sum(self.metadata)
        for child in self.children:
            total += child.sum_metadata()
        return total

    def value(self):
        if self.children_number == 0:
            return sum(self.metadata)
        ret = 0
        for val in self.metadata:
            if val <= self.children_number:
                ret += self.children[val - 1].value()
        return ret


def get_data(my_file):
    with open(my_file) as f:
        data = list(map(int, f.read().strip().split()))
    return data


def get_tree(data, idx=0):
    children_number = data[idx]
    metadata_number = data[idx + 1]
    idx += 2
    my_tree = Tree(children_number, metadata_number)
    for _ in range(children_number):
        child_tree, idx = get_tree(data, idx)
        my_tree.children.append(child_tree)
    my_tree.metadata += data[idx: idx + metadata_number]
    idx += metadata_number
    return my_tree, idx


def main(my_file):
    data = get_data(my_file)
    tree, idx = get_tree(data)
    print("part 1:", tree.sum_metadata())
    print("part 2:", tree.value())


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "08_input.txt"
    main(filename)
