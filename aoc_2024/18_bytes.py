from collections import deque
from pathlib import Path


def get_data_lines(my_file: Path) -> list:
    with open(my_file) as f:
        lines = f.readlines()
    return [line.strip('\n').strip() for line in lines]


def get_coordinates(lines):
    corrupted_bytes = []
    for line in lines:
        corrupted_bytes.append(tuple(map(int, line.split(","))))
    return corrupted_bytes


def shortest_path(corrupted_bytes, dim):
    start = (0, 0)
    end = (dim, dim)
    visited = set()
    queue = deque()
    queue.append((start[0], start[1], 0))  # row, col, cost
    visited.add((start[0], start[1]))

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # W, E, N, S

    while queue:
        x, y, cost = queue.popleft()

        if (x, y) == end:
            return cost

        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if (
                    0 <= new_x <= dim and
                    0 <= new_y <= dim and
                    (new_x, new_y) not in corrupted_bytes
                    and (new_x, new_y) not in visited
            ):
                visited.add((new_x, new_y))
                queue.append((new_x, new_y, cost + 1))

    return -1  # No path found


def blocking_byte(corrupted_bytes, dim):
    min_idx = 0
    max_idx = len(corrupted_bytes)
    while True:
        mid_idx = (min_idx + max_idx) // 2
        path_length = shortest_path(corrupted_bytes[:mid_idx + 1], dim)
        if path_length > 0:
            if mid_idx + 1 == max_idx:
                return corrupted_bytes[max_idx]
            min_idx = mid_idx
        else:
            max_idx = mid_idx


def main(my_file: Path, inp: int) -> None:
    lines = get_data_lines(my_file)
    corrupted_bytes = get_coordinates(lines)
    dim, corrupted = {
        1: (6, 12),
        2: (70, 1024)
    }.get(inp)
    path_length = shortest_path(corrupted_bytes[:corrupted], dim)
    coordinates = blocking_byte(corrupted_bytes, dim)

    print(f"input {inp}:", path_length, coordinates)


if __name__ == "__main__":
    root = Path(__file__).parent
    prefix = Path(__file__).name.split("_")[0]
    for inpt, filename in enumerate([f"{prefix}_inp.txt", f"{prefix}_input.txt"], 1):
        if (root / filename).exists():
            main(root / filename, inpt)
