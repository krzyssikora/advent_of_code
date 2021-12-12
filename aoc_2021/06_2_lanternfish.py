input_data = "input.txt"
# make fish list
with open(input_data) as f:
    fish_list = f.readline().strip("\n").split(",")
    fish_list = [int(x) for x in fish_list]

# make fish dictionary
fish_dict = dict()
for fish in fish_list:
    fish_dict[fish] = fish_dict.get(fish, 0) + 1


def lanternfish_after_days(list_of_fish, days):
    if days == 1:
        return lanternfish_after_one_day(list_of_fish)
    else:
        return lanternfish_after_one_day(lanternfish_after_days(list_of_fish, days - 1))


def lanternfish_after_one_day(dict_of_fish):
    new_fish = dict()
    # changes
    # 0 -> 6, 8
    # 0 <= n <= 70:
    # n+1 -> n
    for days_left in range(8):
        new_fish[days_left] = dict_of_fish.get(days_left + 1, 0)
    if 0 in dict_of_fish:
        new_fish[6] = new_fish.get(6, 0) + dict_of_fish.get(0)
        new_fish[8] = dict_of_fish.get(0)
    return new_fish


for day in range(256):
    fish_dict = lanternfish_after_one_day(fish_dict)

# print("After {} days:".format(day + 1), fish_dict)
sum_of_fish = sum(fish_dict.values())
print(sum_of_fish)
