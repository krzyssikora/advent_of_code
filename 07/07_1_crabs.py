input_data = "input.txt"


def sum_of_distances(position, crab_list):
    total = 0
    for crab in crab_list:
        total += abs(crab - position)
    return total


def main():
    with open(input_data) as f:
        all_data = list(map(int, f.readline().split(",")))
        max_distance = max(all_data)
        distances = list()
        for i in range(max_distance + 1):
            # print("total distance from {} is {}".format(i, sum_of_distances(i, all_data)))
            distances.append(sum_of_distances(i, all_data))
        print(min(distances))

if __name__ == "__main__":
    main()