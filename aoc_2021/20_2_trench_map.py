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


def add_borders(input_image, offset=2, outer_char="."):
    columns = len(input_image[0])
    output_image = list()
    # add top row
    for _ in range(offset):
        output_image.append(outer_char * (columns + 2 * offset))
    for row in input_image:
        output_image.append(outer_char * offset + row + outer_char * offset)
    for _ in range(offset):
        output_image.append(outer_char * (columns + 2 * offset))
    return output_image


def image_dimensions(my_image):
    return str(len(my_image))+"x"+str(len(my_image[0]))


def change_string_into_number(pixel_string):
    binary_string = ""
    for character in pixel_string:
        if character == "#":
            binary_string += "1"
        elif character == ".":
            binary_string += "0"
    return int(binary_string, 2)


def get_output_string(input_image, row, column, outer_char):
    rows = range(len(input_image))
    columns = range(len(input_image[0]))
    output_string = ""
    for r in range(row - 1, row + 2):
        for c in range(column - 1, column + 2):
            if r in rows and c in columns:
                output_string += input_image[r][c]
            else:
                output_string += outer_char
    return output_string


def get_output_image(input_image, algorithm, outer_char):
    my_image = add_borders(input_image, offset=1, outer_char=outer_char)
    output_image = list()
    rows = range(len(my_image))
    columns = range(len(my_image[0]))
    for row in rows:
        output_row = ""
        for column in columns:
            output_string = get_output_string(my_image, row, column, outer_char)
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
    a0 = algorithm[0]
    if a0 == ".":
        a1 = a0
    else:
        a1 = algorithm[511]
    outer_char = "."
    for step in range(50):
        input_image = get_output_image(input_image, algorithm, outer_char)
        print(step, ":", light_pixels(input_image), "(" + image_dimensions(input_image) + ")")
        if outer_char == a0:
            outer_char = a1
        else:
            outer_char = a0
    print(light_pixels(input_image))


if __name__ == "__main__":
    if len(sys.argv) == 2:
        filename = sys.argv[1]
    elif len(sys.argv) == 3:
        filename = ""
    else:
        filename = "20_input.txt"
    main(filename)
