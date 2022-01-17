import sys


def get_instructions(my_file):
    bots_status = dict()
    instructions = dict()
    with open(my_file) as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip().split()
            if line[0] == "value":
                bot_number = int(line[5])
                if bot_number not in bots_status:
                    bots_status[bot_number] = list()
                bots_status[bot_number].append(int(line[1]))
            elif line[0] == "bot":
                bot_number = int(line[1])
                if bot_number in instructions:
                    print("import instructions error")
                    quit()
                low_destination = int(line[6]) if line[5] == "bot" else "output" + line[6]
                high_destination = int(line[11]) if line[10] == "bot" else "output" + line[11]
                instructions[bot_number] = {"low":  low_destination,
                                            "high": high_destination}
            else:
                print("import error")
                quit()
    return bots_status, instructions


def solve_part(part, bots_status, instructions):
    print("part", part)
    outputs = dict()
    current_boot, chips = max(bots_status.items(), key=lambda x: len(x[1]))
    potential_bots = {current_boot: chips.copy()}
    while True:
        if len(potential_bots) == 0:
            if part == 2:
                print(outputs[0] * outputs[1] * outputs[2])
            break
        current_boot = list(potential_bots.keys())[0]
        chips = potential_bots.pop(current_boot)
        if part == 1 and set(chips) == {17, 61}:
            print(current_boot)
            break
        low, high = min(chips), max(chips)
        low_destination = instructions[current_boot]["low"]
        high_destination = instructions[current_boot]["high"]
        for chip, destination in zip([low, high], [low_destination, high_destination]):
            if str(destination).startswith("output"):
                outputs[int(destination[6:])] = chip
            else:
                if destination not in bots_status:
                    bots_status[destination] = list()
                bots_status[destination].append(chip)
                if len(bots_status[destination]) > 1:
                    potential_bots[destination] = bots_status[destination].copy()


def main(my_file):
    bots_status, instructions = get_instructions(my_file)
    for part in {1, 2}:
        solve_part(part, bots_status, instructions)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "10_input.txt"
    main(filename)
