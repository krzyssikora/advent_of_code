import math


def single_step(a_string):
    a_int = int(a_string, 2)
    b_int_ = 2 ** len(a_string) - a_int - 1
    b_string = bin(b_int_)[2:]
    b_string = "0" * (len(a_string) - len(b_string)) + b_string
    b_string = b_string[::-1]
    return a_string + "0" + b_string


def checksum(string):
    str_list = list()
    length = len(string)
    if length % 2 != 0:
        return string
    for left, right in zip(string[::2], string[1::2]):
        if left == right:
            str_list.append("1")
        else:
            str_list.append("0")
    return checksum("".join(str_list))


def main():
    string = "01000100010010111"
    parts = [(1, 272), (2, 35651584)]
    for part, length in parts:
        steps = math.ceil(math.log((length + 1)/(len(string) + 1), 2))
        for _ in range(steps):
            string = single_step(string)
        string = string[:length]
        print(f"part {part}:", checksum(string))


if __name__ == "__main__":
    main()
