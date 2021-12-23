import math
import sys


def get_data(my_file):
    with open(my_file) as f:
        lines = f.readlines()
    all_numbers = list()
    for line in lines:
        line = line.strip()
        if line != "":
            brackets = bracketing(line)
            opening_position, closing_position = brackets[0]
            brackets.pop(0)
            all_numbers.append(get_number(line, opening_position + 1, brackets))
    return all_numbers


def string_to_snailfish(input_string):
    brackets = bracketing(input_string)
    opening_position, closing_position = brackets[0]
    brackets.pop(0)
    return get_number(input_string, opening_position + 1, brackets)


def bracketing(input_string, opening_char="[", closing_char="]"):
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


def get_number(line, position_from, brackets, parent=None, left=None):
    number = [dict(), left]
    number[0]["parent"] = parent
    # check if left is a regular number
    temp_position = position_from
    while line[temp_position].isdigit():
        temp_position += 1
    if temp_position > position_from:
        number[0]["left"] = [int(line[position_from: temp_position]), True]
    elif line[position_from] != "[":
        print("should be opening square bracket at", position_from)
        quit()
    else:  # another snailfish number starts here
        # find where it ends
        for opening_bracket, closing_bracket in brackets:
            if opening_bracket == position_from:
                # make connections
                brackets.remove([opening_bracket, closing_bracket])
                temp_position = closing_bracket + 1
                number[0]["left"] = get_number(line, position_from + 1, brackets, number, True)
                break
    # now it is time to get the right element
    if line[temp_position] != ",":
        print("Where is the coma?")
        quit()
    position_from = temp_position + 1
    temp_position = position_from
    while line[temp_position].isdigit():
        temp_position += 1
    if temp_position > position_from:
        number[0]["right"] = [int(line[position_from: temp_position]), False]
    elif line[position_from] != "[":
        print("should be opening square bracket at", position_from)
        quit()
    else:  # another snailfish number starts here
        # find where it ends
        for opening_bracket, closing_bracket in brackets:
            if opening_bracket == position_from:
                # make connections
                brackets.remove([opening_bracket, closing_bracket])
                number[0]["right"] = get_number(line, position_from + 1, brackets, number, False)
                break
    return number


def snailfish_string(number):
    if isinstance(number[0], int):  # change to tuple here
        return str(number[0])  # change to tuple here
    else:
        return "[" + snailfish_string(number[0]["left"]) + "," \
               + snailfish_string(number[0]["right"]) + "]"  # change to tuple here


def snailfish_add(number_1, number_2):
    snailfish_sum = [dict(), None]
    snailfish_sum[0]["parent"] = None
    snailfish_sum[0]["left"] = number_1
    number_1[1] = True
    snailfish_sum[0]["right"] = number_2
    number_2[1] = False
    if not isinstance(number_1[0], int):
        number_1[0]["parent"] = snailfish_sum
    if not isinstance(number_2[0], int):
        number_2[0]["parent"] = snailfish_sum
    return snailfish_sum


def snailfish_magnitude(number):
    if isinstance(number[0], int):
        return number[0]
    else:
        return 3 * snailfish_magnitude(number[0]["left"]) + \
               2 * snailfish_magnitude(number[0]["right"])  # change to tuple here


def go_4_deep(number):
    if isinstance(number[0], int):  # change to tuple here
        return -1, ""
    left_value, left_string = go_4_deep(number[0]["left"])
    right_value, right_string = go_4_deep(number[0]["right"])
    if left_value == right_value == -1:
        return 0, ""
    if left_value >= right_value:
        return left_value + 1, "L" + left_string
    else:
        return right_value + 1, "R" + right_string


def find_subnumber_4_deep(number, depth_string):
    return_number = number
    for letter in depth_string:
        if letter == "L":
            return_number = return_number[0]["left"]  # change to tuple here
        elif letter == "R":
            return_number = return_number[0]["right"]  # change to tuple here
    return return_number


def is_left_kid(node):
    return node[1]  # change to tuple here
#    return node["parent"]["left"] == node


def is_right_kid(node):
    return not node[1]  # change to tuple here
#    return node["parent"]["right"] == node


def type_of_kid(node, direction):
    if direction == "left":
        return node[1]
    elif direction == "right":
        return not node[1]
    else:
        print("Habla, habla")
        quit()


def explode(number, subnumber):
    left_regular_number = subnumber[0]["left"][0]  # change to tuple here
    right_regular_number = subnumber[0]["right"][0]  # change to tuple here
    # remove subnumber
    new_leaf = subnumber[0]["parent"]
    temp_node = new_leaf
    if new_leaf[0]["left"] == subnumber:
        new_leaf[0]["left"] = [0, True]  # change to tuple here
        # for left number:
        while temp_node[0]["parent"] is not None and is_left_kid(temp_node):
            temp_node = temp_node[0]["parent"]
        if temp_node[0]["parent"] is not None:
            temp_node = temp_node[0]["parent"]
            if isinstance(temp_node[0]["left"][0], int):  # change to tuple here
                temp_node[0]["left"][0] += left_regular_number  # change to tuple here
