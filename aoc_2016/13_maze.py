import math


def draw_grid(rows, columns, favourite=1358):
    # unnecessary, just for checking
    for y in range(rows):
        for x in range(columns):
            value = x ** 2 + 3 * x + 2 * x * y + y + y ** 2 + favourite
            if is_open(value):
                print(".", end="")
            else:
                print("#", end="")
        print()


def draw_grid_with_reach(rows, columns, reach, favourite=1358):
    # unnecessary, just for checking
    for y in range(rows):
        for x in range(columns):
            if (x, y) in reach:
                print("O", end=" ")
            else:
                value = x ** 2 + 3 * x + 2 * x * y + y + y ** 2 + favourite
                if is_open(value):
                    print(".", end=" ")
                else:
                    print("#", end=" ")
        print()


def is_open(int_value):
    max_power = math.ceil(math.log(int_value + 1, 2))
    count = 0
    for n in range(max_power):
        if 2 ** n & int_value != 0:
            count += 1
    return count % 2 == 0


def neighbours(x, y, value):
    global visited
    neighbour_list = list()
    tmp_value = value - 2 * x - 2 * y - 2
    if x > 0 and (x - 1, y) not in visited and is_open(tmp_value):
        neighbour_list.append(((x - 1, y), tmp_value))
    tmp_value += 2
    if y > 0 and (x, y - 1) not in visited and is_open(tmp_value):
        neighbour_list.append(((x, y - 1), tmp_value))
    tmp_value = value + 2 * x + 2 * y + 2
    if (x, y + 1) not in visited and is_open(tmp_value):
        neighbour_list.append(((x, y + 1), tmp_value))
    tmp_value += 2
    if (x + 1, y) not in visited and is_open(tmp_value):
        neighbour_list.append(((x + 1, y), tmp_value))
    return neighbour_list


def find_shortest(initial, final, part, favourite=1358):
    global visited
    x, y = initial
    value = x ** 2 + 3 * x + 2 * x * y + y + y ** 2 + favourite
    costs = {initial: 0}
    queue = [(initial, value, 0)]
    while True:
        if len(queue) == 0:
            break
        current, value, cost = queue.pop()
        x, y = current
        current_neighbours = neighbours(x, y, value)
        for neighbour, n_value in current_neighbours:
            if neighbour not in costs or costs[neighbour] > costs[current] + 1:
                costs[neighbour] = costs[current] + 1
                queue.append((neighbour, n_value, costs[neighbour]))
        queue.sort(key=lambda elt: elt[2], reverse=True)
    if part == 1:
        return costs[final]
    elif part == 2:
        reach = set()
        for place, distance in costs.items():
            if distance <= 50:
                reach.add(place)
        return len(reach)
    else:
        return None


def main():
    global visited
    favourite = 1358
    initial = (1, 1)
    final = (31, 39)
    print("part 1:", find_shortest(initial, final, 1, favourite))
    visited = set()
    print("part 2:", find_shortest(initial, final, 2, favourite))


if __name__ == "__main__":
    visited = set()
    main()
