from pathlib import Path
from collections import defaultdict
import math


def get_data_lines(my_file: Path) -> list:
    with open(my_file) as f:
        lines = f.readlines()
    return [line.strip('\n').strip() for line in lines]


def get_antennas(lines):
    antennas = defaultdict(list)
    for row, line in enumerate(lines):
        for column, char in enumerate(line):
            if char.isalnum():
                antennas[char].append((column, row))
    return antennas, (len(lines[0]), len(lines))


def in_the_box(x, y, dim_x, dim_y):
    if 0 <= x < dim_x and 0 <= y < dim_y:
        return True
    return False


def get_antinodes(antennas, dim):
    dim_x, dim_y = dim
    antinodes = set()
    for antenna_name, positions in antennas.items():
        for idx_1 in range(len(positions)):
            for idx_2 in range(idx_1 + 1, len(positions)):
                ant_1 = positions[idx_1]
                ant_2 = positions[idx_2]
                dx = ant_2[0] - ant_1[0]
                dy = ant_2[1] - ant_1[1]
                x_1 = ant_2[0] + dx
                y_1 = ant_2[1] + dy
                x_2 = ant_1[0] - dx
                y_2 = ant_1[1] - dy
                if in_the_box(x_1, y_1, dim_x, dim_y):
                    antinodes.add((x_1, y_1))
                if in_the_box(x_2, y_2, dim_x, dim_y):
                    antinodes.add((x_2, y_2))
    return antinodes


def get_improved_antinodes(antennas, dim):
    dim_x, dim_y = dim
    antinodes = set()
    for antenna_name, positions in antennas.items():
        for idx_1 in range(len(positions)):
            for idx_2 in range(idx_1 + 1, len(positions)):
                ant_1 = positions[idx_1]
                ant_2 = positions[idx_2]
                dx = ant_2[0] - ant_1[0]
                dy = ant_2[1] - ant_1[1]
                divisor = math.gcd(dx, dy)
                if divisor > 1:
                    dx = dx / divisor
                    dy = dy / divisor
                if dx < 0:
                    dx = -dx
                    dy = -dy
                x0 = ant_1[0] - (ant_1[0] // dx + 2) * dx
                y0 = ant_1[1] - (ant_1[0] // dx + 2) * dy

                steps = dim_x // dx + 3
                for step in range(steps):
                    x = x0 + step * dx
                    y = y0 + step * dy
                    if in_the_box(x, y, dim_x, dim_y):
                        antinodes.add((x, y))
    return antinodes


def main(my_file: Path, inp: int) -> None:
    lines = get_data_lines(my_file)
    antennas, dim = get_antennas(lines)
    antinodes = get_antinodes(antennas, dim)
    improved_antinodes = get_improved_antinodes(antennas, dim)

    print(f"input {inp}:", len(antinodes), len(improved_antinodes))


if __name__ == "__main__":
    root = Path(__file__).parent
    prefix = Path(__file__).name.split("_")[0]
    for inpt, filename in enumerate([f"{prefix}_inp.txt", f"{prefix}_input.txt"], 1):
        if (root / filename).exists():
            main(root / filename, inpt)
