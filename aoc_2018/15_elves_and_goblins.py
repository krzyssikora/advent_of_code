import os
import sys
import msvcrt as m

cavern_strings = list()

def take_char():  # works on windows only
    a = ord(m.getch())
    if a == 224:
        b = ord(m.getch())
    elif a == 0:
        b = ord(m.getch())
    else:
        b = -1
    return a, b


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
                elves[(row, column)] = [3, 200]  # attack power, hit points
            elif char == 'G':
                units[(row, column)] = ['G', 3, 200]  # species, attack power, hit points
                goblins[(row, column)] = [3, 200]  # attack power, hit points
            column += 1
        row += 1

    max_row = max(max(iterab, key=lambda x: x[0])[0] for iterab in [free_spots, units]) + 2
    max_column = max(max(iterab, key=lambda x: x[1])[1] for iterab in [free_spots, units]) + 2

    return free_spots, units, elves, goblins, max_row, max_column


def logger(*args):
    return
    log_output = ''
    for arg in args:
        log_output += str(arg) + ' '
    print(log_output)


def display_cavern_1(free_spots: set, units: dict, rows, columns):
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


def display_cavern_2(free_spots: set, units: dict, elves: dict, goblins: dict, rows, columns):
    for row in range(rows):
        info_string = ''
        for column in range(columns):
            pos = (row, column)
            if pos in free_spots:
                print(".", end="")
            elif pos in units:
                info_string += ' {}({}/{}),'.format(units[pos][0], units[pos][2],
                                                    elves[pos][1] if units[pos][0] == 'E' else goblins[pos][1])
                print(units[pos][0], end="")
            else:
                print("#", end="")
        print(info_string[:-1])
    print()


def display_cavern(free_spots: set, units: dict, elves: dict, goblins: dict, rows, columns, rounds=None):
    cavern_string = 'rounds completed: {}'.format(rounds) if rounds is not None else ''
    cavern_string += '\n'
    cavern_string += 'elves:' + str(len(elves)).rjust(5) + ', goblins:' + str(len(goblins)).rjust(5) + '\n'
    for row in range(rows):
        info_string = ''
        for column in range(columns):
            pos = (row, column)
            if pos in free_spots:
                cavern_string += "."
            elif pos in units:
                info_string += ' {}({}/{}),'.format(units[pos][0], units[pos][2],
                                                    elves[pos][1] if units[pos][0] == 'E' else goblins[pos][1])
                cavern_string += units[pos][0]
            else:
                cavern_string += '#'
        cavern_string += info_string[:-1] + '\n'
    cavern_string += '\n'
    return cavern_string


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
    positions.sort(key=lambda x: x[1])
    positions.sort()
    return positions


def make_move(free_spots, units, elves, goblins, targets_range, unit):
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
    closest_positions.sort(key=lambda x: x[1])
    closest_positions.sort()
    # print('debug: unit, closest_positions: ', unit, closest_positions)
    if closest_positions:
        closest_position = closest_positions[0]
    else:
        # no possibility to move into enemy's range
        return free_spots, units, elves, goblins, None, unit
        # targets_range set to None, so that we will proceed to attack

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
        free_spots.add(unit)
        free_spots.remove(position)
        units.pop(unit)
        units[position] = ['E', *units_values]
    else:
        units_values = goblins.pop(unit)
        goblins[position] = units_values
        free_spots.add(unit)
        free_spots.remove(position)
        units.pop(unit)
        units[position] = ['G', *units_values]

    if position in targets_range:
        targets_range = None
    return free_spots, units, elves, goblins, targets_range, position


