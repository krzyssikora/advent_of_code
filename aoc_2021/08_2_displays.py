def get_patterns_and_outputs(my_file):
    with open(my_file) as f:
        lines = f.readlines()
        patterns = list()
        outputs = list()
        for line in lines:
            p, o = line.strip("\n").split("|")
            pattern = p.split()
            output = o.split()
            patterns.append(pattern)
            outputs.append(output)
    return patterns, outputs


def is_in(string_1, string_2):
    ret_bool = True
    for character in string_1:
        ret_bool = ret_bool and (character in string_2)
    return ret_bool


def translate(pattern):
    pattern = list(sorted(pattern, key=len, reverse=True))
    translation = [None for _ in range(10)]
    # 1, 4, 7, 8
    d_1478 = {2: 1, 4: 4, 3: 7, 7: 8}
    for code in pattern:
        if len(code) in d_1478:
            translation[d_1478.get(len(code))] = code
    for code in translation:
        if code:
            pattern.remove(code)
    # 9
    for code in pattern:
        if len(code) == 6 and is_in(translation[4], code):
            translation[9] = code
            break
    pattern.remove(code)
    # 0
    for code in pattern:
        if len(code) == 6 and is_in(translation[7], code):
            translation[0] = code
            break
    pattern.remove(code)
    # 3
    for code in pattern:
        if len(code) == 5 and is_in(translation[7], code):
            translation[3] = code
            break
    pattern.remove(code)
    # 6
    for code in pattern:
        if len(code) == 6:
            translation[6] = code
            break
    pattern.remove(code)
    # 5
    for code in pattern:
        if is_in(code, translation[9]):
            translation[5] = code
            break
    pattern.remove(code)
    # 2
    translation[2] = pattern[0]
    return_dict = dict()
    for code in translation:
        return_dict["".join(sorted(code))] = translation.index(code)
    return return_dict


def how_many_unique_patterns(input_list):
    count = 0
    for line in input_list:
        for code in line:
            if len(code) in {2, 3, 4, 7}:
                count += 1
    return count


def output_value(translation, output):
    ret_value = 0
    for i, code in enumerate(output):
        ret_value += 10 ** (3 - i) * translation.get("".join(sorted(code)))
    return ret_value


def main():
    patterns, outputs = get_patterns_and_outputs("08_input.txt")
    total = 0
    for pattern, output in zip(patterns, outputs):
        my_dict = translate(pattern)
        total += output_value(my_dict, output)
    print(total)



if __name__ == "__main__":
    main()
