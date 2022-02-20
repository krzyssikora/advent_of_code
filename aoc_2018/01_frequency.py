import sys


def get_frequencies(my_file):
    with open(my_file) as f:
        lines = f.readlines()
    frequencies = list()
    for line in lines:
        frequencies.append(int(line.strip()))
    return frequencies


def find_double(frequencies):
    obtained = set()
    current = 0
    while True:
        for frequency in frequencies:
            current += frequency
            if current in obtained:
                return current
            obtained.add(current)


def main(my_file):
    frequencies = get_frequencies(my_file)
    print("part 1:", sum(frequencies))
    print("part 2:", find_double(frequencies))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "01_input.txt"
    main(filename)
