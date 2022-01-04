import sys


def display_burrow(state):
    room_length = (len(state) - 7) // 4
    print("#" * 13)
    print("#" + state[0] + ".".join(list(state[1:6])) + state[6] + "#")
    for i in range(room_length):
        left = "###" if i == 0 else "  #"
        right = "###" if i == 0 else "#  "
        print(left + "#".join([state[7 + i + room_length * j] for j in range(4)]) + right)
    print("  " + "#" * 9 + "  ")


def get_data_from_file(my_file):
    burrow = "." * 7
    with open(my_file) as f:
        lines = f.readlines()
        rooms = list()
        for i in range(2, len(lines) - 1):
            rooms.append(lines[i][3:10:2])
        for i in range(4):
            for j in range(len(lines) - 3):
                burrow += rooms[j][i]
    return burrow


def single_move(state, i, j):
    i, j = min(i, j), max(i, j)
    return state[:i] + state[j] + state[i + 1:j] + state[i] + state[j + 1:]


def get_moves(hallway, room_no, room_pos):
    # returns the number of moves between hallway and room
    return abs(hallway - room_no) * 2 \
           + 4 * (room_no >= hallway) \
           - 2 * (hallway - room_no >= 2) \
           - 1 * (hallway in {0, 6}) \
           + room_pos


def go_home(state, cost):
    # if there is an option to move an amphipod from the hallway to its homeroom for good
    # (so that it will not heve to be removed again), return such final state and its cost
    costs = {"A": 1, "B": 10, "C": 100, "D": 1000}
    homerooms = {"A": 0, "B": 1, "C": 2, "D": 3}
    room_length = (len(state) - 7) // 4

    for hallway_position in range(7):
        if state[hallway_position] == ".":
            continue
        # first amphipod found
        amphipod = state[hallway_position]
        room = homerooms[amphipod]
        # check if home is ready to be moved to
        room_position = room_length - 1
        while room_position > 0 and state[7 + room_length * room + room_position] == amphipod:
            room_position -= 1
        if state[7 + room_length * room + room_position] != ".":
            continue  # a different type of amphipod found
        # now room_position points to where the amphipod from hallway can be moved
        # we need to see if the road is free
        # go right firstly, from the hallway to the homeroom
        pos = hallway_position
        while pos < room + 2 and state[pos + 1] == ".":
            pos += 1
        # now try left
        while pos > room + 1 and state[pos - 1] == ".":
            pos -= 1
        if pos == room + 1 or pos == room + 2:
            new_cost = get_moves(hallway_position, room, room_position) * costs[amphipod]
            new_state = single_move(state, hallway_position, 7 + room_length * room + room_position)
            return go_home(new_state, cost + new_cost)  # to move other amphipods from hallway to their homes
    return state, cost


def neighbours(state):
    # TODO: make elements of the list unique
    costs = {"A": 1, "B": 10, "C": 100, "D": 1000}
    homerooms = {"A": 0, "B": 1, "C": 2, "D": 3}
    room_length = (len(state) - 7) // 4
    neighbour_list = list()

    # IDEA: firstly move from homes to hallway and check if they can be moved to their proper homes

    # find a position of the first amphipod in a room to move out to the hallway
    for room in range(4):
        entrance = 7 + room_length * room
        room_position = 0
        while room_position < room_length and state[entrance + room_position] == ".":
            room_position += 1
        if room_position == room_length:  # nothing to move from this room
            continue
        amphipod = state[entrance + room_position]
        # an amphipod found. Should it be moved out?
        if room == homerooms[amphipod] and \
                all([state[entrance + i] == amphipod for i in range(room_position, room_length)]):
            continue  # all belong here, should not be moved out
        # amphipod from position (entrance + room_position) should be moved out. Where to?
        # note that for (room) the hallway positions
        # left and right from the entrance are (room + 1) and (room + 2) respectively
        # firstly check all possible positions right from the entrance
        right_position = room + 2
        while state[right_position] == "." and right_position < 7:
            right_cost = get_moves(right_position, room, room_position) * costs[amphipod]
            neighbour_list.append(go_home(single_move(state, entrance + room_position, right_position), right_cost))
            right_position += 1
        # now check all possible positions left from the entrance
        left_position = room + 1
        while state[left_position] == "." and left_position >= 0:
            left_cost = get_moves(left_position, room, room_position) * costs[amphipod]
            neighbour_list.append(go_home(single_move(state, entrance + room_position, left_position), left_cost))
            left_position -= 1
    return neighbour_list


def dijkstra(start, end):
    predecessors = {start: None}
    distances = {start: 0}  # {state: cost from state to start}
    queue = {0: [start]}  # {cost: list of states with this cost of getting to start}
    current_cost = 0
    while True:
        if current_cost % 10000 == 0 and current_cost > 0:
            print("Cost is more than", current_cost)
        current_states = queue.get(current_cost, [])
        for current_state in current_states:
            if current_state == end:
                return steps_list(predecessors, end), current_cost
            if distances.get(current_state) < current_cost:
                continue
            current_neighbours = neighbours(current_state)
            current_neighbours.sort(key=lambda x: x[1])
            for neighbour, neighbours_cost in current_neighbours:
                if neighbour in distances and \
                        distances.get(neighbour, 0) < current_cost + neighbours_cost:
                    continue
                else:
                    new_cost = current_cost + neighbours_cost
                    distances[neighbour] = new_cost
                    states_with_same_cost = queue.get(new_cost, [])
                    states_with_same_cost.append(neighbour)
                    queue[new_cost] = states_with_same_cost
                    predecessors[neighbour] = current_state
        current_cost += 1


def steps_list(predecessors, last):
    return_list = list()
    state = last
    while True:
        return_list.append(state)
        state = predecessors.get(state)
        if state is None:
            break
    return return_list


def main(my_file):
    burrow = get_data_from_file(my_file)
    room_length = (len(burrow) - 7) // 4
    final = "......." + "".join([letter * room_length for letter in 'ABCD'])
    path, cost = dijkstra(burrow, final)
    """path.reverse()
    for step in path:
        display_burrow(step)
        print()"""
    print(cost)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        filename = sys.argv[1]
    elif len(sys.argv) == 3:
        filename = ""
    else:
        filename = "23_input.txt"
    main(filename)
