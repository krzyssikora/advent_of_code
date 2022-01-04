import sys
import csv


def get_commands_from_data(my_file):
    with open(my_file) as f:
        commands = list()
        for _ in range(14):
            commands_pile = list()
            for _ in range(18):
                line = f.readline().strip().split(" ")
                commands_line = list()
                for elt in line:
                    commands_line.append(int(elt) if (elt.isdigit() or (elt[0] == "-" and elt[1:].isdigit())) else elt)
                commands_pile.append(commands_line)
            commands.append(commands_pile)
    return commands


def sole_commands_and_differences(command_list):
    sole_commands = list()
    differences = list()
    for j in range(18):
        print("command", str(j + 1).rjust(2), end=":")
        commands = [command_list[i][j] for i in range(14)]
        all_same = commands.count(commands[0]) == len(commands)
        if all_same:
            sole_commands.append(commands[0])
            differences.append(None)
        else:
            sole_commands.append(commands[0][:-1])
            differences.append([commands[i][-1] for i in range(14)])
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


def main(my_file):
    command_list = get_commands_from_data(my_file)
    sole_commands, differences = sole_commands_and_differences(command_list)
    save_to_csv(sole_commands, differences)
    for s, d in zip(sole_commands, differences):
        print(s, d)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "24_input.txt"
    main(filename)
