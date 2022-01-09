import sys
import re


sys.setrecursionlimit(10000)


def get_back_dict_and_string(my_file):
    with open(my_file) as f:
        replacements = dict()
        inp_string = ""
        lines = f.readlines()
        for line in lines:
            data = line.strip().split(" => ")
            if len(data) == 2:
                value, key = data
                replacements[key] = value
            else:
                inp_string += data[0]
    return replacements, inp_string


def get_dict_and_string(my_file):
    with open(my_file) as f:
        replacements = dict()
        inp_string = ""
        lines = f.readlines()
        for line in lines:
            data = line.strip().split(" => ")
            if len(data) == 2:
                key, value = data
                if key in replacements:
                    replacements[key].append(value)
                else:
                    replacements[key] = [value]
            else:
                inp_string += data[0]
    return replacements, inp_string


def get_translations(string, inp, out_list):
    string_list = set()
    length = len(inp)
    p = re.compile("(" + inp + ")")
    positions = list()
    for m in p.finditer(string):
        positions.append(int(m.start()))
    for pos in positions:
        for out in out_list:
            string_list.add(string[:pos] + out + string[pos + length:])
    return string_list


def how_many_outputs(replacements, inp_string):
    outputs = set()
    for inp, out_list in replacements.items():
        outputs = outputs.union(get_translations(inp_string, inp, out_list))
    return len(outputs)


def translate_back(replacements, string, iteration=0, final="e"):
    print(len(string), iteration)
    if string == final:
        print(iteration)
        return True
    outputs = set()
    for inp, out_list in replacements.items():
        outputs = outputs.union(get_translations(string, inp, out_list))
    for output in outputs:
        if iteration > 100:
            print("outputs:", len(outputs))
        if translate_back(replacements, output, iteration + 1):
            return True
    return False


def main(my_file):
    replacements, inp_string = get_dict_and_string(my_file)
    print(how_many_outputs(replacements, inp_string))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "19_input.txt"
    main(filename)
