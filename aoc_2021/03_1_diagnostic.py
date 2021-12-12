with open("input.txt") as f:
    number_length = len("110000000001")
    lines = f.readlines()
    frequencies = [dict() for _ in range(number_length)]
    for line in lines:
        for bit in range(number_length):
            frequencies[bit][line[bit]] = frequencies[bit].get(line[bit], 0) + 1
    # frequencies collected
    gamma_string = ""
    epsilon_string = ""
    for bit in range(number_length):
        if frequencies[bit].get("0", 0) > frequencies[bit].get("1", 0):
            gamma_string += "0"
            epsilon_string += "1"
        else:
            gamma_string += "1"
            epsilon_string += "0"
    gamma_rate = int(gamma_string, 2)
    epsilon_rate = int(epsilon_string, 2)
    print(gamma_string, epsilon_string)
    print(gamma_rate * epsilon_rate)
