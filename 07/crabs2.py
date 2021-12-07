input_data = "input.txt"


def sum_of_fuel_usages(position, crab_list):
    total = 0
    for crab in crab_list:
        distance = abs(crab - position)
        total += distance * (distance + 1) // 2
    return total


def main():
    with open(input_data) as f:
        all_data = list(map(int, f.readline().split(",")))
        max_distance = max(all_data)
        fuel_usage = list()
        for i in range(max_distance + 1):
            # print("total fuel usage from {} is {}".format(i, sum_of_fuel_usages(i, all_data)))
            fuel_usage.append(sum_of_fuel_usages(i, all_data))
        print(min(fuel_usage))


if __name__ == "__main__":
    main()
    