import numpy as np
from pathlib import Path


def get_data_lines(my_file: Path) -> list:
    with open(my_file) as f:
        lines = f.readlines()
    return [line.strip('\n').strip() for line in lines]


def get_grid_and_moves(lines, part):
    grid_list = []
    moves_string = ""
    robot = None
    for row, line in enumerate(lines):
        if line.startswith("#"):
            if part == 2:
                line = line.replace("#", "##").replace(".", "..").replace("O", "[]").replace("@", "@.")
            grid_list.append(list(line))
            if "@" in line:
                col = line.index("@")
                robot = (col, row)
        elif line.strip() == "":
            continue
        else:
            moves_string += line
    grid = np.array(grid_list)

    mdict = {
        "<": (-1, 0),
        ">": (1, 0),
        "v": (0, 1),
        "^": (0, -1),
    }
    moves = []
    idx_start = 0
    idx_end = 1
    while True:
        move_char = moves_string[idx_start]
        while idx_end < len(moves_string) and moves_string[idx_end] == move_char:
            idx_end += 1
        moves.append((mdict[move_char], idx_end - idx_start))
        if idx_end >= len(moves_string):
            break
        idx_start = idx_end
        idx_end += 1
    return grid, moves, robot


def make_move(grid, robot, move_data, part):
    if part == 1:
        return make_move_1(grid, robot, move_data)
    elif part == 2:
        return make_move_2(grid, robot, move_data)


def make_move_1(grid, robot, move_data):
    move, steps = move_data
    dx, dy = move
    rx, ry = robot
    next_x, next_y = robot
    empties = 0
    boxes = 0
    while True:
        if empties == steps:
            break
        next_x += dx
        next_y += dy
        nxt = grid[next_y, next_x]
        if nxt == "#":
            break
        if nxt == ".":
            empties += 1
        if nxt == "O":
            boxes += 1

    if empties == 0:
        # no empty spot, no move possible
        return grid, robot

    # and now the path that we checked will be filled with:
    # 1. empty spaces
    # 2. robot in new position
    # 3. moved boxes
    x = rx
    y = ry
    while empties > 0:
        grid[y, x] = "."
        empties -= 1
        x += dx
        y += dy
    grid[y, x] = "@"
    rx = x
    ry = y
    x += dx
    y += dy
    while boxes > 0:
        grid[y, x] = "O"
        boxes -= 1
        x += dx
        y += dy

    return grid, (rx, ry)


def make_move_2(grid, robot, move_data):
    move, steps = move_data
    dx, dy = move
    rx, ry = robot
    next_x, next_y = robot
    empties = 0
    boxes = 0
    if dx:
        while True:
            if empties == steps:
                break
            next_x += dx
            next_y += dy
            nxt = grid[next_y, next_x]
            if nxt == "#":
                break
            if nxt == ".":
                empties += 1
            if nxt == "[":
                boxes += 1

        if empties == 0:
            # no empty spot, no move possible
            return grid, robot

        # and now the path that we checked will be filled with:
        # 1. empty spaces
        # 2. robot in new position
        # 3. moved boxes
        x = rx
        y = ry
        while empties > 0:
            grid[y, x] = "."
            empties -= 1
            x += dx
            y += dy
        grid[y, x] = "@"
        rx = x
        ry = y
        x += dx
        y += dy
        while boxes > 0:
            if dx > 0:
                grid[y, x] = "["
                grid[y, x + 1] = "]"
            else:
                grid[y, x - 1] = "["
                grid[y, x] = "]"
            boxes -= 1
            x += dx * 2
            y += dy
    if dy:
        border = {robot}
        should_be_moved = set()
        while True:
            if steps == 0:
                break
            # first check, if next from border are boxes or empty
            wall_found = False
            new_border = set()
            for elt in border:
                x_elt, y_elt = elt
                x_nxt, y_nxt = x_elt, y_elt + dy
                nxt = grid[y_nxt, x_nxt]
                if nxt == "#":
                    wall_found = True
                    break
                elif nxt == ".":
                    new_border.add(elt)
                elif nxt == "[":
                    new_border.add((x_nxt, y_nxt))
                    new_border.add((x_nxt + 1, y_nxt))
                elif nxt == "]":
                    new_border.add((x_nxt, y_nxt))
                    new_border.add((x_nxt - 1, y_nxt))
            if wall_found:
                break
            # wall not found, so we can continue
            if new_border.issubset(border):
                # move robot and boxes
                steps -= 1
                should_be_moved |= border
                should_be_moved.add(robot)
                should_be_moved = sorted(list(should_be_moved), key=lambda l: l[1], reverse=(dy > 0))
                for elt in should_be_moved:
                    x_elt, y_elt = elt
                    x_nxt, y_nxt = x_elt, y_elt + dy
                    elt_val = grid[y_elt, x_elt]
                    grid[y_elt, x_elt] = "."
                    grid[y_nxt, x_nxt] = elt_val
                # adjust robot's position
                ry += dy
                robot = (rx, ry)
                border = {robot}
                should_be_moved = set()
            else:
                # move border
                should_be_moved |= (border.difference(new_border))
                border = new_border
        # wall found, the end of movement

    return grid, (rx, ry)


def make_moves(grid, moves, robot, part):
    for idx, move_data in enumerate(moves):
        grid, robot = make_move(grid, robot, move_data, part)
    return grid


def get_gps(grid):
    rows, cols = grid.shape
    gps = 0
    for row in range(rows):
        for col in range(cols):
            if grid[row, col] in {"O", "["}:
                gps += 100 * row + col
    return gps


def grid_correct(grid):
    rows, columns = grid.shape
    for row in range(rows):
        for col in range(columns - 1):
            if grid[row, col] == "[" and grid[row, col + 1] != "]":
                return False
            if grid[row, col] != "[" and grid[row, col + 1] == "]":
                return False
    return True


def main(my_file: Path, inp: int) -> None:
    lines = get_data_lines(my_file)
    grid_1, moves, robot = get_grid_and_moves(lines, 1)
    grid_1 = make_moves(grid_1, moves, robot, 1)
    gps_1 = get_gps(grid_1)
    grid_2, moves, robot = get_grid_and_moves(lines, 2)
    grid_2 = make_moves(grid_2, moves, robot, 2)
    gps_2 = get_gps(grid_2)

    print(f"input {inp}:", gps_1, gps_2)


if __name__ == "__main__":
    root = Path(__file__).parent
    prefix = Path(__file__).name.split("_")[0]
    for inpt, filename in enumerate([f"{prefix}_in.txt", f"{prefix}_inp.txt", f"{prefix}_input.txt"], 1):
        if (root / filename).exists():
            main(root / filename, inpt)
