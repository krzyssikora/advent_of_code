import sys


def get_dict_from_data(my_file):
    rules = dict()
    template = ""
    with open(my_file) as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip("\n")
            if "->" in line:
                rules[line[:2]] = line[-1:]
            elif line != "":
                template = line
    return rules, template


def change_template_to_dict(my_string):
    my_dict = dict()
    for i in range(len(my_string) - 1):
        letters = my_string[i: i + 2]
        my_dict[letters] = my_dict.get(letters, 0) + 1
    return my_dict


def frequencies_from_string(my_string):
    frequencies = dict()
    for letter in my_string:
        frequencies[letter] = frequencies.get(letter, 0) + 1
    return frequencies


def frequencies_from_dict(my_dict, first, last):
    frequencies = dict()
    my_dict = {k: v for k, v in my_dict.items() if v > 0}
    for pair in my_dict:
        if pair[0] == pair[1]:
            frequencies[pair[0]] = frequencies.get(pair[0], 0) + my_dict[pair] * 2
        else:
            frequencies[pair[0]] = frequencies.get(pair[0], 0) + my_dict[pair]
            frequencies[pair[1]] = frequencies.get(pair[1], 0) + my_dict[pair]
    frequencies[first] = frequencies.get(first, 0) + 1
    frequencies[last] = frequencies.get(last, 0) + 1
    for letter in frequencies:
        frequencies[letter] = frequencies.get(letter) // 2
    return frequencies


def dictionary_range(my_dict):
    return max(my_dict.values()) - min(my_dict.values())


def insertion_step(my_dict, rules):
    # my dict is like: {pair of letters : frequency}
    my_dict = {k: v for k, v in my_dict.items() if v > 0}
    template = dict()  # dictionary of changes in pairs
    for pair in my_dict:
        if pair in rules:
            first = pair[0]
            last = pair[1]
            middle = rules.get(pair)
            template[first + middle] = template.get(first + middle, 0) + my_dict[pair]
            template[middle + last] = template.get(middle + last, 0) + my_dict[pair]
            template[pair] = template.get(pair, 0) - my_dict[pair]
    # merge changes into my_dict
    for pair in template:
        my_dict[pair] = my_dict.get(pair, 0) + template[pair]
    my_dict = {k: v for k, v in my_dict.items() if v > 0}
    return my_dict


def insertion_steps(template, rules, steps):
    if steps == 0:
        return template
    else:
        return insertion_steps(insertion_step(template, rules), rules, steps - 1)


def main(my_file):
    rules, template = get_dict_from_data(my_file)
    first = template[0]
    last = template[-1:]
    template = change_template_to_dict(template)
    template = insertion_steps(template, rules, 40)
    frequencies = frequencies_from_dict(template, first, last)
    print(dictionary_range(frequencies))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "14_input.txt"
    main(filename)
