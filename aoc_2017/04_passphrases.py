import sys
import itertools


def get_data(my_file):
    phrases = list()
    with open(my_file) as f:
        lines = f.readlines()
        for line in lines:
            phrases.append(line.strip().split())
    return phrases


def valid_1(passphrases):
    number_valid = 0
    for phrase in passphrases:
        if len(phrase) == len(set(phrase)):
            number_valid += 1
    return number_valid


def are_anagrams(word_1, word_2):
    freq_1 = dict()
    freq_2 = dict()
    for letter in word_1:
        freq_1[letter] = freq_1.get(letter, 0) + 1
    for letter in word_2:
        freq_2[letter] = freq_2.get(letter, 0) + 1
    return freq_2 == freq_1


def valid_2(passphrases):
    number_valid = 0
    for phrase in passphrases:
        invalid = False
        combs = itertools.combinations(phrase, 2)
        for word_1, word_2 in combs:
            if are_anagrams(word_1, word_2):
                invalid = True
                break
        if not invalid:
            number_valid += 1
    return number_valid


def main(my_file):
    passphrases = get_data(my_file)
    for part, function in [[1, valid_1], [2, valid_2]]:
        print(f"part {part}", function(passphrases))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "04_input.txt"
    main(filename)
