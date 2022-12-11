import sys
import os


operations_dict = {
    '*': int.__mul__,
    '+': int.__add__,
    '-': int.__sub__,
    '**': int.__rpow__
}


def get_data_lines(my_file):
    with open(my_file) as f:
        lines = f.readlines()
    return [line.strip('\n').strip() for line in lines]


def get_monkey_item(lines, line_idx):
    monkey_item = dict()

    line = lines[line_idx]
    line_idx += 1
    monkey_id = int(line.split()[1].strip(':'))

    line = lines[line_idx]
    line_idx += 1
    worry_levels = list(map(int, line.split(': ')[1].split(', ')))
    monkey_item['worry'] = worry_levels

    line = lines[line_idx]
    line_idx += 1
    old, operation, factor = line.split(' = ')[1].split()
    if factor == 'old':
        operation = '**'
        factor = 2
    monkey_item['operation'] = (operations_dict[operation], int(factor))

    line = lines[line_idx]
    line_idx += 1
    monkey_item['test'] = int(line.split()[-1])

    line = lines[line_idx]
    line_idx += 1
    monkey_item[True] = int(line.split()[-1])

    line = lines[line_idx]
    line_idx += 1
    monkey_item[False] = int(line.split()[-1])

    monkey_item['inspections'] = 0

    return monkey_id, monkey_item, line_idx


def get_monkey_dict(lines):
    line_idx = 0
    monkey_dict = dict()
    while True:
        if line_idx >= len(lines):
            break

        line = lines[line_idx]
        if line.startswith('Monkey'):
            monkey_id, monkey_item, line_idx = get_monkey_item(lines, line_idx)
            monkey_dict[monkey_id] = monkey_item
        else:
            line_idx += 1

    return monkey_dict


def make_turn(monkey_dict, monkey_id, mod_value, reduce=True):
    monkey = monkey_dict[monkey_id]
    for item in monkey['worry']:
        operation, factor = monkey['operation']
        new = operation(factor, item) % mod_value
        new = new // 3 if reduce else new
        test_passed = new % monkey['test'] == 0
        recipient_id = monkey[test_passed]
        monkey_dict[recipient_id]['worry'].append(new)
        monkey['inspections'] += 1
    monkey['worry'] = list()
    return monkey_dict


def make_a_round(monkey_dict, mod_value, reduce=True):
    monkey_ids = list(range(len(monkey_dict)))
    for monkey_id in monkey_ids:
        monkey_dict = make_turn(monkey_dict, monkey_id, mod_value, reduce)
    return monkey_dict


def make_rounds(monkey_dict, n, mod_value, reduce=True):
    for _ in range(n):
        monkey_dict = make_a_round(monkey_dict, mod_value, reduce)
    return monkey_dict


def display_monkeys(monkey_dict):
    monkey_ids = list(range(len(monkey_dict)))
    for monkey_id in monkey_ids:
        print(f'{monkey_id}: {", ".join(map(str, monkey_dict[monkey_id]["worry"]))} // {monkey_dict[monkey_id]["inspections"]}')


def get_product_of_two_max_inspections(monkey_dict):
    monkey_ids = list(range(len(monkey_dict)))
    inspections = [monkey_dict[monkey_id]['inspections'] for monkey_id in monkey_ids]
    inspections.sort(reverse=True)
    return inspections[0] * inspections[1]


def get_mod_value(monkey_dict):
    product = 1
    for m in monkey_dict:
        product *= monkey_dict[m]['test']
    return product


def main(my_file):
    lines = get_data_lines(my_file)

    monkey_dict = get_monkey_dict(lines)
    mod_value = get_mod_value(monkey_dict)
    monkey_dict = make_rounds(monkey_dict, 20, mod_value)
    print("part 1:", get_product_of_two_max_inspections(monkey_dict))

    monkey_dict = get_monkey_dict(lines)
    mod_value = get_mod_value(monkey_dict)
    monkey_dict = make_rounds(monkey_dict, 10000, mod_value, False)
    print("part 2:", get_product_of_two_max_inspections(monkey_dict))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = f'{os.path.basename(__file__)[:2]}_input.txt'
    main(filename)
