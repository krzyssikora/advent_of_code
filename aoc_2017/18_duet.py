import sys


def get_commands(my_file):
    commands = list()
    registers = dict()
    with open(my_file) as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip().split()
            command = list()
            for elt in line:
                if elt.isalpha():
                    command.append(elt)
                else:
                    command.append(int(elt))
            register = command[1]
            if isinstance(register, str) and register not in registers:
                registers[register] = 0
            commands.append(command)
    return commands, registers


def apply_command_1(command, registers, frequency, count):
    if count == 4:
        count = 6
        registers["a"] = 2 ** registers["i"]
        registers["i"] = 0
        return registers, frequency, count
    if command[0] == "snd":
        frequency = registers.get(command[1], command[1])
    elif command[0] == "set":
        registers[command[1]] = registers.get(command[2], command[2])
    elif command[0] == "add":
        registers[command[1]] += registers.get(command[2], command[2])
    elif command[0] == "mul":
        registers[command[1]] *= registers.get(command[2], command[2])
    elif command[0] == "mod":
        registers[command[1]] %= registers.get(command[2], command[2])
    elif command[0] == "rcv" and command[1] != 0:
        return registers, frequency, None
    elif command[0] == "jgz" and registers.get(command[1], command[1]) > 0:
        count += registers.get(command[2], command[2])
        return registers, frequency, count
    count += 1
    return registers, frequency, count


def apply_command_2(command, registers, count):
    frequency = None
    if count == 4:
        count = 6
        registers["a"] = 2 ** registers["i"]
        registers["i"] = 0
        return registers, frequency, count
    if command[0] == "snd":
        frequency = registers.get(command[1], command[1])
    elif command[0] == "set":
        registers[command[1]] = registers.get(command[2], command[2])
    elif command[0] == "add":
        registers[command[1]] += registers.get(command[2], command[2])
    elif command[0] == "mul":
        registers[command[1]] *= registers.get(command[2], command[2])
    elif command[0] == "mod":
        registers[command[1]] %= registers.get(command[2], command[2])
    elif command[0] == "rcv":
        return registers, command[1], count
    elif command[0] == "jgz" and registers.get(command[1], command[1]) > 0:
        count += registers.get(command[2], command[2])
        return registers, frequency, count
    count += 1
    return registers, frequency, count


def main(my_file):
    commands, registers = get_commands(my_file)
    # part 1
    count = 0
    # registers["p"] = 1
    frequency = None
    while True:
        registers, frequency, count = apply_command_1(commands[count], registers, frequency, count)
        if count is None:
            print("part 1:", frequency)
            break
    # part 2
    program = 0
    one_sent = 0
    counts = [0, 0]
    values = [list(), list()]
    registers_names = sorted(list(registers.keys()))
    registers = [dict(), dict()]
    for register in registers_names:
        registers[0][register] = 0
        registers[1][register] = 0
    registers[1]["p"] = 1
    while True:
        while True:
            registers[program], received, counts[program] = \
                apply_command_2(commands[counts[program]], registers[program], counts[program])
            if isinstance(received, str):  # receive
                if len(values[program]) > 0:
                    registers[program][received] = values[program].pop(0)
                    counts[program] += 1
                else:
                    program = 1 - program
                    break
            elif isinstance(received, int):  # sent
                values[1 - program].append(received)
                if program == 1:
                    one_sent += 1
        if len(values[0]) + len(values[1]) == 0:
            break
    print("part 2:", one_sent)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "18_input.txt"
    main(filename)
