import sys
import os
import re


def get_data_lines(my_file):
    with open(my_file) as f:
        lines = f.readlines()
    return [line.strip('\n').strip() for line in lines]


def one_range_contains_the_other(line):
    pattern = re.compile(r'(\d+)-(\d+),(\d+)-(\d+)')
    a, b, c, d = map(int, re.findall(pattern, line)[0])

    return (a <= c and b >= d) or (a >= c and b <= d)


def get_number_of_pairs_with_one_containing_the_other(lines):
    return sum([1 if one_range_contains_the_other(line) else 0 for line in lines])


def one_range_overlaps_the_other(line):
    ranges = line.split(',')
    sections = list()
    for r in ranges:
        start, end = list(map(int, r.split('-')))
        sections += [start, end]

    a, b, c, d = sections

    return (a <= c <= b) or\
           (a <= d <= b) or \
           (c <= a <= d) or \
           (c <= b <= d)


def get_number_of_overlapping_pairs(lines):
    return sum([1 if one_range_overlaps_the_other(line) else 0 for line in lines])


def main(my_file):
    lines = get_data_lines(my_file)

    print("part 1:", get_number_of_pairs_with_one_containing_the_other(lines))
    print("part 2:", get_number_of_overlapping_pairs(lines))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = f'{os.path.basename(__file__)[:2]}_input.txt'
    main(filename)
