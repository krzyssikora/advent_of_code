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


def single_command(commands, index, a, b, c, d):
    registers = {"a": a, "b": b, "c": c, "d": d}
    command = commands[index]
    command_type = command[0]
    if command_type == "cpy":
        registers[command[2]] = registers.get(command[1], command[1])
    elif command_type == "inc":
        registers[command[1]] += 1
    elif command_type == "dec":
        registers[command[1]] -= 1
    elif command_type == "jnz" and registers.get(command[1], command[1]) != 0:
        index += registers.get(command[2], command[2])
    elif command_type == "tgl":
        # TODO:
        # If toggling produces an invalid instruction (like cpy 1 2)
        # and an attempt is later made to execute that instruction, skip it instead.
        idx = index + registers.get(command[1])
        if idx < len(commands) and idx != index:
            tgld_command = commands[idx]
            if len(tgld_command) == 2:
                if tgld_command[0] == "inc":
                    tgld_command[0] = "dec"
                else:
                    tgld_command[0] = "inc"
            elif tgld_command[0] == "jnz":
                tgld_command[0] = "cpy"
            else:
                tgld_command[0] = "jnz"
    return registers["a"], registers["b"], registers["c"], registers["d"], commands, index


def get_a_from_all_commands(commands, part):
    many = len(commands)
    a, b, c, d, index = 7 + 5 * (part == 2), 0, 0, 0, 0
    count = 0
    while True:
        if index == 4 and d >= 0:
            a += b * d
            d = 0
            c = 0
            index += 6
        if index == 5:
            a += c
            c = 0
            index += 3
        count += 1
        if count % 1000000 == 0:
            print(str(count).rjust(6) + str(index).rjust(3) + " ".join(list(map(str, commands[index]))).rjust(10)
                  + str(a).rjust(10) + str(b).rjust(10) + str(c).rjust(10) + str(d).rjust(10))
        if index >= many:
            break
        a, b, c, d, commands, idx = single_command(commands, index, a, b, c, d)
        if index == idx:
            index += 1
        else:
            index = idx
    return a


def main(my_file):
    for part in {1, 2}:
        commands = get_commands(my_file)
        print(f"part {part}: {get_a_from_all_commands(commands, part)}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
    else:
        file_name = "23_input.txt"
    main(file_name)
