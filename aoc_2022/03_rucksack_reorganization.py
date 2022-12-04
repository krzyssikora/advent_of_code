import sys
import os


def get_data_lines(my_file):
    with open(my_file) as f:
        lines = f.readlines()
    return [line.strip() for line in lines]


def get_shared_item(line):
    line = line.strip('\n')
    length = len(line) // 2
    left = set(line[:length])
    right = set(line[length:])
    ret_char = ''
    for char in left:
        if char in right:
            ret_char = char
            break
    return ret_char


def get_item_priority(item):
    if ord('a') <= ord(item) <= ord('z'):
        return ord(item) - ord('a') + 1
    elif ord('A') <= ord(item) <= ord('Z'):
        return ord(item) - ord('A') + 27
    else:
        raise ValueError(f'I wanted a letter and i got this: {item}')


def get_sum_of_priorities(lines):
    priorities = [get_item_priority(get_shared_item(line)) for line in lines]
    return sum(priorities)


def get_sum_of_priorities_for_groups_of_three_elves(lines):
    many = len(lines) // 3
    priorities = list()
    for idx in range(many):
        s1 = set(lines[3 * idx])
        s1 = set(lines[3 * idx + 1]).intersection(s1)
        s1 = set(lines[3 * idx + 2]).intersection(s1)
        if len(s1) == 1:
            priorities.append(get_item_priority(s1.pop()))
        else:
            raise ValueError(f'non-unique shared item: {s1}')
    return sum(priorities)


def main(my_file):
    lines = get_data_lines(my_file)

    print("part 1:", get_sum_of_priorities(lines))
    print("part 2:", get_sum_of_priorities_for_groups_of_three_elves(lines))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = f'{os.path.basename(__file__)[:2]}_input.txt'
    main(filename)
