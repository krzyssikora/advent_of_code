import sys


def main(my_file):
    with open(my_file) as f:
        lines = f.readlines()
        total = 0
        for line in lines:
            total += 2 + line.count("\\") + line.count("\"")
        print(total)
        print(sum(2+s.count('\\')+s.count('"') for s in open(my_file)))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "08_input.txt"
    main(filename)
