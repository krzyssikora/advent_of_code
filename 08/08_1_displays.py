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


def how_many_unique_patterns(input_list):
    count = 0
    for line in input_list:
        for code in line:
            if len(code) in {2, 3, 4, 7}:
                count += 1
    return count


def main():
    patterns, outputs = get_patterns_and_outputs("08_input.txt")
    print(how_many_unique_patterns(outputs))


if __name__ == "__main__":
    main()
