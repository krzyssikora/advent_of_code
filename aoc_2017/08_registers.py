import sys


def get_commands(my_file):
    commands = list()
    with open(my_file) as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip().split()
            commands.append(line[:2] + [int(line[2])] + line[4:6] + [int(line[-1])])
    return commands


def apply_commands(commands):
    registers = dict()
    maximum = 0
    for command in commands:
        register, action, action_value, cond_register, condition, cond_value = command
        cond_register_value = registers.get(cond_register, 0)
        if condition == "==":
            make_action = (cond_register_value == cond_value)
        elif condition == ">=":
            make_action = (cond_register_value >= cond_value)
        elif condition == "<=":
            make_action = (cond_register_value <= cond_value)
        elif condition == "!=":
            make_action = (cond_register_value != cond_value)
        elif condition == ">":
            make_action = (cond_register_value > cond_value)
        elif condition == "<":
            make_action = (cond_register_value < cond_value)
        else:
            make_action = False
        sign = 1 if action == "inc" else -1
        if make_action:
            registers[register] = registers.get(register, 0) + sign * action_value
            if registers[register] > maximum:
                maximum = registers[register]
    return registers, maximum


def main(my_file):
    commands = get_commands(my_file)
    registers, maximum = apply_commands(commands)
    print("part 1:", max(registers.values()))
    print("part 2:", maximum)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "08_input.txt"
    main(filename)
