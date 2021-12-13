import sys


def get_string_from_file(my_file):
    ret_string = ""
    with open(my_file) as f:
        lines = f.readlines()
        for line in lines:
            ret_string += line.strip("\n")
    return ret_string


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


def main(my_file):
    places = get_positions_visited(get_string_from_file(my_file))
    print(len(places))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "03_input.txt"
    main(filename)
