import sys


def get_data_lines(my_file):
    with open(my_file) as f:
        lines = f.readlines()
    return [line.strip('\n').strip() for line in lines]


def get_all_sums(lines):
    current_sum = 0
    sums = list()
    for line in lines:
        try:
            value = int(line)
            current_sum += value
        except ValueError:
            sums.append(current_sum)
            current_sum = 0
    return sums


def main(my_file):
    lines = get_data_lines(my_file)
    sums = get_all_sums(lines)
    sums.sort()

    print("part 1:", max(sums))
    print("part 2:", sum(sums[-3:]))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "01_input.txt"
    main(filename)
