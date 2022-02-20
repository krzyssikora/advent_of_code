import sys
import re
from datetime import datetime


def get_data(my_file):
    with open(my_file) as f:
        lines = f.readlines()
    # key is the ID, value is a dictionary:
    #    key = day number,
    #    value = list, where the first element is time from which the gourd is active
    #    and the following elements are tuples (a,b), where the gourd is asleep from time a incl. to b excl.
    pattern = r"\[([0-9- :]+)\] ([\S]+) ([\S]+)"
    tmp_list = list()
    for line in lines:
        data = re.findall(pattern, line)[0]
        date = datetime.strptime(data[0], "%Y-%m-%d %H:%M")
        tmp_list.append((date, data[1], data[2]))
    tmp_list.sort()
    guards = dict()
    count = 0
    many = len(tmp_list)
    while True:
        if count >= many:
            break
        date, one, two = tmp_list[count]
        if one == "Guard":
            guard_id = int(two[1:])
            data = list()
            data.append(date)
            if guard_id not in guards:
                guards[guard_id] = dict()
            guards[guard_id][str(date.month) + "-" + str(date.day)] = data
            start, end = None, None
            while True:
                count += 1
                if count >= many:
                    break
                date, one, two = tmp_list[count]
                if one == "Guard":
                    break
                elif one == "falls":
                    start = date
                elif one == "wakes":
                    end = date
                if end is not None and start is not None:
                    data.append((start, end))
                    start, end = None, None
    return guards


def minutes_asleep(guards):
    asleep = dict()
    for guard, days in guards.items():
        minutes = 0
        for day, data in days.items():
            for i in range(1, len(data)):
                minutes += (data[i][1] - data[i][0]).seconds // 60
        asleep[guard] = minutes
    return asleep


def minutes_frequencies(guard):
    freq = dict()
    for day in guard.values():
        for i in range(1, len(day)):
            start, end = day[i][0].minute, day[i][1].minute
            for m in range(start, end):
                freq[m] = freq.get(m, 0) + 1
    maximum = max(freq, key=freq.get) if len(freq) > 0 else -1
    if maximum > 0:
        fr = freq[maximum]
    else:
        fr = 0
    return maximum, fr


def part_1(guards):
    minutes = minutes_asleep(guards)
    sleeping_guard_id = max(minutes, key=minutes.get)
    sleeping_guard = guards[sleeping_guard_id]
    freq = minutes_frequencies(sleeping_guard)[0]
    return sleeping_guard_id * freq


def part_2(guards):
    freqs = dict()
    for guard in guards:
        freqs[guard] = minutes_frequencies(guards[guard])
    most_frequent_minute, highest_frequency = max(freqs.values(), key=lambda x: x[1])
    sleeper = next(key for key, val in freqs.items() if val == (most_frequent_minute, highest_frequency))
    return sleeper * most_frequent_minute


def main(my_file):
    guards = get_data(my_file)
    print("part 1:", part_1(guards))
    print("part 2:", part_2(guards))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "04_input.txt"
    main(filename)
