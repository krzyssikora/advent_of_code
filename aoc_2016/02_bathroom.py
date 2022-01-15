import sys


def find_code_1(commands):
    code = 0
    decode = [[1, 2, 3],
              [4, 5, 6],
              [7, 8, 9]]
    horizontal, vertical = 1, 1
    for command in commands:
        command = command.strip()
        for letter in command:
            if letter == "L":
                horizontal = max(0, horizontal - 1)
            elif letter == "R":
                horizontal = min(2, horizontal + 1)
            elif letter == "U":
                vertical = max(0, vertical - 1)
            elif letter == "D":
                vertical = min(2, vertical + 1)
        code = 10 * code + decode[vertical][horizontal]
    return code


def find_code_2(commands):
    def outside(h, v):
        if h + v in {1, 7} or h - v in {-3, 3}:
            return True
        else:
            return False

    code = ""
    decode = [[None, None, 1, None, None],
              [None, 2, 3, 4, None],
              [5, 6, 7, 8, 9],
              [None, "A", "B", "C", None],
              [None, None, "D", None, None]]
    horizontal, vertical = 0, 2
    for command in commands:
        command = command.strip()
        for letter in command:
            if letter == "L":
                horizontal = max(0, horizontal - 1)
                if outside(horizontal, vertical):
                    horizontal += 1
            elif letter == "R":
                horizontal = min(4, horizontal + 1)
                if outside(horizontal, vertical):
                    horizontal -= 1
            elif letter == "U":
                vertical = max(0, vertical - 1)
                if outside(horizontal, vertical):
                    vertical += 1
            elif letter == "D":
                vertical = min(4, vertical + 1)
                if outside(horizontal, vertical):
                    vertical -= 1
        code = code + str(decode[vertical][horizontal])
    return code


def main(my_file):
    commands = open(my_file).readlines()
    print(find_code_1(commands))
    print(find_code_2(commands))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "02_input.txt"
    main(filename)
