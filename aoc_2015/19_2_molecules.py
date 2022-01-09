import sys
import re


sys.setrecursionlimit(5000)


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


def get_translations(string, inp, out_elt):
    string_list = set()
    length = len(inp)
    p = re.compile("(" + inp + ")")
    positions = list()
    for m in p.finditer(string):
        positions.append(int(m.start()))
    for pos in positions:
        string_list.add(string[:pos] + out_elt + string[pos + length:])
    return string_list


def translate_back(replacements, string, iteration=0, final="e"):
    if string == final:
        return True, iteration
    outputs = set()
    replacements_keys = list(replacements.keys())
    replacements_keys.sort(key=len)
    for inp in replacements_keys:
        out_list = replacements[inp]
        outputs = outputs.union(get_translations(string, inp, out_list))
    for output in outputs:
        result = translate_back(replacements, output, iteration + 1, final=final)
        if result[0]:
            return True, result[1]
    return False, iteration


def main(my_file):
    replacements, inp_string = get_back_dict_and_string(my_file)
    print(translate_back(replacements, inp_string))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "19_input.txt"
    main(filename)