def attack(free_spots, units, elves, goblins, unit):
    # check all adjacent enemies
    row, column = unit
    neighbours = {(row - 1, column),
                  (row + 1, column),
                  (row, column - 1),
                  (row, column + 1)}
    enemy_type = 'E' if unit in goblins else 'G'
    if enemy_type == 'E':
        neighbours = neighbours.intersection(set(elves.keys()))
    else:
        neighbours = neighbours.intersection(set(goblins.keys()))
    if len(neighbours) == 0:
        logger('Aaaah! No one to attack!')
        return free_spots, units, elves, goblins
    logger('potential targets:', neighbours)

    # choose the one with fewest hit points (reading order in case of a tie)
    min_hit_points = 201
    neighbours_with_min_hit_points = list()
    for neighbour in neighbours:
        neighbour_hit_points = elves[neighbour][1] if enemy_type == 'E' else goblins[neighbour][1]
        if neighbour_hit_points == min_hit_points:
            neighbours_with_min_hit_points.append(neighbour)
        elif neighbour_hit_points < min_hit_points:
            min_hit_points = neighbour_hit_points
            neighbours_with_min_hit_points = [neighbour]
    neighbours_with_min_hit_points.sort(key=lambda x: x[1])
    neighbours_with_min_hit_points.sort()
    selected_target = neighbours_with_min_hit_points[0]
    if selected_target == (2, 4):
        logger('##### Elf is attacked by goblin at {}'.format(unit))
    # if enemy_type == 'G':
    #     print('unit {} selects target: {}, {}'.format(unit, selected_target, enemy_type))
    #     print(neighbours_with_min_hit_points)
    #     print(neighbours)

    # The unit deals damage equal to its attack power to the selected target, reducing its hit points by that amount
    # If this reduces its hit points to 0 or fewer, the selected target dies: its square becomes .,
    # it is removed from its dict
    if enemy_type == 'E':
        elves[selected_target][1] -= goblins[unit][0]
        units[selected_target][2] -= goblins[unit][0]
        if elves[selected_target][1] <= 0:
            elves.pop(selected_target)
            free_spots.add(selected_target)
            units.pop(selected_target)
    else:
        try:
            goblins[selected_target][1] -= elves[unit][0]
            units[selected_target][2] -= elves[unit][0]
        except KeyError:
            logger('unit {} is in elves: {}'.format(unit, unit in elves))
            logger('target {} is in goblins: {}'.format(selected_target, selected_target in goblins))
            quit()
        if goblins[selected_target][1] <= 0:
            goblins.pop(selected_target)
            free_spots.add(selected_target)
            units.pop(selected_target)
    return free_spots, units, elves, goblins


def make_single_units_turn(free_spots, units, elves, goblins, unit):
    global cavern_strings

    # targets = get_targets(units, unit)
    targets = elves if unit in goblins else goblins
    targets_range = get_range(free_spots, targets, unit)
    logger('unit {} of type {} targets range: {}'.format(unit, 'E' if unit in elves else 'G', targets_range))
    if targets_range:
        # find a place to move firstly
        free_spots, units, elves, goblins, targets_range, unit = make_move(free_spots,
                                                                           units, elves, goblins, targets_range, unit)
        logger('range was not None, so move was made:')
        cavern_strings.append(display_cavern(free_spots, units, elves, goblins, 32, 32))
    if targets_range is None:
        # unit is in target's range, attack
        logger('so it is time for attack for unit {}'.format(unit))
        free_spots, units, elves, goblins = attack(free_spots, units, elves, goblins, unit)
    return free_spots, units, elves, goblins


def make_round(free_spots, units, elves, goblins):
    ordered_units = list(units.keys())
    # alternatively:
    # ordered_units = list(elves.keys()) + list(goblins.keys())
    ordered_units.sort(key=lambda x: x[1])
    ordered_units.sort()
    logger('order for next round:', ordered_units)
    for unit in ordered_units:
        if unit not in elves and unit not in goblins:
            continue
        free_spots, units, elves, goblins = make_single_units_turn(free_spots, units, elves, goblins, unit)
    return free_spots, units, elves, goblins


def battle(free_spots, units, elves, goblins, max_row, max_column):
    global cavern_strings

    rounds_count = 0
    cavern_strings.append(display_cavern(free_spots, units, elves, goblins, max_row, max_column, 0))
    while True:
        rounds_count += 1
        free_spots, units, elves, goblins = make_round(free_spots, units, elves, goblins)
        cavern_strings.append(display_cavern(free_spots, units, elves, goblins, max_row, max_column, rounds_count))
        if len(elves) == 0 or len(goblins) == 0:
            print('Combat ends after {} full rounds.'.format(rounds_count))
            total_hit_points = 0
            for elf in elves.values():
                total_hit_points += elf[1]
            for goblin in goblins.values():
                total_hit_points += goblin[1]
            print('{} win with {} total hit points left.'.format('Goblins' if len(goblins) > 0 else 'Elves',
                                                                 total_hit_points))
            print('Outcome: {}'.format(rounds_count * total_hit_points))
            show_all(cavern_strings)
            quit()


def show_all(caverns):
    idx = 0
    steps = len(caverns)
    while True:
        os.system('cls')
        print(caverns[idx])
        ch1, ch2 = take_char()
        if ch1 == 224 and ch2 == 75:
            idx = (idx - 1) % steps
        elif ch1 == 224 and ch2 == 77:
            idx = (idx + 1) % steps
        elif ch1 == ord('q') or ch1 == ord('Q'):
            quit()


def main(my_file):
    free_spots, units, elves, goblins, max_row, max_column = get_cavern(my_file)
    display_cavern(free_spots, units, elves, goblins, max_row, max_column)
    battle(free_spots, units, elves, goblins, max_row, max_column)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "15_input.txt"
    main(filename)


# elves:    0, goblins:   16
# Combat ends after 80 full rounds.
# Goblins win with 186 total hit points left.
# Outcome: 14880
# answer too low

# elves:    0, goblins:   16
# Combat ends after 82 full rounds.
# Goblins win with 2627 total hit points left.
# Outcome: 215414
# answer too high
