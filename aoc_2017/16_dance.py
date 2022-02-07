def read_commands(my_file):
    commands = list()
    with open(my_file) as f:
        data = f.read().strip()
    data = data.split(",")
    for elt in data:
        commands.append([elt[0]] + elt[1:].split("/"))
    return commands


def spin(string, value):
    return string[-value:] + string[:-value]


def exchange(string, pos_1, pos_2):
    if pos_1 > pos_2:
        pos_1, pos_2 = pos_2, pos_1
    return string[:pos_1] + string[pos_2] + string[pos_1 + 1:pos_2] + string[pos_1] + string[pos_2 + 1:]


def partner(string, char_1, char_2):
    return exchange(string, string.find(char_1), string.find(char_2))


def apply_commands(string, commands):
    for command in commands:
        if command[0] == "s":
            string = spin(string, int(command[1]))
        elif command[0] == "x":
            string = exchange(string, int(command[1]), int(command[2]))
        elif command[0] == "p":
            string = partner(string, command[1], command[2])
    return string


def main(my_file):
    commands = read_commands(my_file)
    string = ""
    for i in range(16):
        string += chr(ord("a") + i)
    new_string = apply_commands(string, commands)
    print("part 1:", new_string)
    counter = 1
    while True:
        new_string = apply_commands(new_string, commands)
        counter += 1
        if new_string == string:
            break
    many = 10 ** 9 % counter
    for _ in range(many):
        new_string = apply_commands(new_string, commands)
    print("part 2:", new_string)


if __name__ == "__main__":
    main("16_input.txt")
