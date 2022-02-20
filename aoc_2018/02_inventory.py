import sys


def get_ids(my_file):
    with open(my_file) as f:
        lines = f.readlines()
    return [line.strip() for line in lines]


def twos_threes(idx):
    freq_dict = dict()
    for ch in idx:
        freq_dict[ch] = freq_dict.get(ch, 0) + 1
    frequencies = list(freq_dict.values())
    two = 1 if 2 in frequencies else 0
    three = 1 if 3 in frequencies else 0
    return two, three


def checksum(ids):
    twos, threes = 0, 0
    for idx in ids:
        two, three = twos_threes(idx)
        twos += two
        threes += three
    return twos * threes


def differences(string_1, string_2):
    chars_number = len(string_1)
    i = 0
    diffs = 0
    while True:
        if diffs > 1 or i >= chars_number:
            break
        if string_1[i] != string_2[i]:
            diffs += 1
        i += 1
    return diffs


def similar_ids(ids):
    ids_number = len(ids)
    for i in range(ids_number):
        for j in range(i + 1, ids_number):
            if differences(ids[i], ids[j]) == 1:
                return i, j
    return None, None


def same_chars(ids):
    id_1, id_2 = similar_ids(ids)
    string_1, string_2 = ids[id_1], ids[id_2]
    ret_string = ""
    for ch_1, ch_2 in zip(string_1, string_2):
        if ch_1 == ch_2:
            ret_string += ch_1
    return  ret_string


def main(my_file):
    ids = get_ids(my_file)
    print("part 1:", checksum(ids))
    print("part 2:", same_chars(ids))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "02_input.txt"
    main(filename)
