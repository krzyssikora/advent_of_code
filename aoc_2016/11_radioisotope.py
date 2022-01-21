import itertools
import sys


def get_data_string(input_data):
    items_number = 0
    items = list()
    for val in input_data.values():
        items_number += len(val)
        items += val
    items.sort()
    items_number += 1  # place for an elevator
    items_number *= 2  # two chars for an item
    expected = "." * items_number * 3 + "EL" + "".join(items)
    current = ""
    for floor_number in range(1, 5):
        floor_items = input_data.get(floor_number)
        floor = "." * items_number
        for item in floor_items:
            position = items.index(item) * 2 + 2
            floor = floor[: position] + item + floor[position + 2:]
        current += floor
    current = "EL" + current[2:]
    return current, expected


def get_dict_from_string(state):
    state_dict = dict()
    line_length = len(state) // 4
    for i in range(4):
        state_dict[i + 1] = get_items_from_floor(state[i * line_length: (i + 1) * line_length])
    return state_dict


def display_state(state):
    line_length = len(state) // 4
    for i in range(3, -1, -1):
        floor = ""
        tmp_floor = state[i * line_length: (i + 1) * line_length]
        for j in range(line_length // 2):
            floor += tmp_floor[:2] + " "
            tmp_floor = tmp_floor[2:]
        print(str(i + 1) + ": " + floor)
    print()


def replace_floor_in_state(state, floor, floor_number):
    line_length = len(state) // 4
    new_state = state[: floor_number * line_length] + floor + state[(floor_number + 1) * line_length:]
    return new_state


def get_items_from_floor(floor):
    items = list()
    for i in range(len(floor) // 2):
        item = floor[2 * i: 2 * (i + 1)]
        if item not in {"..", "EL"}:
            items.append(item)
    return items


def move_item_from_floor_to_floor(state, item, floor_from_number, floor_to_number):
    line_length = len(state) // 4
    floor_from = state[floor_from_number * line_length: (floor_from_number + 1) * line_length]
    floor_to = state[floor_to_number * line_length: (floor_to_number + 1) * line_length]
    item_pos = floor_from.find(item)
    floor_from = floor_from[:item_pos] + ".." + floor_from[item_pos + 2:]
    floor_to = floor_to[:item_pos] + item + floor_to[item_pos + 2:]
    # move elevator
    floor_from = ".." + floor_from[2:]
    floor_to = "EL" + floor_to[2:]
    state = state[:floor_from_number * line_length] + floor_from + state[(floor_from_number + 1) * line_length:]
    state = state[:floor_to_number * line_length] + floor_to + state[(floor_to_number + 1) * line_length:]
    return state


def safe_row(row):
    m_set = set()
    g_set = set()
    for item in row:
        if item[1] == "M":
            m_set.add(item[0])
        elif item[1] == "G":
            g_set.add(item[0])
    if len(g_set) == 0:
        return True
    for m_item in m_set:
        if m_item not in g_set:
            return False
    return True


def neighbours(state):
    line_length = len(state) // 4
    current_floor_number = state.index("EL") // line_length  # actually, floor - 1
    current_floor = state[current_floor_number * line_length: (current_floor_number + 1) * line_length]
    current_floor_items = get_items_from_floor(current_floor)
    new_floor_numbers = {0, 1, 2, 3}.intersection({current_floor_number - 1,
                                                   current_floor_number,
                                                   current_floor_number + 1}).difference({current_floor_number})
    neighbours_list = list()
    for new_floor_number in new_floor_numbers:
        new_floor = state[new_floor_number * line_length: (new_floor_number + 1) * line_length]
        new_floor_items = get_items_from_floor(new_floor)
        # firstly, two items' moves
        items_to_move = list()
        pairs_of_items = itertools.combinations(current_floor_items, 2)
        for item_1, item_2 in pairs_of_items:
            if item_1[1] != item_2[1] and item_1[0] != item_2[0]:
                continue  # as they cannot go into the elevator together
            new_row_items = set(new_floor_items).union({item_1, item_2})
            old_row_items = set(current_floor_items).difference({item_1, item_2})
            if safe_row(new_row_items) and safe_row(old_row_items):
                items_to_move.append((item_1, item_2))
        # secondly, single item's moves
        single_items_to_move = list()
        for item in current_floor_items:
            new_row_items = set(new_floor_items).union({item})
            old_row_items = set(current_floor_items).difference({item})
            if safe_row(new_row_items) and safe_row(old_row_items):
                single_items_to_move.append(item)
        # if 2 items can be moved upstairs, there is no sense to move one
        for item in single_items_to_move:
            if current_floor_number < new_floor_number:
                if any([item in pair for pair in items_to_move]):
                    continue
            if current_floor_number > new_floor_number:
                if any([item in pair for pair in items_to_move]):
                    pairs_to_remove = list()
                    for pair in items_to_move:
                        if item in pair:
                            pairs_to_remove.append(pair)
                    for pair in pairs_to_remove:
                        items_to_move.remove(pair)
        # Given on a certain floor: AG, AM, BG, BM,
        # if both AM and BM are to move up, it is enough to check AM.
        if current_floor_number < new_floor_number:
            # Let us firstly find pairs >> XG, XM << on the floor
            tools = ["G", "M"]
            microchips_to_consider = set()
            for item in current_floor_items:
                if item[0] + tools[1 - tools.index(item[1])] in current_floor_items \
                        and item[0] + "M" in single_items_to_move:
                    microchips_to_consider.add(item[0])
            microchips_to_consider = sorted(list(microchips_to_consider))
            # remove redundant microchips from single_items_to_move
            for microchip in microchips_to_consider[1:]:
                single_items_to_move.remove(microchip + "M")
        # add to neighbours the states from moving pairs of items
        for item_1, item_2 in items_to_move:
            state_1 = move_item_from_floor_to_floor(state, item_1, current_floor_number, new_floor_number)
            state_2 = move_item_from_floor_to_floor(state_1, item_2, current_floor_number, new_floor_number)
            neighbours_list.append(state_2)
        # add to neighbours the states from moving pairs of items
        for item in single_items_to_move:
            neighbours_list.append(
                move_item_from_floor_to_floor(state, item, current_floor_number, new_floor_number))
    return neighbours_list


def path_between(previous, state_1, state_2):
    final_path = list()
    current_state = state_1
    while current_state != state_2:
        final_path = [current_state] + final_path
        current_state = previous[current_state]
    final_path = [current_state] + final_path
    return final_path


def equivalent_states(state, types_list):
    elevator = state.find("EL")
    for i, char in enumerate(types_list):
        state = state.replace(char + "M", str(i) + "M")
        state = state.replace(char + "G", str(i) + "G")
    state_dict = get_dict_from_string(state)
    equivalent = set()
    for permutation in itertools.permutations(types_list):
        tmp_dict = dict()
        for floor_number, items in state_dict.items():
            tmp_dict[floor_number] = list()
            for item in items:
                tmp_dict[floor_number].append(permutation[int(item[0])] + item[1])
        new_state = get_data_string(tmp_dict)[0]
        new_state = ".." + new_state[2:]
        new_state = new_state[:elevator] + "EL" + new_state[elevator + 2:]
        equivalent.add(new_state)
    return equivalent


def types(state):
    line_length = len(state) // 4
    types_set = set()
    for i in range(4):
        floor = state[i * line_length: (i + 1) * line_length]
        items = get_items_from_floor(floor)
        for item in items:
            types_set.add(item[0])
    types_list = sorted(list(types_set))
    return types_list


def dijkstra(initial_state, final_state):
    types_list = types(initial_state)
    previous = {initial_state: None}
    costs = dict()
    for state in equivalent_states(initial_state, types_list):
        costs[state] = 0
    queue = [initial_state]
    tmp_count = 0
    while True:
        if abs(len(queue) - tmp_count) > 10:
            tmp_count = len(queue)
            print(len(costs), tmp_count)
        if len(queue):
            current_state = queue.pop()
        else:
            break
        current_neighbours = neighbours(current_state)
        for neighbour in current_neighbours:
            if neighbour not in costs or costs[neighbour] > costs[current_state] + 1:
                new_cost = costs[current_state] + 1
                for state in equivalent_states(neighbour, types_list):
                    costs[state] = new_cost
                queue.append(neighbour)
                previous[neighbour] = current_state
#        if current_state == final_state:
#            break
    final_path = path_between(previous, final_state, initial_state)
    return costs[final_state], final_path


def main():
    data_num = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    input_data_0 = {
        1: ["HM", "LM"],
        2: ["HG"],
        3: ["LG"],
        4: []}
    input_data_1 = {
        1: ["SG", "SM", "PG", "PM"],
        2: ["TG", "RG", "RM", "CG", "CM"],
        3: ["TM"],
        4: []}
    input_data_2 = {
        1: ["SG", "SM", "PG", "PM", "DG", "DM", "EG", "EM"],
        2: ["TG", "RG", "RM", "CG", "CM"],
        3: ["TM"],
        4: []}
    input_data_3 = {
        1: ["AM", "BM", "BG"],
        2: ["CM", "CG"],
        3: ["AG"],
        4: []
    }
    inputs = [input_data_0, input_data_1, input_data_2, input_data_3]
    input_data = inputs[data_num]
    current_state, expected_state = get_data_string(input_data)
    """for state in equivalent_states(current_state, types(current_state)):
        display_state(state)
    quit()"""
    """for neighbour in neighbours(current_state):
        display_state(neighbour)
    quit()"""
    result, final_path = dijkstra(current_state, expected_state)
    print(result)
    for elt in final_path:
        display_state(elt)


if __name__ == "__main__":
    main()
