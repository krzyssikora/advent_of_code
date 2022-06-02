import sys


def get_cavern(my_file):
    with open(my_file) as f:
        lines = f.readlines()

    free_spots = set()
    units = dict()
    elves = dict()
    goblins = dict()
    row = 0

    for line in lines:
        column = 0
        for char in line.strip():
            if char == '.':
                free_spots.add((row, column))
            elif char == 'E':
                units[(row, column)] = ['E', 3, 200]  # species, attack power, hit points
                elves[(row, column)] = [3, 200]
            elif char == 'G':
                units[(row, column)] = ['G', 3, 200]  # species, attack power, hit points
                goblins[(row, column)] = [3, 200]
            column += 1
        row += 1

    max_row = max(max(iterab, key=lambda x: x[0])[0] for iterab in [free_spots, units]) + 2
    max_column = max(max(iterab, key=lambda x: x[1])[1] for iterab in [free_spots, units]) + 2

    return free_spots, units, elves, goblins, max_row, max_column


def display_cavern(free_spots: set, units: dict, rows, columns):
    for row in range(rows):
        for column in range(columns):
            pos = (row, column)
            if pos in free_spots:
                print(".", end="")
            elif pos in units:
                print(units[pos][0], end="")
            else:
                print("#", end="")
        print()
    print()


def get_targets(units, current_unit_coordinates):
    targets = set()
    current_type = units[current_unit_coordinates][0]

    for unit in units:
        if units[unit][0] == current_type:
            continue
        else:
            targets.add(unit)

    return targets


def get_range(free_spots, targets, my_spot):
    targets_range = set()
    for target in targets:
        row, column = target
        for x in {(row - 1, column), (row + 1, column), (row, column - 1), (row, column + 1)}:
            if x == my_spot:
                return None
            if x in free_spots:
                targets_range.add(x)
    return targets_range


def get_distances(current_position, free_spots):
    distances = {current_position: 0}
    queue = [current_position]
    while True:
        if len(queue) == 0:
            break
        current_position = queue.pop()
        row, column = current_position
        neighbours = {(row - 1, column),
                      (row + 1, column),
                      (row, column - 1),
                      (row, column + 1)}.intersection(free_spots)
        for neighbour in neighbours:
            if neighbour not in distances or distances[neighbour] > distances[current_position] + 1:
                distances[neighbour] = distances[current_position] + 1
                queue.append(neighbour)
    return distances


def get_positions_within_steps(current_position, free_spots, steps):
    positions = list()
    distances = get_distances(current_position, free_spots)
    for coordinates, distance in distances.items():
        if distance == steps:
            positions.append(coordinates)
    positions.sort()
    positions.sort(key=lambda x: x[1])
    return positions


def make_move(free_spots, elves, goblins, targets_range, unit):
    # firstly determine, which of the positions in targets_range can be reached in the fewest steps
    distances = get_distances(unit, free_spots)
    min_dist = 1000
    closest_positions = set()

    for coordinates, dist in distances.items():
        if coordinates in targets_range:
            if dist == min_dist:
                closest_positions.add(coordinates)
            elif dist < min_dist:
                closest_positions = {coordinates}
                min_dist = dist

    closest_positions = list(closest_positions)
    closest_positions.sort()
    closest_positions.sort(key=lambda x: x[1])
    if closest_positions:
        closest_position = closest_positions[0]
    else:
        return

    # make single step towards closest position
    position = None, None
    if min_dist > 1:
        positions = get_positions_within_steps(closest_position, free_spots, min_dist - 1)
        for position in positions:
            if abs(position[0] - unit[0]) + abs(position[1] - unit[1]) == 1:
                break
    else:
        position = closest_position

    # move unit to position
    if unit in elves:
        units_values = elves.pop(unit)
        elves[position] = units_values
    else:
        units_values = goblins.pop(unit)
        goblins[position] = units_values

    if unit in targets_range:
        targets_range = None
    return free_spots, elves, goblins, targets_range


def attack(free_spots, units, elves, goblins, unit):
    # TODO finish it
    return free_spots, units, elves, goblins


def make_single_units_turn(free_spots, units, elves, goblins, unit):
    # targets = get_targets(units, unit)
    targets = elves if unit in goblins else goblins
    targets_range = get_range(free_spots, targets, unit)
    if targets_range:
        # find a place to move firstly
        free_spots, elves, goblins, targets_range = make_move(free_spots, elves, goblins, targets_range, unit)
    if targets_range is None:
        # unit is in target's range, attack
        free_spots, units, elves, goblins = attack(free_spots, units, elves, goblins, unit)
    return free_spots, units, elves, goblins


def make_round(free_spots, units, elves, goblins):
    ordered_units = list(units.keys())
    # alternatively:
    # ordered_units = list(elves.keys()) + list(goblins.keys())
    ordered_units.sort()
    ordered_units.sort(key=lambda x: x[1])
    for unit in ordered_units:
        pass
        free_spots, units, elves, goblins = make_single_units_turn(free_spots, units, elves, goblins, unit)
    return free_spots, units, elves, goblins


def battle(free_spots, units, elves, goblins):
    while True:
        free_spots, units, elves, goblins = make_round(free_spots, units, elves, goblins)
        # stop when units of one type left
        # TODO finish it


def main(my_file):
    free_spots, units, elves, goblins, max_row, max_column = get_cavern(my_file)
    display_cavern(free_spots, units, max_row, max_column)
    # battle(free_spots, units, elves, goblins)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "15_input.txt"
    main(filename)
