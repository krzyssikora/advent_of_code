import sys


def read_states(my_file):
    # states are kept in a dictionary
    # each state is a dictionary:
    # state: {value: [new_value, step = -1/1 for L/R, new_state], ...}
    states = dict()
    with open(my_file) as f:
        initial_state = f.readline().strip()[-2]
        steps = int(f.readline().strip().split()[-2])
        lines = f.readlines()
    idx = 0
    total = len(lines)
    while True:
        if idx >= total:
            break
        line = lines[idx].strip()
        if line.startswith("In state"):
            state = line[-2]
            states[state] = dict()
            for option in {0, 1}:
                data = list()
                data.append(int(lines[idx + 2].strip()[-2]))
                direction = lines[idx + 3].strip().split()[-1]
                if direction == "left.":
                    data.append(-1)
                elif direction == "right.":
                    data.append(1)
                data.append(lines[idx + 4].strip()[-2])
                states[state][option] = data
                idx += 4 + option
        else:
            idx += 1
    return states, initial_state, steps


def single_state(slots, state, current_position):
    new_value, step, new_state = state[slots.get(current_position, 0)]
    slots[current_position] = new_value
    current_position += step
    return slots, new_state, current_position


def main(my_file):
    states, state, steps = read_states(my_file)
    slots = {0: 0}
    current_position = 0
    for i in range(-3, 3):
        slots[i] = 0
    for step in range(steps):
        slots, state, current_position = single_state(slots, states[state], current_position)
    print(sum(slots.values()))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "25_input.txt"
    main(filename)
