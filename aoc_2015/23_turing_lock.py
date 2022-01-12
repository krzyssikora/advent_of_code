import sys


def get_commands(my_file):
    commands = list()
    with open(my_file) as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip().split(", ")
            first, second = line[0].split()
            if second not in {"a", "b"}:
                second = int(second)
            third = None
            if len(line) > 1:
                third = int(line[1])
            if third:
                commands.append([first, second, third])
            else:
                commands.append([first, second])
    return commands


def single_command(a, b, command):
    cmd = command[0]
    if cmd == "jmp":
        return a, b, command[1]
    register = a if command[1] == "a" else b
    if cmd == "hlf":
        register //= 2
    elif cmd == "tpl":
        register *= 3
    elif cmd == "inc":
        register += 1
    elif cmd == "jie" and register % 2 == 0:
        return a, b, command[2]
    elif cmd == "jio" and register == 1:
        return a, b, command[2]
    else:
        return a, b, 1
    if command[1] == "a":
        a = register
    else:
        b = register
    return a, b, 1


def main(my_file):
    commands = get_commands(my_file)
    length = len(commands)
    for part in [1, 2]:
        command_index = 0
        a = part - 1
        b = 0
        while True:
            if command_index >= length:
                break
            command = commands[command_index]
            a, b, offset = single_command(a, b, command)
            if a is None:
                break
            command_index += offset
        print("part", part, ":", b)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "23_input.txt"
    main(filename)
