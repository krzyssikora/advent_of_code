import sys
import os
import logging
from itertools import cycle

# create logger
# logging.basicConfig(level='DEBUG')
_logger = logging.getLogger()
_logger.setLevel(logging.WARNING)
# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# create formatter
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
formatter = logging.Formatter('%(funcName)s, line: %(lineno)d >> \n %(message)s')
# add formatter to ch
ch.setFormatter(formatter)
# add ch to logger
_logger.addHandler(ch)


LEFT = -1  # -3
RIGHT = 7
BOTTOM = 0
ROCKS = [tuple((x + 2, y) for x, y in rock) for rock in [
    [(0, 0), (1, 0), (2, 0), (3, 0)],
    [(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)],
    [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)],
    [(0, 0), (0, 1), (0, 2), (0, 3)],
    [(0, 0), (1, 0), (0, 1), (1, 1)]
]]


class Cyclometer:
    def __init__(self):
        self.storage = None
        self.rock_idx = None
        self.move_idx = None
        self.max_height = None
        self.logs = None

    def initialize(self, storage: dict, rock_idx: int, move_idx: int):
        self.storage = {k: v.copy() for k, v in storage.items()}
        self.rock_idx = rock_idx
        self.move_idx = move_idx
        self.max_height = get_max_height(self.storage)
        self.logs = set()

    def cycle_found(self, storage: dict, rock_idx: int, move_idx: int, moves: list):
        repeated_pattern = self.storage is not None
        if not repeated_pattern:
            return False

        repeated_pattern = (self.rock_idx - rock_idx) % 5 == 0
        if not repeated_pattern:
            return False

        repeated_pattern = (self.move_idx - move_idx) % len(moves) == 0
        if not repeated_pattern:
            return False

        max_height = get_max_height(storage)
        offset = max_height - self.max_height
        repeated_pattern = \
            all(
                hit == rock_is_stopped(tuple((x, y + offset) for x, y in rock), storage)
                for hit, rock in self.logs
            )

        return repeated_pattern

    def add_rock_to_logs(self, hit: bool, rock: tuple):
        if not hit or rock_is_stopped(rock, self.storage):
            self.logs.add((hit, rock))


def get_max_height(storage: dict):
    max_height = 0
    for x in storage.keys():
        if storage[x]:
            max_height = max(max_height, *storage[x])
    return max_height


def get_moves(my_file: str):
    with open(my_file) as f:
        line = f.read()
    return line.strip('\n').strip()


def rock_is_stopped(rock: tuple, storage: dict):
    return any(
        x == LEFT or x == RIGHT or y == BOTTOM or
        y in storage[x] for x, y in rock
    )


def get_moves_values(my_file: str, idx_from=0, many=None):
    def mapping(char):
        return -1 if char == '<' else 1

    moves = get_moves(my_file)

    if many is None:
        many = len(moves) - idx_from

    return list(map(mapping, moves[idx_from: idx_from + many]))


def place_rock_on_the_tower(rock: tuple, storage: dict):
    for x, y in rock:
        storage[x].add(y)
    return storage


# def display_rock(rock: tuple):
#     min_x, min_y = min(r[0] for r in rock), min(r[1] for r in rock)
#     max_x, max_y = max(r[0] for r in rock), max(r[1] for r in rock)
#     print(min_x, min_y)
#     for y in reversed(range(min_y, max_y + 1)):
#         for x in range(min_x, max_x + 1):
#             if (x, y) in rock:
#                 print('#', end='')
#             else:
#                 print(' ', end='')
#         print()
#     print()
#
#
# def display_storage(storage: dict, max_row=None):
#     if max_row is None:
#         max_row = get_max_height(storage)
#     rows = dict()
#     for x, heights in storage.items():
#         for h in heights:
#             if h not in rows:
#                 rows[h] = set()
#             rows[h].add(x)
#
#     storage_string = ''
#     for row in reversed(range(1, max_row + 1)):
#         storage_string += str(row + 1).ljust(4) + '|'
#         if row not in rows:
#             storage_string += '       '
#         else:
#             for x in range(7):
#                 storage_string += '#' if x in rows[row] else ' '
#         storage_string += '|\n'
#     storage_string += '    +-------+\n'
#
#     print(storage_string)
#
#
def get_height_of_the_tower(moves: list):
    move_idx = 0
    current_height = 0
    height_from_cycles = 0
    height_2022, height_final = 0, 0
    rocks_to_fall = 10 ** 12
    storage = {x: set() for x in range(7)}
    cyclometer = Cyclometer()

    for rock_idx, rock in enumerate(cycle(ROCKS)):
        if cyclometer.cycle_found(storage, rock_idx, move_idx, moves):
            number_of_rocks_in_cycle = rock_idx - cyclometer.rock_idx
            skipped_cycles = (rocks_to_fall - rock_idx) // number_of_rocks_in_cycle
            height_from_cycles += skipped_cycles * (current_height - cyclometer.max_height)
            rocks_to_fall -= skipped_cycles * number_of_rocks_in_cycle

        if rock_idx == 2022:
            height_2022 = current_height

        if rock_idx == rocks_to_fall:
            height_final = current_height + height_from_cycles
            break

        if rock_idx > 2000 and cyclometer.max_height is None:
            cyclometer.initialize(storage, rock_idx, move_idx)

        current_rock = [(x, y + current_height + 4) for x, y in rock]

        while True:
            move = moves[move_idx % len(moves)]
            move_idx += 1
            # move horizontally
            rock_moved = tuple((x + move, y) for x, y in current_rock)
            hit = rock_is_stopped(rock_moved, storage)
            if not hit:
                current_rock = rock_moved
            if cyclometer.max_height:
                cyclometer.add_rock_to_logs(hit, rock_moved)

            # move down
            rock_moved = tuple((x, y - 1) for x, y in current_rock)
            hit = rock_is_stopped(rock_moved, storage)
            if cyclometer.max_height:
                cyclometer.add_rock_to_logs(hit, rock_moved)
            if not hit:
                current_rock = rock_moved
            else:
                break
        storage = place_rock_on_the_tower(current_rock, storage)
        current_height = get_max_height(storage)

    return height_2022, height_final


def main(my_file: str):
    moves = get_moves_values(my_file)

    height_2022, height_final = get_height_of_the_tower(moves)

    print("part 1:", height_2022)
    print("part 2:", height_final)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = f'{os.path.basename(__file__)[:2]}_input.txt'
    main(filename)
