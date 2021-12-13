import sys


def get_string_from_file(my_file):
    ret_string = ""
    with open(my_file) as f:
        lines = f.readlines()
        for line in lines:
            ret_string += line.strip("\n")
    return ret_string


def get_two_strings_from_file(my_file):
    ret_string_1 = ""
    ret_string_2 = ""
    first = True
    with open(my_file) as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip("\n")
            for elt in line:
                if first:
                    ret_string_1 += elt
                else:
                    ret_string_2 += elt
                first = not first
    return ret_string_1, ret_string_2


def move(pos1, pos2):
    return [pos1[0] + pos2[0], pos1[1] + pos2[1]]


def get_positions_visited(places):
    position = [0, 0]
    visited = [position]
    moves = {">": [1, 0],
             "<": [-1, 0],
             "^": [0, 1],
             "v": [0, -1]
             }
    for elt in places:
        position = move(position, moves.get(elt))
        if position not in visited:
            visited.append(position)
    return visited


def merged_list(list_1, list_2):
    return_list = list()
    for elt in list_1:
        return_list.append(elt)
    for elt in list_2:
        if elt not in return_list:
            return_list.append(elt)
    return return_list


def main(my_file):
    places_for_santa, places_for_robosanta = get_two_strings_from_file(my_file)
    places_santa = get_positions_visited(places_for_santa)
    places_robosanta = get_positions_visited(places_for_robosanta)
    print(len(merged_list(places_santa, places_robosanta)))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "03_input.txt"
    main(filename)
