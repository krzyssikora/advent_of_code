import sys


def get_algorithm_and_image(my_file):
    input_image = list()
    with open(my_file) as f:
        algorithm = f.readline().strip()
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            if line:
                input_image.append(line)
    return algorithm, input_image


def get_output_string(input_image, row, column, outer_char="."):
    rows = range(len(input_image))
    columns = range(len(input_image[0]))
    output_string = ""
    for r in range(row - 1, row + 2):
        for c in range(column - 1, column + 2):
            if c in columns and r in rows:
                output_string += input_image[r][c]
            else:
                output_string += outer_char
    return output_string


def image_dimensions(my_image):
    return len(my_image), len(my_image[0])


def change_string_into_number(pixel_string):
    binary_string = ""
    for character in pixel_string:
        if character == "#":
            binary_string += "1"
        elif character == ".":
            binary_string += "0"
    return int(binary_string, 2)


def get_output_image(input_image, algorithm, outer_char):
    output_image = list()
    rows = range(len(input_image) + 2)
    columns = range(len(input_image[0]) + 2)
    for row in rows:
        output_row = ""
        for column in columns:
            output_string = get_output_string(input_image, row - 1, column - 1, outer_char)
            output_row += algorithm[change_string_into_number(output_string)]
        output_image.append(output_row)
    return output_image


def light_pixels(my_image):
    count = 0
    for row in my_image:
        count += row.count("#")
    return count


def print_image(my_image):
    for row in my_image:
        print(row)
    print(image_dimensions(my_image))
    print()


def main(my_file):
    algorithm, input_image = get_algorithm_and_image(my_file)
    for _ in range(2):
        if _ == 0:
            outer_char = "."
        else:
            outer_char = algorithm[0]
        input_image = get_output_image(input_image, algorithm, outer_char)
    print(light_pixels(input_image))


if __name__ == "__main__":
    if len(sys.argv) == 2:
        filename = sys.argv[1]
    elif len(sys.argv) == 3:
        filename = ""
    else:
        filename = "20_input.txt"
    main(filename)
