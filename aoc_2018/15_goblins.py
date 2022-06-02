import sys


def get_cavern(my_file):
    with open(my_file) as f:
        lines = f.readlines()
    free_spots = set()
    # goblins = dict()
    # elves = dict()
    units = dict()
    row = 0
    for line in lines:
        column = 0
        for char in line.strip():
            if char == ".":
                free_spots.add((row, column))
            elif char in {"E", "G"}:
                units[(row, column)] = [char, 3, 200]  # species, attack power, hit points
            # elif char == "E":
            #     elves[(row, column)] = (3, 200)
            # elif char == "G":
            #     goblins[(row, column)] = (3, 200)
            column += 1
        row += 1
    max_row = max(max(iterab, key=lambda x: x[0])[0] for iterab in [free_spots, units]) + 2
    max_column = max(max(iterab, key=lambda x: x[1])[1] for iterab in [free_spots, units]) + 2
    # return free_spots, elves, goblins, max_row, max_column
    return free_spots, units, max_row, max_column


def display_cavern(free_spots, units, rows, columns):
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


def display_distances(distances, free_spots, units, rows, columns):
    for row in range(rows):
        for column in range(columns):
            pos = (row, column)
            if pos in distances:
                print(str(distances[pos]).center(3), end="")
            elif pos in free_spots:
                print(".".center(3), end="")
            elif pos in units:
                print(units[pos][0].center(3), end="")
            else:
                print("#".center(3), end="")
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
    my_range = set()
    for target in targets:
        row, column = target
        for x in {(row - 1, column), (row + 1, column), (row, column - 1), (row, column + 1)}:
            if x == my_spot:
                return None
            if x in free_spots:
                my_range.add(x)
    return my_range


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


def best_step(free_spots, current_range, current_coordinates):
    # 1. find positions from current_range with the smallest distance from current_coordinates
    # 2. choose the first one in the reading order (top row, leftmost)
    # 3. choose the first step in the reading order from all shortest paths
    # 4. make the step
    distances = get_distances(current_coordinates, free_spots)
    min_distance = distances[min(distances, key=lambda x: distances[x] if x in current_range else 1000)]
    closest_positions = sorted([x for x in distances if distances[x] == min_distance and x in current_range])
    if closest_positions:
        closest_position = closest_positions[0]
    else:
        return None
    # closest_position is the aim (so that we are done with 1 and 2),
    # now we have to find the path towards the aim
    min_distance -= 1
    previous_positions = {closest_position}
    new_positions = set()
    while True:
        if min_distance == 0:
            break
        for row, column in previous_positions:
            for r, c in {(row - 1, column),
                         (row + 1, column),
                         (row, column - 1),
                         (row, column + 1)}:
                if distances.get((r, c), None) == min_distance:
                    new_positions.add((r, c))
        previous_positions = new_positions.copy()
        new_positions = set()
        min_distance -= 1
    previous_positions = sorted(list(previous_positions))
    return previous_positions[0]


def battle_round(free_spots, units, goblins, elves, max_row, max_column):
    def attack(current_coordinates):
        nonlocal elves, goblins
        print("ATTACK")
        cr, cc = current_coordinates
        c_targets = list()
        for r, c in {(cr - 1, cc),
                     (cr + 1, cc),
                     (cr, cc - 1),
                     (cr, cc + 1)}:
            if (r, c) in units and units[(r, c)][0] != current_type:
                c_targets.append((r, c))
        if c_targets:
            c_targets.sort(reverse=True)
            r, c = c_targets.pop()
            units[(r, c)][2] -= current_unit[1]
            if units[(r, c)][2] <= 0:
                # target destroyed
                units.pop((r, c))
                if (r, c) in units_round:
                    units_round.remove((r, c))
                free_spots.add((r, c))
                if current_type == "G":
                    elves -= 1
                else:
                    goblins -= 1
    units_round = sorted(list(units.keys()).copy(), reverse=True)
    while True:
        print("units left in this round:", len(units_round), units.get((4, 5), None))
        if len(units_round) == 0:
            break
        current_unit_coordinates = units_round.pop()
        current_unit = units[current_unit_coordinates]
        current_type = current_unit[0]
        targets = get_targets(units, current_unit_coordinates)
        current_range = get_range(free_spots, targets, current_unit_coordinates)
        print("current unit:")
        print("    type:        ", current_unit[0])
        print("    position:    ", current_unit_coordinates)
        print("    attack / hit:", current_unit[1], current_unit[2])
        print("    range:       ", current_range)
        print("current range size:", len(current_range) if current_range is not None else -1)
        if current_range is None:
            # If the unit is already in range of a target, it does not move, but continues its turn with an attack.
            # To attack, the unit first determines all of the targets that are in range of it by being
            # immediately adjacent to it. If there are no such targets, the unit ends its turn.
            # Otherwise, the adjacent target with the fewest hit points is selected; in a tie,
            # the adjacent target with the fewest hit points which is first in reading order is selected.
            # TODO: After moving (or if the unit began its turn in range of a target), the unit attacks.
            attack(current_unit_coordinates)
        elif len(current_range) > 0:
            next_step = best_step(free_spots, current_range, current_unit_coordinates)
            if next_step:
                print("MOVE to", next_step)
                free_spots.remove(next_step)
                units.pop(current_unit_coordinates)
                units[next_step] = current_unit
                free_spots.add(current_unit_coordinates)
                current_unit_coordinates = next_step
                attack(current_unit_coordinates)
                display_cavern(free_spots, units, max_row, max_column)
                a = input()
    print(units)
    return free_spots, units, goblins, elves


def battle(free_spots, units, max_row, max_column):
    display_cavern(free_spots, units, max_row, max_column)
    goblins = len([x for x in units.values() if x[0] == "G"])
    elves = len([x for x in units.values() if x[0] == "E"])
    rounds = 0
    while True:
        rounds += 1
        print("N E W   R O U N D:", rounds)
        free_spots, units, goblins, elves = battle_round(free_spots, units, goblins, elves, max_row, max_column)
        if elves == 0 or goblins == 0:
            break
    print("rounds:    ", rounds)
    hit_points = sum([x[2] for x in units.values()])
    print("hit points:", hit_points)
    print("outcome:   ", rounds * hit_points)


def main(my_file):
    free_spots, units, max_row, max_column = get_cavern(my_file)
    battle(free_spots, units, max_row, max_column)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "15_input.txt"
    main(filename)
