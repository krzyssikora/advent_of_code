import sys


def main(my_file):
    with open(my_file) as f:
        lines = f.readlines()
        total = 0
        for line in lines:
            line = line.strip("\n")
            total += len(line) - len(eval(line))
        print(total)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "08_input.txt"
    main(filename)
