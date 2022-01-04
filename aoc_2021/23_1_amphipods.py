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


def neighbours(state):
    def get_cost(hallway, room_no, room_pos):
        return abs(hallway - room_no) * 2 \
               + 4 * (room_no >= hallway) \
               - 2 * (hallway - room_no >= 2) \
               - 1 * (hallway in {0, 6}) \
               + room_pos

    costs = {"A": 1, "B": 10, "C": 100, "D": 1000}
    homerooms = {"A": 0, "B": 1, "C": 2, "D": 3}
    room_length = (len(state) - 7) // 4
    neighbour_list = list()
    # find positions of free spots in the hallway
    free_hallway_places = list()
    for i in range(7):
        if state[i] == ".":
            free_hallway_places.append(i)
    # find positions of first amphipods in each room that are ready to leave
    amphipods_on_room_tops = list()
    # amphipods_on_room_tops[0] = 2 means that 0^th room is ..XX
    for room in range(4):
        i = 0
        while i < room_length and state[7 + room_length * room + i] == ".":
            i += 1
        amphipods_on_room_tops.append(i)
    # find possible spots for each amphipod from rooms
    amphipods_spots = [list() for _ in range(4)]
    for i in range(4):
        position = i + 1
        if position not in free_hallway_places:
            position += 1
        # go left
        tmp_pos = position
        while tmp_pos in free_hallway_places:
            amphipods_spots[i].append(tmp_pos)
            tmp_pos -= 1
        # go right
        tmp_pos = position
        while tmp_pos in free_hallway_places:
            if tmp_pos not in amphipods_spots[i]:
                amphipods_spots[i].append(tmp_pos)
            tmp_pos += 1
        amphipods_spots[i].sort()
    # create neighbours as tuples (neighbour - string, cost of getting to the neighbour)
    # amphipods in hallway moving to their homerooms
    amphipods_in_hallway = [i for i in range(7) if state[i] != "."]
    for amphipod_pos in amphipods_in_hallway:
        amphipod = state[amphipod_pos]
        homeroom = homerooms[amphipod]
        homeroom_position = amphipods_on_room_tops[homeroom] - 1
        # if there is an amphipod in the hallway between the amphipod and its homeroom, then continue
        range_to_check = range(amphipod_pos + 1, homeroom + 2) if amphipod_pos < homeroom + 2 \
            else range(homeroom + 2, amphipod_pos)
        if any([state[i] != "." for i in range_to_check]):
            continue
        if homeroom_position >= 0:
            # check if the room is empty or all amphipds in the room are of the same kind
            if state[room_length - 1] == "." \
                            or all([state[i] == amphipod for i in range(homeroom_position + 1, 4)]):
                swap_cost = get_cost(amphipod_pos, homeroom, homeroom_position) * costs[amphipod]
                neighbour_list.append((single_move(state, amphipod_pos,
                                                   7 + room_length * homeroom + homeroom_position),
                                       swap_cost))
    # amphipods leaving homerooms for the hallway
    for room, amphipod_pos in enumerate(amphipods_on_room_tops):
        if amphipod_pos == room_length:
            continue
        amphipod_in_state = 7 + room_length * room + amphipod_pos
        amphipod = state[amphipod_in_state]
        for empty_pos in amphipods_spots[room]:
            swap_cost = get_cost(empty_pos, room, amphipod_pos) * costs[amphipod]
            neighbour_list.append((single_move(state, amphipod_in_state, empty_pos), swap_cost))
    return neighbour_list


def dijkstra(start, end):
    predecessors = {start: None}
    distances = dict()
    current_state = start
    distances[start] = 0
    to_visit = list()
    visited = set()
    # current_neighbours = list()
    while True:
        # print(current_state, len(current_neighbours), len(to_visit), len(visited))
        visited.add(current_state)
        if current_state in to_visit:
            to_visit.remove(current_state)
        if current_state == end:
            break
        current_neighbours = neighbours(current_state)
        current_neighbours.sort(key=lambda x: x[1])
        for neighbour in current_neighbours:
            if neighbour[0] not in visited and neighbour[0] not in to_visit:
                to_visit.append(neighbour[0])
            if neighbour[0] not in distances:
                distances[neighbour[0]] = distances[current_state] + neighbour[1]
                predecessors[neighbour[0]] = current_state
            elif distances[neighbour[0]] > distances[current_state] + neighbour[1]:
                distances[neighbour[0]] = distances[current_state] + neighbour[1]
                predecessors[neighbour[0]] = current_state
        if len(to_visit) == 0:
            break
        current_state = to_visit.pop(0)
    return distances, predecessors


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
    distance, predecessors = dijkstra(burrow, final)
    path = steps_list(predecessors, final)
    path.reverse()
    for step in path:
        display_burrow(step)
        print()
    print(distance[final])


if __name__ == "__main__":
    if len(sys.argv) == 2:
        filename = sys.argv[1]
    elif len(sys.argv) == 3:
        filename = ""
    else:
        filename = "23_input.txt"
    main(filename)
