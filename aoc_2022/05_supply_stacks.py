import sys
import os
import re


def get_data_lines(my_file):
    with open(my_file) as f:
        lines = f.readlines()
    return [line.strip('\n').rstrip() for line in lines]


def get_stacks_and_moves(lines):
    pattern = re.compile(r'move (\d+) from (\d+) to (\d+)')
    stacks = {_: list() for _ in range(1, 10)}
    moves = list()

    for line in lines:
        if line.endswith(']'):
            for stack_idx in range(1, 10):
                idx = 4 * stack_idx - 3
                if idx >= len(line):
                    break
                if line[idx] == ' ':
                    continue
                stacks[stack_idx].append(line[idx])

        if line.startswith('move'):
            many, stack_from, stack_to = map(int, re.findall(pattern, line)[0])
            moves.append((many, stack_from, stack_to))

    for stack_idx in stacks:
        stacks[stack_idx].reverse()

    return stacks, moves


def make_single_move(stacks, move, reverse_order=True):
    many, stack_from, stack_to = move
    supplies_staying, supplies_moving = stacks[stack_from][:-many], stacks[stack_from][-many:]
    stacks[stack_from] = supplies_staying
    if reverse_order:
        supplies_moving.reverse()
    stacks[stack_to] += supplies_moving


def make_moves(stacks, moves, reverse_order=True):
    for move in moves:
        make_single_move(stacks, move, reverse_order)

    top_supplies = [stacks[idx].pop() for idx in range(1, 10) if stacks[idx]]

    return ''.join(top_supplies)


def stacks_copy(initial_stacks):
    stacks = dict()
    for stack_idx in initial_stacks:
        stacks[stack_idx] = initial_stacks[stack_idx].copy()
    return stacks


def main(my_file):
    lines = get_data_lines(my_file)
    initial_stacks, moves = get_stacks_and_moves(lines)

    stacks = stacks_copy(initial_stacks)
    print("part 1:", make_moves(stacks, moves))
    stacks = stacks_copy(initial_stacks)
    print("part 2:", make_moves(stacks, moves, False))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = f'{os.path.basename(__file__)[:2]}_input.txt'
    main(filename)
