import sys


def get_infected(my_file):
    infected = set()
    with open(my_file) as f:
        lines = f.readlines()
        dim = len(lines) // 2
        for row, line in enumerate(lines):
            for column, char in enumerate(line.strip()):
                if char == "#":
                    infected.add((column - dim, dim - row))
    return infected


def make_step(infected, current_position, direction_index, directions):
    burst = False
    if current_position in infected:
        direction_index = (direction_index + 1) % 4
        infected.remove(current_position)
    else:
        direction_index = (direction_index - 1) % 4
        infected.add(current_position)
        burst = True
    current_position = (current_position[0] + directions[direction_index][0],
                        current_position[1] + directions[direction_index][1])
    return infected, current_position, direction_index, burst


def make_evolved_step(infected, weakened, flagged, current_position, direction_index, directions):
    burst = False
    if current_position in infected:
        direction_index = (direction_index + 1) % 4
        infected.remove(current_position)
        flagged.add(current_position)
    elif current_position in weakened:
        weakened.remove(current_position)
        infected.add(current_position)
        burst = True
    elif current_position in flagged:
        direction_index = (direction_index + 2) % 4
        flagged.remove(current_position)
    else:
        direction_index = (direction_index - 1) % 4
        weakened.add(current_position)
    current_position = (current_position[0] + directions[direction_index][0],
                        current_position[1] + directions[direction_index][1])
    return infected, weakened, flagged, current_position, direction_index, burst


def main(my_file):
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    infected = get_infected(my_file)
    direction_index = 0
    current_position = (0, 0)
    bursts = 0
    for step in range(10000):
        infected, current_position, direction_index, burst = \
            make_step(infected, current_position, direction_index, directions)
        if burst:
            bursts += 1
    print("part 1:", bursts)
    infected = get_infected(my_file)
    weakened = set()
    flagged = set()
    direction_index = 0
    current_position = (0, 0)
    bursts = 0
    for step in range(10000000):
        infected, weakened, flagged, current_position, direction_index, burst = \
            make_evolved_step(infected, weakened, flagged, current_position, direction_index, directions)
        if burst:
            bursts += 1
    print("part 2:", bursts)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "22_input.txt"
    main(filename)
