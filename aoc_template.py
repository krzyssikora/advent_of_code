import sys


def get_data_lines(my_file):
    with open(my_file) as f:
        lines = f.readlines()
    return [line.strip() for line in lines]


def main(my_file):
    lines = get_data_lines(my_file)

    print("part 1:", )
    print("part 2:", )


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "01_input.txt"
    main(filename)
