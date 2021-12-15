import sys


def is_digit(character):
    if len(character) > 1:
        character = character[0]
    return 48 <= ord(character) <= 57


def get_list_from_file(my_file):
    # returns a dictionary and a list:
    # the dictionary, inputs, consists of items:
    # wire: value
    # the list, instructions, consists of elements:
    # [command, input, output], where:
    # command = one of the bitwise operators' names
    # input = a wire (for NOT) or a list of wires / wire + value
    # output = a wire
    inputs = dict()
    instructions = list()
    with open(my_file) as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip("\n").split(" -> ")
            line_list = list()
            line_inputs = line[0].split(" ")
            if len(line_inputs) == 1:
                # either just assignment or just a number
                if is_digit(line[0][0]):
                    # must be just a number
                    inputs[line[1]] = int(line[0])
                else:
                    line_list = ["", line[0], line[1]]
            elif len(line_inputs) == 2:
                # must be NOT
                line_list = [line_inputs[0], line_inputs[1], line[1]]
            elif len(line_inputs) == 3:
                if is_digit(line_inputs[0][0]):
                    left_arg = int(line_inputs[0])
                else:
                    left_arg = line_inputs[0]
                if is_digit(line_inputs[2][0]):
                    right_arg = int(line_inputs[2])
                else:
                    right_arg = line_inputs[2]
                line_list = [line_inputs[1], [left_arg, right_arg], line[1]]
            if len(line_list) > 0:
                instructions.append(line_list)
    return inputs, instructions


def get_args_fixed(arguments, values):
    if isinstance(arguments, list):
        return [get_args_fixed(arguments[0], values), get_args_fixed(arguments[1], values)]
    elif isinstance(arguments, int):
        return arguments
    elif isinstance(arguments, str):
        return values.get(arguments, None)
    else:
        return None


def perform_operation(line, values):
    operation = line[0]
    arguments = get_args_fixed(line[1], values)
    output = line[2]
    if operation == "":
        values[output] = arguments
    elif operation == "NOT":
        values[output] = 2 ** 16 + ~arguments
    elif operation == "AND":
        values[output] = arguments[0] & arguments[1]
    elif operation == "OR":
        values[output] = arguments[0] | arguments[1]
    elif operation == "LSHIFT":
        values[output] = arguments[0] << arguments[1]
    elif operation == "RSHIFT":
        values[output] = arguments[0] >> arguments[1]
    else:
        print("wrong input")
        quit()
    return values


def tmp_operations(instructions):
    ret_list = list()
    for i in range(len(instructions)):
        if instructions[i][0] not in ret_list:
            ret_list.append(instructions[i][0])
    return ret_list


def main(my_file):
    inputs, instructions = get_list_from_file(my_file)
    inputs["b"] = 16076
    while True:
        if len(instructions) == 0:
            break
        line = instructions.pop()
        arguments = get_args_fixed(line[1], inputs)
        if arguments is None or (isinstance(arguments, list) and None in arguments):
            instructions = [line] + instructions
            continue
        inputs = perform_operation(line, inputs)
    print(inputs['a'])


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "07_input.txt"
    main(filename)
