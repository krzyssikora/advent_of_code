import re
from pathlib import Path


def get_data_lines(my_file: Path) -> list:
    with open(my_file) as f:
        lines = f.readlines()
    return [line.strip('\n').strip() for line in lines]


def get_registers_and_program(lines):
    registers = {}
    program = []
    for line in lines:
        if not line:
            continue
        if m := re.match(r"Register ([A-C]{1}): (\d+)", line):
            registers[m.group(1)] = int(m.group(2))
        elif m := re.match(r"Program: ([\d,]+)", line):
            program = list(map(int, m.group(1).split(",")))
    return registers, program


def execute_program(registers, program, part=1):
    def combo(oprnd):
        return oprnd if oprnd < 4 else registers.get(["A", "B", "C"][oprnd - 4])

    def adv(oprnd, pointer, **kwargs):
        registers['A'] = registers['A'] >> combo(oprnd)
        pointer += 2
        return pointer
    
    def bxl(oprnd, pointer, **kwargs):
        registers["B"] = registers["B"] ^ oprnd
        pointer += 2
        return pointer
    
    def bst(oprnd, pointer, **kwargs):
        try:
            registers["B"] = combo(oprnd) % 8
        except TypeError:
            print(oprnd)
            print(registers)
            quit()
        pointer += 2
        return pointer
    
    def jnz(oprnd, pointer, **kwargs):
        if registers["A"]:
            pointer = oprnd
        else:
            pointer += 2
        return pointer
    
    def bxc(oprnd, pointer, **kwargs):
        registers["B"] = registers["B"] ^ registers["C"]
        pointer += 2
        return pointer
    
    def out(oprnd, pointer, part=1):
        output_list.append(combo(oprnd) % 8)
        if part == 2:
            min_len = min(len(output_list), len(program))
            if output_list[:min_len] != program[:min_len]:
                return -1
            elif output_list == program:
                return -2
        pointer += 2
        return pointer
    
    def bdv(oprnd, pointer, **kwargs):
        registers['B'] = registers['A'] >> combo(oprnd)
        pointer += 2
        return pointer
    
    def cdv(oprnd, pointer, **kwargs):
        registers['C'] = registers['A'] >> combo(oprnd)
        pointer += 2
        return pointer
    
    INSTRUCTIONS = {
        0: adv,
        1: bxl,
        2: bst,
        3: jnz,
        4: bxc,
        5: out,
        6: bdv,
        7: cdv,
    }
    output_list = []
    instruction_pointer = 0
    while instruction_pointer < len(program):
        instruction_number = program[instruction_pointer]
        operand = program[instruction_pointer + 1]
        instruction = INSTRUCTIONS[instruction_number]
        instruction_pointer = instruction(operand, instruction_pointer, part=part)
        if part == 2:
            if instruction_pointer == -1:
                return None
            if instruction_pointer == -2:
                return 'got it'
    if part == 2 and instruction_pointer >= len(program):
        return None
    return output_list


def get_initial_a_value(program, prefix="", a_value=0, idx=1):
    initial_digit = program[-idx]
    next_digits = []
    for digit in range(8):
        a_register = int(prefix + str(digit) + '0' * (15 - len(prefix)), 8)
        registers = {"A": a_register, "B": 0, "C": 0}
        output = execute_program(registers, program)
        if output[-idx] == initial_digit:
            next_digits.append(digit)

    if not next_digits:
        return -1
    for next_digit in next_digits:
        if idx == len(program):
            return 8 * a_value + next_digit
        possible_a_value = get_initial_a_value(program,
                                               prefix + str(next_digit),
                                               8 * a_value + next_digit,
                                               idx + 1)
        if possible_a_value > 0:
            return possible_a_value
    return -1


def main(my_file: Path, inp: int) -> None:
    lines = get_data_lines(my_file)
    registers, program = get_registers_and_program(lines)
    output_list = execute_program(registers, program)
    output = ",".join(map(str, output_list))
    a_register = get_initial_a_value(program)
    print(f"input {inp}:", output, a_register)


if __name__ == "__main__":
    root = Path(__file__).parent
    prefix = Path(__file__).name.split("_")[0]
    for inpt, filename in enumerate([f"{prefix}_input.txt"], 1):
        if (root / filename).exists():
            main(root / filename, inpt)
