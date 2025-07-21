from pathlib import Path
import numpy as np


def get_data_lines(my_file: Path) -> list:
    with open(my_file) as f:
        lines = f.readlines()
    return [line.strip('\n').strip() for line in lines]


def get_map(lines: list) -> np.array:
    heights = []
    for line in lines:
        heights.append(list(map(int, list(line))))
    return np.array(heights)


def get_trail_map_positions(trail_map: np.array, value: int) -> list:
    trail_heads = []
    rows, cols = trail_map.shape
    for row in range(rows):
        for column in range(cols):
            if trail_map[row][column] == value:
                trail_heads.append((row, column))
    return trail_heads


def get_trail_head_score(trailhead, trail_map) -> list:
    def get_neighbours(node):
        row, column = node
        return [(r, c) for (r, c) in [
            (row - 1, column),
            (row + 1, column),
            (row, column - 1),
            (row, column + 1),
        ] if 0 <= r < rows and 0 <= c < cols and trail_map[r][c] == trail_map[row][column] + 1]

    rows, cols = trail_map.shape
    current = trailhead
    ends = []

    current_row, current_col = current
    if trail_map[current_row][current_col] == 9:
        return [(current_row, current_col)]
    neighbours = get_neighbours(current)
    if not neighbours:
        return []
    for neighbour in neighbours:
        if path_ends := get_trail_head_score(neighbour, trail_map):
            ends += path_ends

    return ends


def get_trail_heads_scores(trailheads, trail_map) -> dict:
    scores = {}
    for trailhead in trailheads:
        trailhead_score = get_trail_head_score(trailhead, trail_map)
        scores[trailhead] = (len(set(trailhead_score)), len(trailhead_score))
    return scores


def main(my_file: Path, inp: int) -> None:
    lines = get_data_lines(my_file)
    trail_map = get_map(lines)
    trailheads = get_trail_map_positions(trail_map, 0)
    scores = get_trail_heads_scores(trailheads, trail_map)

    print(f"input {inp}:", sum(v[0] for v in scores.values()), sum(v[1] for v in scores.values()))


if __name__ == "__main__":
    root = Path(__file__).parent
    prefix = Path(__file__).name.split("_")[0]
    for inpt, filename in enumerate([f"{prefix}_inp.txt", f"{prefix}_input.txt"], 1):
        if (root / filename).exists():
            main(root / filename, inpt)
