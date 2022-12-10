import sys
import os


def get_data_lines(my_file):
    with open(my_file) as f:
        lines = f.readlines()
    return [line.strip('\n').strip() for line in lines]


def get_cpu_values(lines):
    cpu_values = [1]
    current = 1
    for line in lines:
        if line == 'noop':
            cpu_values.append(current)
        else:
            first, second = line.split()
            cpu_values.append(current)
            current += int(second)
            cpu_values.append(current)
    return cpu_values


def get_signal_strength(cpu_values):
    number_of_forties = len(cpu_values) // 40
    signal_strength = 0
    for n in range(number_of_forties):
        signal_strength += cpu_values[40 * n + 19] * (20 + 40 * n)

    return signal_strength


def is_crt_within_sprite(crt, sprite_middle):
    return sprite_middle - 1 <= crt <= sprite_middle + 1


def get_image(cpu_values):
    image = ''
    for row in range(6):
        for column in range(40):
            crt_position = 40 * row + column
            sprite_position = cpu_values[crt_position]
            if is_crt_within_sprite(column, sprite_position):
                image += '#'
            else:
                image += '.'
        image += '\n'
    return image


def main(my_file):
    lines = get_data_lines(my_file)
    cpu_values = get_cpu_values(lines)

    print("part 1:", get_signal_strength(cpu_values))
    print("part 2:")
    print(get_image(cpu_values))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = f'{os.path.basename(__file__)[:2]}_input.txt'
    main(filename)
