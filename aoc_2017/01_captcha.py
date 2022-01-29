import sys


examples = [["1212", 6], ["1221", 0], ["123425", 4], ["123123", 12], ["12131415", 4]]


def solution(data, step):
    total = 0
    length = len(data)
    for i in range(len(data)):
        total += int(data[i]) * (data[i] == data[(i + step) % length])
    return total


def main(my_file):
    with open(my_file) as f:
        data = f.read().strip()
    length = len(data)
    for part, step in [[1, 1], [2, length // 2]]:
        print(f"part {part}:", solution(data, step))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "01_input.txt"
    main(filename)
