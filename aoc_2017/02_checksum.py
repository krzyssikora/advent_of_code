import sys


def part_1(lines):
    checksum = 0
    for line in lines:
        row = list(map(int, line.strip().split()))
        checksum += max(row) - min(row)
    return checksum


def part_2(lines):
    checksum = 0
    for line in lines:
        row = list(map(int, line.strip().split()))
        row.sort()
        found = False
        for i in range(len(row)):
            for j in range(i + 1, len(row)):
                if row[j] % row[i] == 0:
                    checksum += row[j] // row[i]
                    found = True
                    break
            if found:
                break
    return checksum


def main(my_file):
    with open(my_file) as f:
        lines = f.readlines()
    print("part 1:", part_1(lines))
    print("part 2:", part_2(lines))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "02_input.txt"
    main(filename)
