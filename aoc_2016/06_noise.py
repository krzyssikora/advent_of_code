import sys


def main(my_file):
    lines = open(my_file).readlines()
    length = len(lines[0].strip())
    frequencies = [dict() for _ in range(length)]
    for line in lines:
        for ind in range(length):
            frequencies[ind][line[ind]] = frequencies[ind].get(line[ind], 0) + 1
    word_max = ""
    word_min = ""
    for ind in range(length):
        freq_dict = frequencies[ind]
        word_max += max(freq_dict.items(), key=lambda x: x[1])[0]
        word_min += min(freq_dict.items(), key=lambda x: x[1])[0]
    print("part 1:", word_max)
    print("part 2:", word_min)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "06_input.txt"
    main(filename)
