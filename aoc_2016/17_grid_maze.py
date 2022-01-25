import hashlib


def new_directions(code, coordinates):
    ret = list()
    x, y = coordinates
    code_hash = hashlib.md5(code.encode()).hexdigest()[:4]
    for direction, char in zip("UDLR", code_hash):
        if char in {"b", "c", "d", "e", "f"}:
            if (direction == "U" and y > 0) or \
                    (direction == "D" and y < 3) or \
                    (direction == "L" and x > 0) or \
                    (direction == "R" and x < 3):
                ret.append(direction)
    return ret


def shortest_path(initial_coordinates, code, final_coordinates):
    def new_coordinates(old_coordinates, new_direction):
        x, y = old_coordinates
        if new_direction == "U":
            return x, y - 1
        elif new_direction == "D":
            return x, y + 1
        elif new_direction == "L":
            return x - 1, y
        elif new_direction == "R":
            return x + 1, y
        else:
            return None

    ret = list()
    queue = [(initial_coordinates, [])]
    while queue:
        current_coordinates, current_directions = queue.pop(0)
        current_code = code + "".join(current_directions)
        directions = new_directions(current_code, current_coordinates)
        for direction in directions:
            neighbour_coordinates = new_coordinates(current_coordinates, direction)
            if neighbour_coordinates == final_coordinates:
                ret.append((current_directions + [direction]))
            else:
                queue.append((neighbour_coordinates, current_directions + [direction]))
    return ret


def main():
    passcode = "udskfozm"
    sp = shortest_path((0, 0), passcode, (3, 3))
    print("part 1: " + "".join(min(sp, key=len)))
    print("part 2:", len(max(sp, key=len)))


if __name__ == "__main__":
    main()
