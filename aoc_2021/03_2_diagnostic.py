input_data = "input.txt"
initial_number_length = len("110000000001")
with open(input_data) as f:
    number_length = initial_number_length
    lines = f.readlines()
    lines = [x.strip("\n") for x in lines]
    bit = 0
    while True:
        if len(lines) == 1:
            break
        if bit >= number_length:
            raise Exception("did not work")
        frequencies = dict()
        for line in lines:
            frequencies[line[bit]] = frequencies.get(line[bit], 0) + 1
        if frequencies.get("0", 0) > frequencies.get("1", 0):
            pivot_char = "0"
        else:
            pivot_char = "1"
        old_lines = lines.copy()
        lines = list()
        for line in old_lines:
            if line[bit] == pivot_char:
                lines.append(line)
        bit += 1
    oxygen_generator_string = lines[0]
    oxygen_generator_rating = int(oxygen_generator_string, 2)
with open(input_data) as f:
    number_length = initial_number_length
    lines = f.readlines()
    lines = [x.strip("\n") for x in lines]
    bit = 0
    while True:
        if len(lines) == 1:
            break
        if bit >= number_length:
            raise Exception("did not work")
        frequencies = dict()
        for line in lines:
            frequencies[line[bit]] = frequencies.get(line[bit], 0) + 1
        if frequencies.get("0", 0) <= frequencies.get("1", 0):
            pivot_char = "0"
        else:
            pivot_char = "1"
        old_lines = lines.copy()
        lines = list()
        for line in old_lines:
            if line[bit] == pivot_char:
                lines.append(line)
        bit += 1
    CO2_scrubber_string = lines[0]
    CO2_scrubber_rating = int(CO2_scrubber_string, 2)
print(oxygen_generator_rating * CO2_scrubber_rating)
