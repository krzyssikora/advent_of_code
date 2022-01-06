import sys
import re


def get_data(my_file):
    with open(my_file) as f:
        ret_list = [list(map(int, re.findall(r"([0-9]+)", line))) for line in f.readlines()]
    return ret_list


def distance(reindeer, duration):
    velocity, race_time, rest_time = reindeer
    num_rests = duration // (race_time + rest_time)
    remaining_time = duration % (race_time + rest_time)
    num_races = num_rests + 1 * (remaining_time >= race_time)
    return velocity * race_time * num_races + velocity * remaining_time * (remaining_time < race_time)


def main(my_file):
    reindeer_data = get_data(my_file)
    reindeer_list = [0 for _ in range(len(reindeer_data))]
    for duration in range(1, 2504):
        distances = [distance(reindeer, duration) for reindeer in reindeer_data]
        max_distance = max(distances)
        pos = -1
        for i in range(distances.count(max_distance)):
            pos = distances[pos + 1:].index(max_distance) + pos + 1
            reindeer_list[pos] += 1
    print(max(reindeer_list))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "14_input.txt"
    main(filename)
