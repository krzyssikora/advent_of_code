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


def insertion_step(template, rules):
    position = 0
    while True:
        if position > len(template) - 2:
            break
        if template[position: position + 2] in rules:
            template = template[: position + 1] \
                       + rules.get(template[position: position + 2], "") \
                       + template[position + 1:]
            position += 2
        else:
            position += 1
    return template


def frequencies_from_string(my_string):
    frequencies = dict()
    for letter in my_string:
        frequencies[letter] = frequencies.get(letter, 0) + 1
    return frequencies


def dictionary_range(my_dict):
    return max(my_dict.values()) - min(my_dict.values())


def insertion_steps(template, rules, steps):
    if steps == 1:
        return insertion_step(template, rules)
    else:
        return insertion_steps(insertion_step(template, rules), rules, steps - 1)


def main(my_file):
    rules, template = get_dict_from_data(my_file)
    output_string = insertion_steps(template, rules, 10)
    frequencies = frequencies_from_string(output_string)
    print(dictionary_range(frequencies))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "14_input.txt"
    main(filename)
