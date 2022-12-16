import sys
import os
import re


def get_data_lines(my_file):
    with open(my_file) as f:
        lines = f.readlines()
    return [line.strip('\n').strip() for line in lines]


def get_sensors_and_beacons(lines):
    pattern = re.compile(r'Sensor at x=(-*\d+), y=(-*\d+): closest beacon is at x=(-*\d+), y=(-*\d+)')
    sensors_with_beacons = dict()
    beacons = set()
    for line in lines:
        sensor_x, sensor_y, beacon_x, beacon_y = map(int, re.findall(pattern, line)[0])
        sensors_with_beacons[(sensor_x, sensor_y)] = (beacon_x, beacon_y)
        beacons.add((beacon_x, beacon_y))
    return sensors_with_beacons, beacons


def get_range_with_centre_radius(centre, radius):
    return centre - radius, centre + radius + 1


def get_range_with_centre_radius_within_range(centre, radius, range_start=0, range_end=4000001):
    return max(centre - radius, range_start), min(centre + radius + 1, range_end)


def get_number_of_positions_without_beacon_in_line(sensors_with_beacons, beacons, line_idx=2000000):
    positions_without_beacon = set()
    # firstly, get positions seen by sensors
    for sensor, beacon in sensors_with_beacons.items():
        sensor_x, sensor_y = sensor
        beacon_x, beacon_y = beacon
        radius = abs(sensor_y - beacon_y) + abs(sensor_x - beacon_x)
        # print('sensor: {}, beacon: {}, radius: {}'.format(sensor, beacon, radius))
        line_range_start, line_range_end = get_range_with_centre_radius(sensor_y, radius)
        # print('line_range_start: {}, line_range_end: {}'.format(line_range_start, line_range_end))
        # for line_idx in set(range(line_range_start, line_range_end)).intersection(lines_indexes):
        if line_range_start <= line_idx < line_range_end:
            pos_range_start, pos_range_end = get_range_with_centre_radius(sensor_x, radius - abs(sensor_y - line_idx))
            # print('pos_range_start: {}, pos_range_end: {}'.format(pos_range_start, pos_range_end))
            for pos in range(pos_range_start, pos_range_end):
                positions_without_beacon.add(pos)
    # secondly, remove positions of beacons
    for beacon_x, beacon_y in beacons:
        if beacon_y == line_idx:
            positions_without_beacon.remove(beacon_x)

    return len(positions_without_beacon)


def find_containing_range(
        value: int,
        ranges: list,
        idx_from: int,
        idx_to: int,
        down: bool
):
    if idx_to < idx_from:
        return False, idx_from if down else idx_from
    idx_mid = (idx_from + idx_to) // 2
    mid_range_start, mid_range_end = ranges[idx_mid]
    mid_range_end -= 1
    if mid_range_start <= value <= mid_range_end:
        return True, idx_mid
    if value < mid_range_start:
        return find_containing_range(value, ranges, idx_from, idx_mid - 1, down)
    if value > mid_range_end:
        return find_containing_range(value, ranges, idx_mid + 1, idx_to, down)


def add_new_range(new_range: tuple, ranges: list):
    if not ranges:
        return [new_range]
    new_range_start, new_range_end = new_range

    inside_lower, range_idx_lower = find_containing_range(new_range_start, ranges, 0, len(ranges) - 1, True)
    inside_upper, range_idx_upper = find_containing_range(new_range_end, ranges, 0, len(ranges) - 1, False)
    if not inside_upper:
        range_idx_upper -= 1
    if range_idx_lower > range_idx_upper:
        range_idx_upper = range_idx_lower
    added_range_start = ranges[range_idx_lower][0] if inside_lower else new_range_start
    added_range_end = ranges[range_idx_upper][1] if inside_upper else new_range_end

    # merge left, when they touch
    if range_idx_lower > 0:
        if added_range_start == ranges[range_idx_lower - 1][1]:
            range_idx_lower -= 1
            added_range_start = ranges[range_idx_lower][0]
        elif added_range_start < ranges[range_idx_lower - 1][1]:
            range_idx_lower -= 1

    # merge right, when they touch
    if range_idx_upper < len(ranges):
        if added_range_end == ranges[range_idx_upper][0]:
            added_range_end = ranges[range_idx_upper][1]
            range_idx_upper += 1
        elif added_range_end > ranges[range_idx_upper][0]:
            range_idx_upper += 1

    ranges = ranges[:range_idx_lower] + [(added_range_start, added_range_end)] + ranges[range_idx_upper:]

    return ranges


def get_positions_without_beacons(sensors_with_beacons_and_miny,
                                  range_start=0, range_end=4000001):
    positions_without_beacons = {idx: list() for idx in range(range_start, range_end)}
    # firstly, get positions seen by sensors
    for sensor_x, sensor_y, beacon_x, beacon_y, min_y in sensors_with_beacons_and_miny:
        radius = abs(sensor_y - beacon_y) + abs(sensor_x - beacon_x)
        line_range_start, line_range_end = get_range_with_centre_radius_within_range(sensor_y,
                                                                                     radius,
                                                                                     range_start,
                                                                                     range_end)
        if line_range_end < min_y:
            continue
        for line_idx in range(line_range_start, line_range_end):
            pos_range_start, pos_range_end = \
                get_range_with_centre_radius_within_range(sensor_x,
                                                          radius - abs(sensor_y - line_idx),
                                                          range_start,
                                                          range_end)
            positions_without_beacons[line_idx] = \
                add_new_range((pos_range_start, pos_range_end), positions_without_beacons[line_idx])

    return positions_without_beacons


def get_tuning_frequency(sensors_with_beacons_and_miny,
                         range_start=0, range_end=4000001):
    positions_without_beacons = get_positions_without_beacons(sensors_with_beacons_and_miny, range_start, range_end)
    y, ranges = max(positions_without_beacons.items(), key=lambda x: len(x[1]))
    x = ranges[0][1]
    return 4000000 * x + y


def add_miny_to_sensors_and_beacons(sensors_with_beacons):
    sensors_with_beacons_and_miny = list()
    for sensor, beacon in sensors_with_beacons.items():
        sensor_x, sensor_y = sensor
        beacon_x, beacon_y = beacon
        sensors_with_beacons_and_miny.append((sensor_x, sensor_y, beacon_x, beacon_y, sensor_y - abs(sensor_y - beacon_y)))

    sensors_with_beacons_and_miny.sort(key=lambda x: x[4])
    return sensors_with_beacons_and_miny


def main(my_file):
    lines = get_data_lines(my_file)
    sensors_with_beacons, beacons = get_sensors_and_beacons(lines)
    sensors_with_beacons_and_miny = add_miny_to_sensors_and_beacons(sensors_with_beacons)

    line_idx = 2000000
    # line_idx = 10
    max_val = 4000000
    # max_val = 20

    print("part 1:", get_number_of_positions_without_beacon_in_line(sensors_with_beacons, beacons, line_idx))
    print("part 2:", get_tuning_frequency(sensors_with_beacons_and_miny, 0, max_val + 1))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = f'{os.path.basename(__file__)[:2]}_input.txt'
    main(filename)
