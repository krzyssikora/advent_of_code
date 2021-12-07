input_data = "inp2.txt"
with open(input_data) as f:
    fish_list = f.readline().strip("\n").split(",")
    fish_list = [int(x) for x in fish_list]


def lanternfish_after_days(list_of_fish, days):
    if days == 1:
        return lanternfish_after_one_day(list_of_fish)
    else:
        return lanternfish_after_one_day(lanternfish_after_days(list_of_fish, days - 1))


def lanternfish_after_one_day(list_of_fish):
    old_fish = list()
    new_fish = list()
    for fish in list_of_fish:
        if fish > 0:
            old_fish.append(fish - 1)
        else:
            old_fish.append(6)
            new_fish.append(8)
    old_fish.extend(new_fish)
    return old_fish


"""
for day in range(19):
    if day == 0:
        print("Initial state:", fish_list)
    else:
        fish_list = lanternfish_after_one_day(fish_list)
        print("After {} days:".format(day), fish_list)
"""
print(len(lanternfish_after_days(fish_list, 256)))
