import sys


def get_commands(my_file):
    with open(my_file) as f:
        commands = list()
        lines = f.readlines()
        for line in lines:
            line = line.strip().split()
            command = list()
            for elt in line:
                if elt.isalpha():
                    command.append(elt)
                else:
                    command.append(int(elt))
            commands.append(command)
    return commands


def single_command(command, a, b, c, d):
    registers = {"a": a, "b": b, "c": c, "d": d}
    index = 0
    command_type = command[0]
    if command_type == "cpy":
        registers[command[2]] = registers.get(command[1], command[1])
    elif command_type == "inc":
        registers[command[1]] += 1
    elif command_type == "dec":
        registers[command[1]] -= 1
    elif command_type == "jnz" and registers.get(command[1], command[1]) != 0:
        index = command[2]
    return registers["a"], registers["b"], registers["c"], registers["d"], index


def get_a_from_all_commands(commands, part):
    many = len(commands)
    a, b, c, d, index = 0, 0, part - 1, 0, 0
    while True:
        if index >= many:
            break
        elif index == 10:
            a += b
            b = 0
            index = 13
        command = commands[index]
        a, b, c, d, ind = single_command(command, a, b, c, d)
        if ind != 0:
            index += ind
        else:
            index += 1
    return a


def main(my_file):
    commands = get_commands(my_file)
    for part in {1, 2}:
        print(f"part {part}: {get_a_from_all_commands(commands, part)}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
    else:
        file_name = "12_input.txt"
    main(file_name)
