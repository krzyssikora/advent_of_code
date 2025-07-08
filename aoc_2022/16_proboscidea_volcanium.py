import sys
import os
import re
from queue import Queue


def get_data_lines(my_file: str):
    with open(my_file) as f:
        lines = f.readlines()
    return [line.strip('\n').strip() for line in lines]


def get_valves(lines: list):
    pattern = r'Valve ([a-zA-Z]+) has flow rate=(\d+); tunnels* leads* to valves* (.+)'
    valves = dict()
    for line in lines:
        valve, flow_str, neighbours_str = re.findall(pattern, line)[0]
        valves[valve] = {
            'flow': int(flow_str),
            'neighbours': neighbours_str.split(', ')
        }
    return valves


def dijkstra(valves: dict, start: str):
    valves_names = set(valves.keys())
    max_len = len(valves_names)
    distances = {valve: max_len for valve in valves_names}
    distances[start] = 0
    sorted_queue = sorted(distances, key=distances.get)

    while True:
        queue = {v: distances[v] for v in sorted_queue}
        if not queue:
            break
        sorted_queue = sorted(queue, key=queue.get)
        u = sorted_queue[0]
        sorted_queue = sorted_queue[1:]

        neighbours = valves[u]['neighbours']
        for neighbour in neighbours:
            alternative = distances[u] + 1
            if alternative < distances[neighbour]:
                distances[neighbour] = alternative

    return distances


def remove_items_with_zero_rate_values(valve: str, valve_dists: dict, valves: dict):
    return {v: d for v, d in valve_dists.items() if (valves[v]['flow'] or v == 'AA') and v != valve}


def get_valves_with_positive_rate(valves: dict):
    valves_plus_names = {valve for valve in valves if valves[valve]['flow'] > 0 or valve == 'AA'}
    valves_plus = dict()
    for idx, valve in enumerate(valves_plus_names):
        new_valves_distances = remove_items_with_zero_rate_values(valve, dijkstra(valves, valve), valves)
        valves_plus[valve] = {
            'flow': valves[valve]['flow'],
            'neighbours': new_valves_distances
        }
    return valves_plus


def update_all_releases_and_best_release(path, new_path, all_releases, best_release):
    tuple_path = (path[0], tuple(path[3:]))
    if tuple_path not in all_releases or all_releases[tuple_path] < path[1]:
        all_releases[tuple_path] = path[1]
    if new_path[1] > best_release:
        best_release = new_path[1]
    return all_releases, best_release


def get_highest_pressure_release(valves: dict, start: str, part: int):
    max_time = 30 if part == 1 else 26
    best_release = 0
    paths = Queue()
    paths.put([0, 0, start])  # paths consists of tuples (time, release, path_elt_0, path_elt_1, path_elt_2...)
    all_releases = dict()

    while True:
        if paths.empty():
            break
        path = paths.get()
        current_valve = path[-1]
        neighbours_dict = valves[current_valve]['neighbours']
        neighbours = list(neighbours_dict).copy()
        all_releases, best_release = update_all_releases_and_best_release(path, path, all_releases, best_release)
        for v in path[2:]:
            if v in neighbours:
                neighbours.remove(v)
            if not neighbours:
                break
        for new_valve in neighbours:
            new_path = path.copy()
            new_time = new_path[0] + neighbours_dict[new_valve] + 1
            if new_time > max_time:
                all_releases, best_release = update_all_releases_and_best_release(path, new_path, all_releases,
                                                                                  best_release)

            else:
                new_path.append(new_valve)
                new_path[0] = new_time
                new_path[1] += (max_time - new_time) * valves[new_valve]['flow']
                if new_time == max_time:
                    all_releases, best_release = update_all_releases_and_best_release(path, new_path, all_releases,
                                                                                      best_release)
                else:
                    paths.put(new_path)

    if part == 2:
        # get best_releases from all_releases
        best_releases = dict()
        for valves_time, release in all_releases.items():
            current_valves = frozenset(valves_time[1])
            if current_valves not in best_releases or best_releases[current_valves] < release:
                best_releases[current_valves] = release
        valves_names = set(valves)
        for first_valves, release in best_releases.items():
            if len(first_valves) <= len(valves_names) // 2:
                all_other_valves = frozenset(valves_names.difference(first_valves))
                for other_valves, other_release in best_releases.items():
                    if other_valves.issubset(all_other_valves):
                        new_release = release + other_release
                        if new_release > best_release:
                            best_release = new_release

    return best_release


def display_valves(valves: dict):
    print('valves:')
    for valve, data in valves.items():
        print(valve.ljust(4) + f' flow: {data["flow"]}')
        print(f'    neigh: {data["neighbours"]}')


def display_distances(distances: dict):
    print('distances:')
    for valve, data in distances.items():
        print(valve.ljust(5) + f'{data}')


def main(my_file: str):
    lines = get_data_lines(my_file)
    valves = get_valves(lines)
    valves = get_valves_with_positive_rate(valves)

    print("part 1:", get_highest_pressure_release(valves, 'AA', 1))
    print("part 2:", get_highest_pressure_release(valves, 'AA', 2))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = f'{os.path.basename(__file__)[:2]}_input.txt'
    main(filename)
