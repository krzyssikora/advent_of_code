#! /usr/bin/env python3
import sys


def find_garbage(data):
    opening = -1
    garbage = list()
    while True:
        opening = data.find("<", opening + 1)
        if opening == -1:
            break
        while True:
            closing = data.find(">", opening + 1)
            exclamation = data.find("!", opening + 1)
            if 0 <= exclamation < closing:
                data = data[:exclamation] + "__" + data[exclamation + 2:]
            else:
                break
        garbage.append((opening, closing))
        opening = closing
    return garbage, data


def bracketing(input_string, garbage_list, opening_char="{", closing_char="}"):
    """Creates a list of pairs of positions of opening and closing brackets.

    Args:
        input_string (str): A string to be analyzed.
        garbage_list (list): A list of tuples: (opening, closing);
            anything between opening and closing should be ignored.
        opening_char (str): A character used for opening bracket.
        closing_char (str): A character used for closing bracket.

    Returns:
        A list of elements: [opening_index, closing_index] of pairs of indexes of opening and closed brackets.
    """
    ret = list()
    openings = list()
    closings = list()
    pos = -1
    # creates lists of positions of opening and closing brackets
    garbage_length = len(garbage_list)
    garbage_pos = 0
    while True:
        pos = input_string.find(opening_char, pos + 1)
        if pos == -1:
            break
        while True:
            if garbage_pos >= garbage_length or pos < garbage_list[garbage_pos][0]:
                openings.append(pos)
                break
            if garbage_list[garbage_pos][0] < pos < garbage_list[garbage_pos][1]:
                break
            garbage_pos += 1
    pos = -1
    garbage_pos = 0
    while True:
        pos = input_string.find(closing_char, pos + 1)
        if pos == -1:
            break
        while True:
            if garbage_pos >= garbage_length or pos < garbage_list[garbage_pos][0]:
                closings.append(pos)
                break
            if garbage_list[garbage_pos][0] < pos < garbage_list[garbage_pos][1]:
                break
            garbage_pos += 1
    if len(openings) != len(closings):
        return None
    ind = 0
    # pairs the brackets, i.e. finds an opening bracket such that the next bracket is a closing one,
    # appends the pair to the final list and removes both brackets from openings / closings
    while True:
        if len(openings) == 0:
            break
        opening = openings[ind]
        closing = input_string.find(closing_char, opening)
        while closing not in closings:
            closing = input_string.find(closing_char, closing + 1)
        if closing < opening:
            return None
        if ind + 1 == len(openings) or openings[ind + 1] > closing:
            # either last opening or next is further than closing
            ret.append([opening, closing])
            openings.remove(opening)
            closings.remove(closing)
            ind -= 1
        else:
            ind += 1
    if len(closings) > 0:
        return None
    ret.sort()
    return ret


def groups_score(groups):
    if len(groups) == 0:
        return 0
    score = 0
    idx = 0
    while True:
        if idx >= len(groups):
            break
        closing = groups[idx][1]
        score += 1
        subgroups = list()
        idx += 1
        while True:
            if idx >= len(groups) or groups[idx][0] > closing:
                break
            subgroups.append(groups[idx])
            idx += 1
        score += groups_score(subgroups) + len(subgroups)
    return score


def garbage_value(data, garbage_list):
    length = 0
    for opening, closing in garbage_list:
        length += closing - opening - 1
    return length - data.count("_")


def main(my_file):
    with open(my_file) as f:
        data = f.read().strip()
    garbage_list, data = find_garbage(data)
    groups = bracketing(data, garbage_list)
    print("part 1:", groups_score(groups))
    print("part 2:", garbage_value(data, garbage_list))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "09_input.txt"
    main(filename)
