import sys


def get_capacities(my_file):
    return sorted([int(line.strip()) for line in open(my_file).readlines()], reverse=True)


def how_many_combinations(capacities, amount):
    options = dict()
    for combination in range(1, 2 ** len(capacities)):
        tmp_list = list()
        for i in range(len(capacities)):
            if 2 ** i & combination:
                tmp_list.append(capacities[i])
        if sum(tmp_list) == amount:
            options[len(tmp_list)] = options.get(len(tmp_list), 0) + 1
    minimum = min(options.keys())
    return options[minimum]


def main(my_file):
    capacities = get_capacities(my_file)
    print(how_many_combinations(capacities, 150))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "17_input.txt"
    main(filename)
