import hashlib


def md5_hash(string, many=1):
    for _ in range(many):
        string = hashlib.md5(string.encode()).hexdigest()
    return string.lower()


def freq_dict(string):
    ret = dict()
    for order in range(97, 123):
        character = chr(order)
        count = string.count(character)
        if count >= 5:
            ret[character] = count
    for order in range(48, 58):
        character = chr(order)
        count = string.count(character)
        if count >= 5:
            ret[character] = count
    if len(ret) == 0:
        ret = None
    return ret


def get_fives(string):
    ret = set()
    length = len(string)
    for ind in range(length - 4):
        if any([string[ind] != string[ind + i] for i in range(1, 5)]):
            continue
        else:
            ret.add(string[ind])
    if len(ret) == 0:
        ret = None
    return ret


def first_three(string):
    length = len(string)
    for ind in range(length - 2):
        if string[ind] != string[ind + 1]:
            continue
        else:
            if string[ind] != string[ind + 2]:
                continue
            else:
                return string[ind]
    return None


def find_keys(salt, number_keys, iterations=1):
    number = 0
    keys = list()
    keys_ids = list()
    triples = list()  # md5 hashes with a sequence of 3 as tuples: (number, character)
    final_hash_id = -1
    while True:
        if number - 1000 > final_hash_id > 0 and len(keys) >= 64:
            break
        my_hash = md5_hash(salt + str(number), iterations)
        triple = first_three(my_hash)
        if triple:
            if triples:
                fives = get_fives(my_hash)
                if fives:
                    # there is a sequence of 5, so let's check all previous potential pads
                    triple_index = 0
                    while True:
                        if triple_index >= len(triples):
                            break
                        triple_number, triple_character = triples[triple_index]
                        if triple_number >= number:
                            break
                        if number - triple_number > 1000:
                            triples.remove((triple_number, triple_character))
                            continue
                        if triple_character in fives:
                            if triple_number not in keys_ids:
                                print(f"Key: {triple_number}, verified at: {number}, "
                                      f"repeating character: {triple_character}")
                                keys.append((triple_number, number, triple_character))
                                keys_ids.append(triple_number)
                                keys.sort()
                                if len(keys) < number_keys:
                                    final_hash_id = triple_number
                        triple_index += 1
            triples.append((number, triple))
        number += 1
    return keys


def main():
    # salt = "abc"
    salt = "ngcjuoqr"
    result = list()
    for part, iterations in [(1, 1), (2, 2017)]:
        print(f"part {part}:")
        result.append(find_keys(salt, 64, iterations))
    print()
    for part in [1, 2]:
        print(f"part {part}: {result[part - 1][63][0]}")


if __name__ == "__main__":
    main()
