from pathlib import Path


DIRECTIONS = [
    (0, -1), (1, 0), (0, 1), (-1, 0),
]


def get_data_lines(my_file: Path) -> list:
    with open(my_file) as f:
        lines = f.readlines()
    return [line.strip('\n').strip() for line in lines]


def find_guard_and_dims(lines: list[str]) -> tuple[int, int, int, int]:
    dim_y = len(lines)
    dim_x = len(lines[0])
    for row, line in enumerate(lines):
        for column, char in enumerate(line):
            if char == "^":
                return column, row, dim_x, dim_y


def get_visited(lines) -> tuple[set[tuple[int, int]], set[tuple[int, int]]]:
    def check_loop(x_obstruction, y_obstruction, x_guard, y_guard, d) -> bool:
        loop_visited = set()
        loop_visited.add((x_guard, y_guard, d))
        x_move, y_move = DIRECTIONS[d]
        while True:
            yy = y_guard + y_move
            xx = x_guard + x_move
            if xx in {-1, dim_x} or yy in {-1, dim_y}:
                break
            if lines[yy][xx] == "#" or (xx, yy) == (x_obstruction, y_obstruction):
                d = (d + 1) % 4
                x_move, y_move = DIRECTIONS[d]
                loop_visited.add((x_guard, y_guard, d))
                continue
            if (xx, yy, d) in loop_visited:
                return True
            x_guard, y_guard = xx, yy
            loop_visited.add((x_guard, y_guard, d))
        return False
    guard_x, guard_y, dim_x, dim_y = find_guard_and_dims(lines)
    x, y = guard_x, guard_y
    direction = 0
    visited = set()
    lvisited = []
    obstructions = set()
    while True:
        dx, dy = DIRECTIONS[direction]
        if x + dx in {-1, dim_x} or y + dy in {-1, dim_y}:
            visited.add((x, y))
            lvisited.append((x, y))
            break
        if lines[y + dy][x + dx] == "#":
            direction = (direction + 1) % 4
            continue
        visited.add((x, y))
        lvisited.append((x, y))
        if (x + dx, y + dy) not in visited and check_loop(x + dx, y + dy, x, y, direction):
            obstructions.add((x + dx, y + dy))
        x += dx
        y += dy

    return visited, obstructions


def main(my_file: Path, inp: int) -> None:
    lines = get_data_lines(my_file)
    visited, obstructions = get_visited(lines)
    print(f"input {inp}:", len(visited), len(obstructions))


if __name__ == "__main__":
    root = Path(__file__).parent
    prefix = Path(__file__).name.split("_")[0]
    for inpt, filename in enumerate([f"{prefix}_inp.txt", f"{prefix}_input.txt"], 1):
        if (root / filename).exists():
            main(root / filename, inpt)
