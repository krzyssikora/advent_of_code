import sys
import os


def get_data_lines(my_file):
    with open(my_file) as f:
        lines = f.readlines()
    return [line.strip('\n').strip() for line in lines]


def get_pairs_and_packets(lines):
    pairs = list()
    packets = list()
    for idx in range((len(lines) + 1) // 3):
        left = eval(lines[3 * idx])
        right = eval(lines[3 * idx + 1])
        pairs.append((left, right))
        packets.append(left)
        packets.append(right)
    return pairs, packets


def is_left_before_right(left, right):
    if type(left) != type(right):
        if isinstance(left, int):
            left = [left]
        else:
            right = [right]
    # same type now
    if isinstance(left, int):
        ret_value = (left <= right) + (left < right)
    elif not left or not right:
        ret_value = (len(left) <= len(right)) + (len(left) < len(right))
    else:
        ret_value = is_left_before_right(left[0], right[0])
        if ret_value == 1:
            ret_value = is_left_before_right(left[1:], right[1:])
    return ret_value


def is_correct_order(pair):
    left, right = pair
    return is_left_before_right(left, right) > 0


def get_sum_of_indexes_of_pairs_in_right_order(pairs):
    total = sum([idx + 1 for idx in range(len(pairs)) if is_correct_order(pairs[idx])])
    return total


def get_distress_signal(packets):
    larger_than_first = list()
    first = [[2]]
    second = [[6]]

    for packet in packets:
        if not is_correct_order((packet, first)):
            larger_than_first.append(packet)
    idx_1 = len(packets) - len(larger_than_first) + 1
    idx_2 = idx_1 + 1

    for packet in larger_than_first:
        if is_correct_order((packet, second)):
            idx_2 += 1

    return idx_1 * idx_2


def main(my_file):
    lines = get_data_lines(my_file)
    pairs, packets = get_pairs_and_packets(lines)

    print("part 1:", get_sum_of_indexes_of_pairs_in_right_order(pairs))
    print("part 2:", get_distress_signal(packets))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = f'{os.path.basename(__file__)[:2]}_input.txt'
    main(filename)
