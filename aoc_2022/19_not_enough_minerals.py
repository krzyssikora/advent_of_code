import sys
import os
import re
from queue import Queue


def get_data(my_file: str) -> str:
    with open(my_file) as f:
        data = f.read()
    while '\n' in data:
        data = data.replace('\n', '')
    while '  ' in data:
        data = data.replace('  ', ' ')
    return data


def get_blueprints(data: str) -> dict:
    blueprints = dict()
    pattern = re.compile(r'Blueprint (\d+): '
                         r'Each ore robot costs (\d+) ore. '
                         r'Each clay robot costs (\d+) ore. '
                         r'Each obsidian robot costs (\d+) ore and (\d+) clay. '
                         r'Each geode robot costs (\d+) ore and (\d+) obsidian.')
    while True:
        m = re.match(pattern, data)
        if not m:
            break
        g = list(map(int, m.groups()))
        data = data[m.end():]
        # 'geode': 0,
        # 'obsidian': 1,
        # 'clay': 2,
        # 'ore': 3

        blueprints[g[0]] = {
            3: {3: g[1]},
            2: {3: g[2]},
            1: {
                3: g[3], 2: g[4]
            },
            0: {
                3: g[5], 1: g[6]
            }
        }
    return blueprints


def get_neighbours(robots: tuple, minerals: tuple, blueprint: dict) -> set:
    neighbours = set()
    for idx in range(4):
        current_robots, current_minerals = list(robots), list(minerals)
        prices = blueprint[idx]
        # print(idx, prices, current_robots, current_minerals)
        if all(current_minerals[mineral_idx] >= price for mineral_idx, price in prices.items()):
            # print('buying')
            for mineral_idx, price in prices.items():
                current_minerals[mineral_idx] -= price
            current_robots[idx] += 1
        current_minerals = tuple(current + collected for current, collected in zip(current_minerals, robots))
        neighbours.add((tuple(current_robots), current_minerals))
    # additionally a neighbour got from collecting minerals only
    current_minerals = tuple(current + collected for current, collected in zip(minerals, robots))
    neighbours.add((robots, current_minerals))
    return neighbours


def update_all_geodes_and_max_geodes(path, number_of_geodes, all_geodes, max_geodes):
    tuple_path = (path[0], tuple(path[2:]))
    if tuple_path not in all_geodes or all_geodes[tuple_path] < path[1]:
        all_geodes[tuple_path] = path[1]
    if number_of_geodes > max_geodes:
        max_geodes = number_of_geodes
    return all_geodes, max_geodes


def get_blueprint_quality_level(blueprints: dict, blueprint_idx: int) -> int:
    return blueprint_idx * get_max_gedoes_from_blueprint(blueprints[blueprint_idx])


def get_max_gedoes_from_blueprint(blueprint: dict) -> int:
    names = {
        0: 'geode',
        1: 'obsidian',
        2: 'clay',
        3: 'ore'
    }
    max_time = 24
    max_geodes = 0
    queue = Queue()
    queue.put((0, (0, 0, 0, 1), (0, 0, 0, 0)))  # (time, robots, minerals)

    while True:
        qsize = queue.qsize()
        if qsize % 500000 == 0:
            print(f'{qsize // 1000000 if qsize >= 100000 else ""} {str((qsize % 1000000) // 1000).ljust(3, "0")} 000')
        if queue.empty():
            break
        current_time, current_robots, current_minerals = queue.get()
        neighbours = get_neighbours(current_robots, current_minerals, blueprint)
        new_time = current_time + 1
        for neighbour in neighbours:
            neighbour_robots, neighbours_minerals = neighbour
            if new_time >= max_time:
                if neighbours_minerals[0] > max_geodes:
                    max_geodes = neighbours_minerals[0]
            else:
                queue.put((new_time, neighbour_robots, neighbours_minerals))

    return max_geodes


def main(my_file: str) -> None:
    data = get_data(my_file)
    blueprints = get_blueprints(data)

    print(get_blueprint_quality_level(blueprints, 1))

    print("part 1:", )
    print("part 2:", )


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = f'{os.path.basename(__file__)[:2]}_inp.txt'
    main(filename)
