import sys
import re
import json


def get_numbers(line):
    p = re.compile("([-0-9]+)")
    positions = list()
    numbers = list()
    for m in p.finditer(line):
        positions.append(int(m.start()))
        numbers.append(int(m.group()))
    return numbers, positions


def red_positions(line):
    p = re.compile("(:\"red\")")
    positions = list()
    for m in p.finditer(line):
        positions.append(int(m.start()))
    return positions


def find_brackets_around(line, position, opening="{", closing="}"):
    left = line.rfind(opening, 0, position)
    right = line.find(closing, left)
    if right < position:
        return -1, -1
    else:
        return left, right


def bracketing(input_string, opening_char="{", closing_char="}"):
    """Creates a list of pairs of positions of opening and closing brackets.

    Args:
        input_string (str): A string to be analyzed.
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
    while True:
        pos = input_string.find(opening_char, pos + 1)
        if pos == -1:
            break
        openings.append(pos)
    while True:
        pos = input_string.find(closing_char, pos + 1)
        if pos == -1:
            break
        closings.append(pos)
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
            if closing - opening == 1:  # do not allow empty brackets
                return None
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


def remove_red_values(line):
    reds = red_positions(line)
    numbers, positions = get_numbers(line)
    brackets = bracketing(line)
    neglected = list()
    for red in reds:
        bracket_index = 0
        while True:
            if bracket_index >= len(brackets):
                break
            bracket_pair = brackets[bracket_index]
            if bracket_pair[0] > red:
                break
            elif bracket_pair[0] < red < bracket_pair[1]:
                if bracket_pair not in neglected:
                    neglected.append((red, bracket_pair[0], bracket_pair[1]))
            bracket_index += 1
    neglected.sort(key=lambda x: x[0])
    # delete outer brackets for the same red
    bracket_index = 0
    while True:
        if bracket_index >= len(neglected):
            break
        tmp_list = list()
        red = neglected[bracket_index][0]
        while bracket_index < len(neglected) and neglected[bracket_index][0] == red:
            tmp_list.append(neglected[bracket_index])
            bracket_index += 1
        if len(tmp_list) > 1:
            tmp_list.sort(key=lambda x: x[1], reverse=True)
            for tmp_bracket in tmp_list[1:]:
                neglected.remove(tmp_bracket)
            bracket_index = 0
    neglected.sort(key=lambda x: x[1])
    bracket_index = 0
    while True:
        if bracket_index >= len(neglected) - 1:
            break
        red_0, pair_0_0, pair_0_1 = neglected[bracket_index]
        red_1, pair_1_0, pair_1_1 = neglected[bracket_index + 1]
        if pair_0_0 == pair_1_0 and pair_0_1 == pair_1_1:
            neglected.pop(bracket_index)
        elif pair_1_1 < pair_0_1 and (red_0 < pair_1_0 or red_0 > pair_1_1):
            neglected.pop(bracket_index + 1)
        else:
            bracket_index += 1
    to_subtract = 0
    for red, left, right in neglected:
        for number, position in zip(numbers, positions):
            if left < position < right:
                to_subtract += number
            elif right < position:
                break
    return sum(numbers) - to_subtract


def my_hook(json_object):
    if "red" in json_object.values():
        return dict()
    else:
        return json_object


def main(my_file):
    with open(my_file) as f:
        line = f.read()
    data = str(json.loads(line, object_hook=my_hook))
    # EITHER
    numbers, positions = get_numbers(data)
    print(sum(numbers))
    # OR
    # print(remove_red_values(line))

if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "12_input.txt"
    main(filename)
