import sys
import math


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
    return commands


def apply_command(command, registers, multiplications, count):
    if command[0] == "set":
        registers[command[1]] = registers.get(command[2], command[2])
    elif command[0] == "sub":
        registers[command[1]] -= registers.get(command[2], command[2])
    elif command[0] == "mul":
        multiplications += 1
        registers[command[1]] *= registers.get(command[2], command[2])
    elif command[0] == "jnz" and registers.get(command[1], command[1]) != 0:
        count += registers.get(command[2], command[2])
        return registers, multiplications, count
    count += 1
    return registers, multiplications, count


def part_two():
    b0 = 108400
    c = 125400
    h = 0
    for b in range(b0, c + 1, 17):
        f = 1
        for d in range(2, b + 1):
            if f == 0:
                break
            for e in range(2, b // d + 1):
                if d * e == b:
                    f = 0
                    break
        if f == 0:
            h += 1
    return h


def append_primes(primes, limit):
    suspect = primes[-1] + 2
    while True:
        is_prime = True
        if suspect > limit:
            break
        for prime in primes:
            if prime > math.ceil(math.sqrt(suspect)):
                break
            if suspect % prime == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(suspect)
        suspect += 2
    return primes


def part_two_optimised():
    b0 = 108400
    c = 125400
    h = 0
    primes = [2, 3]
    for b in range(b0, c + 1, 17):
        primes = append_primes(primes, b)
        if primes[-1] == b:
            continue
        else:
            h += 1
    return h


def main(my_file):
    commands = get_commands(my_file)
    commands_number = len(commands)
    registers = dict()
    for register in ["a", "b", "c", "d", "e", "f", "g", "h"]:
        registers[register] = 0
    # part 1
    count = 0
    multiplications = 0
    while True:
        registers, multiplications, count = apply_command(commands[count], registers, multiplications, count)
        if count >= commands_number:
            print("part 1:", multiplications)
            break
    print("part 2:", part_two_optimised())


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "23_input.txt"
    main(filename)
