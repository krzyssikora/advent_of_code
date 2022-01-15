import sys
import re


def get_room_codes(my_file):
    codes = list()
    with open(my_file) as f:
        lines = f.readlines()
        for line in lines:
            code = re.findall(r"([-a-z]+)-([0-9]+)\[([a-z]+)]", line)[0]
            codes.append([code[0], code[2], int(code[1])])
    return codes


def room_real(room_code):
    freq_dict = dict()
    for char in room_code[0]:
        if char == "-":
            continue
        freq_dict[char] = freq_dict.get(char, 0) + 1
    freq_list = list(freq_dict.items())
    freq_list.sort(key=lambda x: x[0])
    freq_list.sort(key=lambda x: x[1], reverse=True)
    expected_checksum = ""
    for i in range(min(5, len(freq_list))):
        expected_checksum += freq_list[i][0]
    if expected_checksum == room_code[1]:
        return True
    else:
        return False


def room_name(room_code):
    shift = room_code[2]
    name = ""
    for char in room_code[0]:
        if char == "-":
            name += " "
        else:
            name += chr((ord(char) - 97 + shift) % 26 + 97)
    return name


def real_room_sector_id(room_code):
    if room_real(room_code):
        return room_code[2]
    else:
        return 0


def main(my_file):
    room_codes = get_room_codes(my_file)
    print("part 1")
    total = 0
    for code in room_codes:
        total += real_room_sector_id(code)
    print(total)
    print("part 2")
    for code in room_codes:
        if room_real(code):
            name = room_name(code)
            if "north" in name:
                print(room_name(code) + ", ID:", code[2])


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "04_input.txt"
    main(filename)