#            elif temp_node["parent"] is not None:
            else:
                temp_node = temp_node[0]["left"]
                while not isinstance(temp_node[0]["right"][0], int):  # change to tuple here
                    temp_node = temp_node[0]["right"]
                temp_node[0]["right"][0] += left_regular_number  # change to tuple here
        # for right number:
        temp_node = new_leaf
        if isinstance(temp_node[0]["right"][0], int):  # change to tuple here
            temp_node[0]["right"][0] += right_regular_number  # change to tuple here
        else:
            temp_node = temp_node[0]["right"]
            while not isinstance(temp_node[0]["left"][0], int):  # change to tuple here
                temp_node = temp_node[0]["left"]
            temp_node[0]["left"][0] += right_regular_number  # change to tuple here
    elif new_leaf[0]["right"] == subnumber:
        new_leaf[0]["right"] = [0, False]  # change to tuple here
        # for right number:
        while temp_node[0]["parent"] is not None and is_right_kid(temp_node):
            temp_node = temp_node[0]["parent"]
        if temp_node[0]["parent"] is not None:
            temp_node = temp_node[0]["parent"]
            if isinstance(temp_node[0]["right"][0], int):  # change to tuple here
                temp_node[0]["right"][0] += right_regular_number  # change to tuple here
#            elif temp_node["parent"] is not None:
            else:
                temp_node = temp_node[0]["right"]
                while not isinstance(temp_node[0]["left"][0], int):  # change to tuple here
                    temp_node = temp_node[0]["left"]
                temp_node[0]["left"][0] += right_regular_number  # change to tuple here
        # for left number:
        temp_node = new_leaf
        if isinstance(temp_node[0]["left"][0], int):  # change to tuple here
            temp_node[0]["left"][0] += left_regular_number  # change to tuple here
        else:
            temp_node = temp_node[0]["left"]
            while not isinstance(temp_node[0]["right"][0], int):  # change to tuple here
                temp_node = temp_node[0]["right"]
            temp_node[0]["right"][0] += left_regular_number  # change to tuple here
    return number


def find_ten(number):
    """Finds a node whose child is a leftmost regular number >= 10.

    Returns:
        the node and True for left child / False for right child being >= 10
    """
    left_number = number[0]["left"]
    right_number = number[0]["right"]
    if isinstance(left_number[0], int) and left_number[0] >= 10:  # change to tuple here
        return number, True
    elif not isinstance(left_number[0], int):  # change to tuple here
        nr, left = find_ten(left_number)
        if nr is not None:
            return nr, left
    if isinstance(right_number[0], int) and right_number[0] >= 10:  # change to tuple here
        return number, False
    elif not isinstance(right_number[0], int):  # change to tuple here
        nr, left = find_ten(right_number)
        if nr:
            return nr, left
    return None, False


def split(regular_number):
    left = math.floor(regular_number[0] / 2)
    right = math.ceil(regular_number[0] / 2)
    split_number = [dict(), None]
    split_number[0]["left"] = [left, True]  # change to tuple here
    split_number[0]["right"] = [right, False]  # change to tuple here
    return split_number


def simplify(number):
    not_finished = True
    while not_finished:
        while True:
            depth_value, depth_string = go_4_deep(number)
            if depth_value == 4:
                subnumber = find_subnumber_4_deep(number, depth_string)
                number = explode(number, subnumber)
            else:
                break
        parent, left = find_ten(number)
        if parent is None:
            not_finished = False
        else:
            direction = "left" if left else "right"
            number_to_split = parent[0][direction]
            split_number = split(number_to_split)
            split_number[1] = direction == "left"
            parent[0][direction] = split_number
            split_number[0]["parent"] = parent
    return number


def types_in_number(number):
    print(type(number), type(number[0]))
    if isinstance(number[0], int):
        return None
    else:
        types_in_number(number[0]["left"])
        types_in_number(number[0]["right"])


def main(my_file):
    snailfish_numbers = get_data(my_file)
    im_starting = True
    final_number = None
    for number in snailfish_numbers:
        if im_starting:
            final_number = number
            im_starting = False
        else:
            final_number = snailfish_add(final_number, number)
            final_number = simplify(final_number)
    print(snailfish_magnitude(simplify(final_number)))


if __name__ == "__main__":
    if len(sys.argv) == 2:
        filename = sys.argv[1]
    elif len(sys.argv) == 3:
        filename = ""
    else:
        filename = "18_input.txt"
    main(filename)
