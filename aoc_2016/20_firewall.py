import sys


def get_ranges(my_file):
    ranges = list()
    with open(my_file) as f:
        lines = f.readlines()
        for line in lines:
            ranges.append(list(map(int, line.strip().split("-"))))
    return sorted(ranges)


def close_range(ranges, value):
    first = 0
    last = len(ranges) - 1
    while True:
        middle = (first + last) // 2
        middle_range = ranges[middle]
        if middle_range[0] <= value <= middle_range[1]:
            return middle
        if first == middle == last:
            return None
        if value < middle_range[0]:
            last = middle
        else:
            first = middle + 1


def remove_range(ranges, new_range):
    lower_range, upper_range = None, None
    lower = close_range(ranges, new_range[0])
    upper = close_range(ranges, new_range[1])
    if lower is None and upper is None:
        return ranges
    if lower == upper:
        removed_range = ranges.pop(lower)
        if removed_range[0] < new_range[0]:
            ranges.append([removed_range[0], new_range[0] - 1])
        if new_range[1] + 1 < removed_range[1]:
            ranges.append([new_range[1] + 1, removed_range[1]])
    else:
        if upper is not None:
            upper_range = ranges[upper]
        if lower is not None:
            lower_range = ranges[lower]
        ranges = ranges[:lower] + ranges[upper + 1:]
        if lower is not None and lower_range[0] <= new_range[0] - 1:
            ranges.pop(lower)
            ranges.append([lower_range[0], new_range[0] - 1])
        if upper is not None and new_range[1] + 1 <= upper_range[1]:
            ranges.pop(upper)
            ranges.append([new_range[1] + 1, upper_range[1]])
    ranges.sort()
    return ranges


def main(my_file):
    ranges_to_clean = get_ranges(my_file)
    ranges = [[0, 4294967295]]
    for rng in ranges_to_clean:
        ranges = remove_range(ranges, rng)
    print("part 1:", ranges[0][0])
    total = 0
    for rng in ranges:
        total += rng[1] - rng[0] + 1
    print("part 2:", total)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "20_input.txt"
    main(filename)
