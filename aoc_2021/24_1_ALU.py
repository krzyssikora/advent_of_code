import sys
import csv
import functools


def get_commands_from_data(my_file):
    with open(my_file) as f:
        lines = f.readlines()
        command_list = list()
        for line in lines:
            line = line.strip().split(" ")
            command_list.append([int(elt) if (elt.isdigit() or (elt[0] == "-" and elt[1:].isdigit()))
                                 else elt for elt in line])
    return command_list


def sole_commands_and_differences(my_file):
    command_list = list()
    with open(my_file) as f:
        for _ in range(14):
            commands_pile = list()
            for _ in range(18):
                line = f.readline().strip().split(" ")
                commands_line = list()
                for elt in line:
                    commands_line.append(int(elt) if (elt.isdigit() or (elt[0] == "-" and elt[1:].isdigit())) else elt)
                commands_pile.append(commands_line)
            command_list.append(commands_pile)
    sole_commands = list()
    differences = list()
    for j in range(18):
        command_list = [command_list[i][j] for i in range(14)]
        all_same = command_list.count(command_list[0]) == len(command_list)
        if all_same:
            sole_commands.append(command_list[0])
            differences.append(None)
        else:
            sole_commands.append(command_list[0][:-1])
            differences.append([command_list[i][-1] for i in range(14)])
    return sole_commands, differences


def save_to_csv(sole_commands, differences):
    with open('24_commands.csv', 'w', newline='') as csvfile:
        fieldnames = ['command', 'parameter1', "other"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for s, d in zip(sole_commands, differences):
            if d is None:
                if len(s) == 2:
                    writer.writerow({'command': str(s[0]), 'parameter1': str(s[1])})
                else:
                    writer.writerow({'command': str(s[0]), 'parameter1': str(s[1]), "other": str(s[2])})
            else:
                writer.writerow({'command': str(s[0]), 'parameter1': str(s[1]), "other": ",".join(map(str, d))})


@functools.cache
def read_command(op_index, w_value=0, x_value=0, y_value=0, z_value=0):
    global commands

    if z_value > 10 ** 6:
        return False, ""

    if op_index >= len(commands):
        return z_value == 0, ""

    values = {"w": w_value, "x": x_value, "y": y_value, "z": z_value}

    command = commands[op_index]
    if command[0] == "inp":
        # for w in range(9, 0, -1):  # for highest value
        for w in range(1, 10):  # for lowest value
            values[command[1]] = w
            result = read_command(op_index + 1, values["w"], values["x"], values["y"], values["z"])
            print(op_index, w_value, x_value, y_value, z_value, str(w) + result[1])
            if result[0]:
                return True, str(w) + result[1]
        return False, "0"
    else:
        value_1 = command[1]
        value_2 = values.get(command[2], command[2])
        if command[0] == "add":
            values[value_1] += value_2
        elif command[0] == "mul":
            values[value_1] *= value_2
        elif command[0] == "div":
            if value_2 == 0:
                return False, ""
            else:
                values[value_1] //= value_2
        elif command[0] == "mod":
            if values[value_1] < 0 or value_2 <= 0:
                return False, ""
            else:
                values[value_1] %= value_2
        elif command[0] == "eql":
            values[value_1] = 1 * (values[value_1] == value_2)
        return read_command(op_index + 1, values["w"], values["x"], values["y"], values["z"])


def test_input(string):
    global commands
    w = x = y = z = 0
    values = {"w": w, "x": x, "y": y, "z": z}
    str_index = 0
    for op_index in range(len(commands)):
        command = commands[op_index]
        if command[0] == "inp":
            values["w"] = int(string[str_index])
            print(str(op_index).rjust(3) +
                  ": w = " + str(values["w"]) + ", x = " + str(values["x"]) +
                  ", y = " + str(values["y"]) + ", z = " + str(values["z"]))
            str_index += 1
        else:
            value_1 = command[1]
            value_2 = values.get(command[2], command[2])
            if command[0] == "add":
                values[value_1] += value_2
            elif command[0] == "mul":
                values[value_1] *= value_2
            elif command[0] == "div":
                if value_2 == 0:
                    return False
                else:
                    values[value_1] //= value_2
            elif command[0] == "mod":
                if values[value_1] < 0 or value_2 <= 0:
                    return False
                else:
                    values[value_1] %= value_2
            elif command[0] == "eql":
                values[value_1] = 1 * (values[value_1] == value_2)
    return values["z"] == 0


def main(my_file):
    global commands
    commands = get_commands_from_data(my_file)
    """
    sole_commands, differences = sole_commands_and_differences(my_file)
    save_to_csv(sole_commands, differences)
    for s, d in zip(sole_commands, differences):
        print(s, d)
    for command in commands:
        print(command)
    """
    print(read_command(0, 0, 0, 0, 0))
#    print(test_input('59998426997979'))
#    print(test_input('13621111481315'))


if __name__ == "__main__":
    commands = list()
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "24_input.txt"
    main(filename)
