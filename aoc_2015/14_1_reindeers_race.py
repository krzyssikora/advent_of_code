import sys
import re


def get_data(my_file):
    with open(my_file) as f:
        ret_list = [list(map(int, re.findall(r"([0-9]+)", line))) for line in f.readlines()]
    return ret_list


def distance(reindeer, duration):
    velocity, race_time, rest_time = reindeer
    num_rests = duration // (race_time + rest_time)
    num_races = num_rests + 1 * (duration % (race_time + rest_time) > race_time)
    return velocity * race_time * num_races


def main(my_file):
    reindeer_data = get_data(my_file)
    max_distance = 0
    for reindeer in reindeer_data:
        current_distance = distance(reindeer, 2503)
        if current_distance > max_distance:
            max_distance = current_distance
    print(max_distance)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "14_input.txt"
    main(filename)
