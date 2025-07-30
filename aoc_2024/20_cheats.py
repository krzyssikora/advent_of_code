import numpy as np
from collections import deque, defaultdict
from pathlib import Path


def get_data_lines(my_file: Path) -> list:
    with open(my_file) as f:
        lines = f.readlines()
    return [line.strip('\n').strip() for line in lines]


def get_data(lines):
    grid_list = []
    start = None
    end = None
    for row, line in enumerate(lines):
        row_list = []
        for col, char in enumerate(line):
            if char == "S":
                start = (row, col)
                row_list.append(".")
            elif char == "E":
                end = (row, col)
                row_list.append(".")
            else:
                row_list.append(char)
        grid_list.append(row_list)

    grid = np.array(grid_list)
    return grid, start, end


def m_dist(first, second):
    return abs(first[0] - second[0]) + abs(first[1] - second[1])


def correct(elt, rows, cols):
    return 0 <= elt[0] < rows and 0 <= elt[1] < cols


def neighbours(r, c, rows, cols):
    return [
        (rr, cc) for (rr, cc) in [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]
        if correct((rr, cc), rows, cols)
    ]


def get_path_data(grid, start, end):
    rows, cols = grid.shape
    current = start
    path_list = []
    path_dict = {}
    while True:
        path_dict[current] = len(path_list)
        path_list.append(current)
        if current == end:
            break
        possible = [
            (nr, nc) for (nr, nc) in neighbours(*current, rows, cols)
            if (nr, nc) not in path_dict and grid[nr, nc] == "."
        ]
        current = possible[0]
    return path_list, path_dict


def get_cheats(grid, path_list, path_dict):
    rows, cols = grid.shape
    cheats = {}
    for idx, elt in enumerate(path_list[:-1]):
        possible = [(nr, nc) for (nr, nc) in neighbours(*elt, rows, cols) if grid[nr, nc] == "#"]
        for wall in possible:
            nxt = (2 * wall[0] - elt[0], 2 * wall[1] - elt[1])
            if (nxt_idx := path_dict.get(nxt, 0)) > idx and nxt_idx - idx - 2 >= 100:
                cheats[wall] = nxt_idx - idx - 2
    return cheats


def get_better_cheats(grid, path_list, path_dict):
    cheats = {}
    for idx, elt in enumerate(path_list[:-1]):
        for target_elt in path_list[idx + 1:]:
            if (steps := m_dist(elt, target_elt)) > 20:
                continue
            target_idx = path_dict.get(target_elt, 0)
            if steps > 0 and target_idx - idx - steps >= 100:
                cheats[(elt, target_elt)] = target_idx - idx - steps
    return cheats


def main(my_file: Path, inp: int) -> None:
    lines = get_data_lines(my_file)
    grid, start, end = get_data(lines)
    path_list, path_dict = get_path_data(grid, start, end)
    cheats_1 = get_cheats(grid, path_list, path_dict)
    cheats_2 = get_better_cheats(grid, path_list, path_dict)
    dd_1 = defaultdict(int)
    dd_2 = defaultdict(int)
    for v in cheats_1.values():
        dd_1[v] += 1
    for v in cheats_2.values():
        dd_2[v] += 1

    print(f"input {inp}:", sum(dd_1.values()), sum(dd_2.values()))


if __name__ == "__main__":
    root = Path(__file__).parent
    prefix = Path(__file__).name.split("_")[0]
    # for inpt, filename in enumerate([f"{prefix}_inp.txt"], 1):
    for inpt, filename in enumerate([f"{prefix}_inp.txt", f"{prefix}_input.txt"], 1):
        if (root / filename).exists():
            main(root / filename, inpt)
