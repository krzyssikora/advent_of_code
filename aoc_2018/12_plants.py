import sys
import re


def get_pots_and_rules(my_file):
    with open(my_file) as f:
        pots = f.readline().strip()[len("initial state: "):]
        f.readline()
        lines = f.readlines()
    rules = dict()
    for line in lines:
        line = line.strip().split(" => ")
        rules[line[0]] = line[1]
    initial_index = pots.find("#")
    pots = pots.strip(".")
    return pots, initial_index, rules


def get_pots_after_generation(pots, initial_index, rules):
    pots = "...." + pots + "...."
    initial_index -= 2
    new_pots = ""
    for i in range(len(pots) - 2):
        new_pots += rules.get(pots[i: i + 5], ".")
    initial_index += new_pots.find("#")
    new_pots = new_pots.strip(".")
    return new_pots, initial_index


def plants_after_generations(pots, initial_index, rules, generations):
    for generation in range(generations):
        pots, initial_index = get_pots_after_generation(pots, initial_index, rules)
    matches = re.finditer("#", pots)
    positions = [initial_index + pos.start() for pos in matches]
    return sum(positions)


def get_number_of_plants(pots, initial_index, rules, generations):
    plants = list()
    for generation in range(generations):
        pots, initial_index = get_pots_after_generation(pots, initial_index, rules)
        matches = re.finditer("#", pots)
        positions = [initial_index + pos.start() for pos in matches]
        plants.append(sum(positions))
    return plants


def part_two(pots, initial_index, rules, generations=50000000000):
    from collections import defaultdict
    # idx       0       1       2       3       ...     98
    # plants    1       2       3       4       ...     99
    # diff      2-1     3-2     4-3             ...     100-99
    plants = get_number_of_plants(pots, initial_index, rules, 1000)
    differences = [plants[i + 1] - plants[i] for i in range(len(plants) - 1)]
    differences_frequencies = defaultdict(int)
    for d in differences:
        differences_frequencies[d] += 1
    ultimate_difference = max(differences_frequencies, key=differences_frequencies.get)
    stable_position = differences.index(ultimate_difference) + 1
    return plants[stable_position - 1] + (generations - stable_position) * ultimate_difference


def main(my_file):
    pots, initial_index, rules = get_pots_and_rules(my_file)
    print("part 1:", plants_after_generations(pots, initial_index, rules, 20))
    print("part 2:", part_two(pots, initial_index, rules))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "12_input.txt"
    main(filename)
