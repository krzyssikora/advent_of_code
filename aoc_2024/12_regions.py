import numpy as np
from collections import defaultdict
from pathlib import Path


def get_data_lines(my_file: Path) -> list:
    with open(my_file) as f:
        lines = f.readlines()
    return [line.strip('\n').strip() for line in lines]


def get_region(node, grid, visited=None):
    def get_neighbours(curr):
        current_row, current_col = curr
        return [(r, c) for (r, c) in [
            (current_row - 1, current_col),
            (current_row + 1, current_col),
            (current_row, current_col - 1),
            (current_row, current_col + 1)
        ] if 0 <= r < rows and 0 <= c < cols and grid[r][c] == plant and (r, c) not in visited]

    region = set()
    rows, cols = grid.shape
    visited = visited or set()
    row, col = node
    plant = grid[row][col]
    current = node
    while True:
        region.add(current)
        visited.add(current)
        neighbours = get_neighbours(current)
        if not neighbours:
            break
        for neighbour in neighbours:
            n_region, n_visited = get_region(neighbour, grid, visited)
            region |= n_region
            visited |= n_visited
    return region, visited


def get_regions(grid):
    regions = []
    visited = set()
    rows, cols = grid.shape
    for row in range(rows):
        for col in range(cols):
            if (row, col) in visited:
                continue
            region, _ = get_region((row, col), grid)
            visited |= region
            regions.append(region)
    return regions


def perimeter(region):
    def get_neighbours(curr):
        current_row, current_col = curr
        return [(r, c) for (r, c) in [
            (current_row - 1, current_col),
            (current_row + 1, current_col),
            (current_row, current_col - 1),
            (current_row, current_col + 1)
        ] if (r, c) not in region]

    return sum(len(get_neighbours(node)) for node in region)


def price_1(region):
    return len(region) * perimeter(region)


def sides(region):
    def vertical(direction):
        dd = defaultdict(set)
        for row, col in region:
            if (row + direction, col) not in region:
                dd[row].add(col)
        sds = 0
        for row in dd:
            for n in dd[row]:
                if n + 1 not in dd[row]:
                    sds += 1
        return sds

    def horizontal(direction):
        dd = defaultdict(set)
        for row, col in region:
            if (row, col + direction) not in region:
                dd[col].add(row)
        sds = 0
        for col in dd:
            for n in dd[col]:
                if n + 1 not in dd[col]:
                    sds += 1
        return sds

    return vertical(-1) + vertical(1) + horizontal(-1) + horizontal(1)


def price_2(region):
    return len(region) * sides(region)


def main(my_file: Path, inp: int) -> None:
    lines = get_data_lines(my_file)
    grid = np.array([list(line) for line in lines])
    regions = get_regions(grid)

    print(f"input {inp}:", sum(price_1(region) for region in regions), sum(price_2(region) for region in regions))


if __name__ == "__main__":
    root = Path(__file__).parent
    prefix = Path(__file__).name.split("_")[0]
    for inpt, filename in enumerate([f"{prefix}_inp.txt", f"{prefix}_input.txt"], 1):
        if (root / filename).exists():
            main(root / filename, inpt)
