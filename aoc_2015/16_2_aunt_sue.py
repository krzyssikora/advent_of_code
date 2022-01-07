import sys


def get_sues(my_file):
    sues = dict()
    with open(my_file) as f:
        lines = f.readlines()
        for line in lines:
            line_data = line.strip().split()
            sue = dict()
            for i in range(3):
                sue[line_data[2 + 2 * i].strip(":")] = int(line_data[3 + 2 * i].strip(","))
            sues[int(line_data[1].strip(":"))] = sue
    return sues


def compare(sue, real_sue):
    for compound in sue:
        if compound in ["cats", "trees"]:
            if real_sue[compound] >= sue[compound]:
                return False
        elif compound in ["pomeranians", "goldfish"]:
            if real_sue[compound] <= sue[compound]:
                return False
        else:
            if real_sue[compound] != sue[compound]:
                return False
    return True


def main(my_file):
    real_sue = {"children": 3,
                "cats": 7,
                "samoyeds": 2,
                "pomeranians": 3,
                "akitas": 0,
                "vizslas": 0,
                "goldfish": 5,
                "trees": 3,
                "cars": 2,
                "perfumes": 1}
    sues_list = get_sues(my_file)
    for sue in sues_list:
        if compare(sues_list[sue], real_sue):
            print(sue)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "16_input.txt"
    main(filename)
