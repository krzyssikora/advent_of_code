import sys


def get_string_from_file(my_file):
    ret_string = ""
    with open(my_file) as f:
        lines = f.readlines()
        for line in lines:
            ret_string += line.strip("\n")
    return ret_string


def get_list_from_file(my_file):
    ret_list = list()
    with open(my_file) as f:
        lines = f.readlines()
        for line in lines:
            ret_list.append(line.strip("\n"))
    return ret_list


def first_check(line):
    counts = 0
    vowels = "aeiou"
    for vowel in vowels:
        if vowel in line:
            counts += line.count(vowel)
    if counts >= 3:
        return True
    else:
        return False


def second_check(line):
    for i in range(len(line) - 1):
        if line[i] == line[i + 1]:
            return True
    return False


def third_check(line):
    forbidden = ["ab", "cd", "pq", "xy"]
    for letters in forbidden:
        if letters in line:
            return False
    return True


def fourth_check(line):
    for i in range(len(line) - 2):
        letters = line[i] + line[i + 1]
        more = line.find(letters, i + 2)
        if more >= 0:
            return True
    return False


def fifth_check(line):
    for i in range(len(line) - 2):
        if line[i] == line[i + 2]:
            return True
    return False


def main(my_file):
    lines = get_list_from_file(my_file)
    nice_lines = 0
    for line in lines:
        if fourth_check(line) and fifth_check(line):
            nice_lines += 1
    print(nice_lines)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "05_input.txt"
    main(filename)
