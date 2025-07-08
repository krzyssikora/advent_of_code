import sys
import os


def get_data(my_file: str) -> (list, list):
    with open(my_file) as f:
        data = f.read()
    data = data.split('\n\n')

    seeds = list(map(int, data[0].split(': ')[1].split()))
    maps = [get_map(map_data.split('\n')[1:]) for map_data in data[1:]]
    return seeds, maps


def get_map(map_data: list) -> list:
    map_data = [st.strip() for st in map_data if st.strip()]
    single_map = []
    for mapping_st in map_data:
        destination_start, source_start, range_length = list(map(int, mapping_st.split()))
        source_end = source_start + range_length
        shift = destination_start - source_start
        single_map.append((source_start, source_end, shift))
    single_map.sort()
    return single_map


def get_lowest_location_number(seeds: list, maps: list) -> int:
    return min(get_location_number(seed, maps) for seed in seeds)


def get_lowest_location_number_for_ranges_of_seeds(seeds: list, maps: list) -> int:
    seed_ranges = []
    for idx in range(0, len(seeds), 2):
        initial, step = seeds[idx], seeds[idx + 1]
        seed_ranges.append((initial, initial + step))
    for single_map in maps:
        print(f'single_map: {single_map}')
        seed_ranges = transform_ranges(seed_ranges, single_map)
        print(f'min: {seed_ranges[0][0]}')
        print()
    return seed_ranges[0][0]

# def get_location_number_for_range_of_seeds(seed_first, seed_last, maps) -> int:
#     for single_map in maps:
#         mapping_first = get_mapping_idx_binary(seed_first, single_map, 0, len(single_map) - 1)
#         # print('mapping_first', mapping_first)
#         mapping_last = get_mapping_idx_binary(seed_last, single_map, mapping_first, len(single_map) - 1)
#         # print('mapping_last', mapping_last)
#         # min_location =


def get_location_number(seed: int, maps: list) -> int:
    location = seed
    for single_map in maps:
        location = get_mapping(location, single_map)
    return location


def get_mapping(location: int, single_map: list) -> int:
    start, end = 0, len(single_map) - 1
    mapping = get_mapping_binary(location, single_map, start, end)
    return mapping


def get_mapping_binary(location: int, single_map: list, start: int, end: int) -> int:
    if start > end:
        return location
    if start == end:
        if single_map[end][0] <= location < single_map[end][1]:
            return location + single_map[end][2]
        else:
            return location
    middle = (start + end) // 2
    mapping = single_map[middle]

    if mapping[0] <= location < mapping[1]:
        return location + mapping[2]
    if location < mapping[0]:
        if middle == 0:
            return location
        else:
            return get_mapping_binary(location, single_map, start, middle - 1)
    if mapping[1] <= location:
        return get_mapping_binary(location, single_map, middle + 1, end)
    return location


def get_mapping_idx_binary(location: int, single_map: list, start: int, end: int) -> int or float:
    middle = (start + end) // 2
    mapping = single_map[middle]

    if mapping[0] <= location < mapping[1]:
        return middle
    if location < mapping[0]:
        if middle == 0:
            return -0.5
        elif middle == start:
            return middle - 0.5
        else:
            return get_mapping_idx_binary(location, single_map, start, middle - 1)
    if location >= mapping[1]:
        if middle == end:
            return middle + 0.5
        else:
            return get_mapping_idx_binary(location, single_map, middle + 1, end)


def get_part_result(seeds: list, maps: list, part: int) -> int:
    if part == 1:
        return get_lowest_location_number(seeds, maps)
    elif part == 2:
        return get_lowest_location_number_for_ranges_of_seeds(seeds, maps)


def simplify_maps(maps: list) -> list:
    new_maps = []
    for single_map in maps:
        new_single_map = [single_map[0]]
        for idx in range(len(single_map) - 1):
            source_1, dest_1, shift_1 = single_map[idx]
            source_2, dest_2, shift_2 = single_map[idx + 1]
            if dest_1 == source_2 and shift_1 == shift_2:
                continue
            new_single_map.append((source_2, dest_2, shift_2))
        new_maps.append(new_single_map)
    return new_maps


def simplify_ranges(ranges: list) -> list:
    ranges.sort()
    simplified_ranges = []
    first, second = ranges[0]
    idx = 1
    while True:
        if idx >= len(ranges):
            simplified_ranges.append((first, second))
            break
        third, fourth = ranges[idx]
        if third <= second < fourth:
            second = fourth
        elif third > second:
            simplified_ranges.append((first, second))
            first, second = third, fourth
        idx += 1
    return simplified_ranges


