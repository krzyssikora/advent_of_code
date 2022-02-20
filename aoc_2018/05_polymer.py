import sys


def get_polymer(my_file):
    with open(my_file) as f:
        polymer = f.read().strip()
    return polymer


def opposite_polarities(polymer):
    opposites = list()
    previous = -2
    for i in range(len(polymer) - 1):
        if abs(ord(polymer[i]) - ord(polymer[i + 1])) == 32 and previous + 1 < i:
            previous = i
            opposites.append(i)
    opposites.sort(reverse=True)
    return opposites


def simplify_polymer(polymer):
    opposites = opposite_polarities(polymer)
    for i in opposites:
        polymer = polymer[:i] + polymer[i + 2:]
    return polymer


def part_1_v0(polymer):
    while True:
        simplified = simplify_polymer(polymer)
        if simplified == polymer:
            break
        polymer = simplified
    return len(polymer)


def part_1(polymer):
    idx = 0
    while True:
        if idx >= len(polymer) - 1:
            break
        if abs(ord(polymer[idx]) - ord(polymer[idx + 1])) == 32:
            polymer = polymer[:idx] + polymer[idx + 2:]
            if idx > 0:
                idx -= 1
        else:
            idx += 1
    return len(polymer)


def part_2(polymer):
    min_length = 11894
    for order in range(65, 91):
        temp_polymer = polymer.replace(chr(order), "").replace(chr(order + 32), "")
        length = part_1(temp_polymer)
        if length < min_length:
            min_length = length
    return min_length


def main(my_file):
    polymer = get_polymer(my_file)
    print("part 1:", part_1(polymer))
    print("part 2:", part_2(polymer))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "05_input.txt"
    main(filename)