def transform_ranges(ranges: list, single_map) -> list:
    def transform_value(value: int, _map: list, _idx: int or float) -> int:
        _shift = _map[_idx][2] if int(_idx) == _idx else 0
        return value + _shift

    min_idx, max_idx = 0, len(single_map) - 1
    transformed_ranges = []
    print(f'ranges: {ranges}')
    for range_start, range_end in ranges:
        start_idx = get_mapping_idx_binary(range_start, single_map, 0, len(single_map) - 1)
        end_idx = get_mapping_idx_binary(range_end, single_map, 0, len(single_map) - 1)
        print(f'range_start: {range_start}, range_end: {range_end}, ', start_idx, end_idx, len(single_map))
        if start_idx == end_idx:
            shift = single_map[start_idx][2] if int(start_idx) == start_idx else 0
            transformed_ranges.append((range_start + shift, range_end + shift))
            print(f'1 appended: {(range_start + shift, range_end + shift)}')
        elif start_idx == max_idx:
            transformed_ranges.append((range_start + single_map[start_idx][2],
                                       single_map[start_idx][0] + single_map[start_idx][2]))
            transformed_ranges.append((single_map[start_idx][0], range_end))
            print(f'2 appended 1: {(range_start + single_map[start_idx][2], single_map[start_idx][0] + single_map[start_idx][2])}')
            print(f'2 appended 2: {(single_map[start_idx][0], range_end)}')
        elif end_idx == min_idx:
            transformed_ranges.append((range_start, single_map[end_idx][1]))
            transformed_ranges.append((single_map[end_idx][1] + single_map[end_idx][2],
                                       range_end + single_map[end_idx][2]))
            print(f'3 appended 1: {(range_start, single_map[end_idx][1])}')
            print(f'3 appended 2: {(single_map[end_idx][1] + single_map[end_idx][2], range_end + single_map[end_idx][2])}')
        else:
            first = transform_value(range_start, single_map, start_idx)
            last = transform_value(range_end, single_map, end_idx)

            print(f'first: {first}, last: {last}')
            if int(start_idx) == start_idx:
                transformed_ranges.append((first, single_map[start_idx][1] + single_map[start_idx][2]))
                transformed_ranges.append((single_map[start_idx][1], single_map[start_idx + 1][0]))
                print(f'4 appended 1: {(first, single_map[start_idx][1] + single_map[start_idx][2])}')
                print(f'4 appended 2: {(single_map[start_idx][1], single_map[start_idx + 1][0])}')
                start_idx += 1
            else:
                start_idx = int(start_idx + 0.5)
                transformed_ranges.append((first, single_map[start_idx][0]))
                print(f'5 appended: {(first, single_map[start_idx][0])}')

            if int(end_idx) == end_idx:
                transformed_ranges.append((single_map[end_idx][0] + single_map[end_idx][2], last))
                transformed_ranges.append((single_map[end_idx - 1][1], single_map[end_idx][0]))
                print(f'6 appended: {(single_map[end_idx][0] + single_map[end_idx][2], last)}')
                print(f'6 appended: {(single_map[end_idx - 1][1], single_map[end_idx][0])}')
                end_idx -= 1
            else:
                end_idx = int(end_idx - 0.5)
                transformed_ranges.append((single_map[end_idx][1], last))
                print(f'7 appended: {(single_map[end_idx][1], last)}')

            boundaries = []
            for idx in range(int(start_idx), int(end_idx) + 1):
                mapping = single_map[idx]
                boundaries += [mapping[0], mapping[1]]
                transformed_ranges.append((mapping[0] + mapping[2], mapping[1] + mapping[2]))
                print(f'8 appended: {(mapping[0] + mapping[2], mapping[1] + mapping[2])}')

            boundaries = boundaries[1:-1]
            left_boundaries = boundaries[0::2]
            right_boundaries = boundaries[1::2]
            for left, right in zip(left_boundaries, right_boundaries):
                transformed_ranges.append((left, right))
                print(f'9 appended: {(left, right)}')

    transformed_ranges = simplify_ranges(transformed_ranges)
    print(f'transformed_ranges: {transformed_ranges}')
    return transformed_ranges


def main(my_file: str) -> None:
    seeds, maps = get_data(my_file)
    maps = simplify_maps(maps)
    for part in [1, 2]:
        print(f'part {part}: {get_part_result(seeds, maps, part)}')


if __name__ == "__main__":
    # ranges = [(0, 5), (5, 7), (10, 20), (15, 25), (30, 50), (33, 37), (40, 45),
    #           (60, 90), (65, 70), (75, 80), (88, 100)]
    # print(simplify_ranges(ranges))
    # quit()
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = f'{os.path.basename(__file__)[:2]}_inp.txt'
    main(filename)
