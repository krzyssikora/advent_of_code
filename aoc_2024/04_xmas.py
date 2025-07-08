from pathlib import Path
from collections import defaultdict


def get_data_lines(my_file: Path) -> list:
    with open(my_file) as f:
        lines = f.readlines()
    return [line.strip('\n').strip() for line in lines]


def collect_x_info(lines: list[str]) -> dict:
    steps = [(i, j) for i in [-1, 0, 1] for j in [-1, 0, 1]]
    steps = [step for step in steps if step != (0, 0)]
    x_info = defaultdict(list)
    for row, line in enumerate(lines):
        for column, char in enumerate(line):
            if char != "X":
                continue
            for step in steps:
                if row < 3 and step[1] == -1:
                    continue
                if row >= len(lines) - 3 and step[1] == 1:
                    continue
                if column < 3 and step[0] == -1:
                    continue
                if column >= len(line) - 3 and step[0] == 1:
                    continue
                x_info[(column, row)].append(step)
    return x_info


def collect_a_coords(lines: list[str]) -> list:
    a_coords = []
    for row, line in enumerate(lines):
        for column, char in enumerate(line):
            if char == "A" and 1 <= row < len(lines) - 1 and 1 <= column < len(line) - 1:
                a_coords.append((column, row))
    return a_coords


def xmases_number(lines: list[str], x_cors: tuple[int, int], steps: list[tuple[int, int]]) -> int:
    xmases = 0
    column, row = x_cors
    for x_step, y_step in steps:
        chance = True
        for many, letter in enumerate("MAS", 1):
            char = lines[row + y_step * many][column + x_step * many]
            if char != letter:
                chance = False
                break
        if chance:
            xmases += 1
    return xmases


def xed_mases_number(lines: list[str], a_col: int, a_row: int) -> int:
    step, perpendicular = ((1, 1), (-1, 1))
    xmases = 0
    x_step, y_step = step
    x_perp, y_perp = perpendicular
    first = lines[a_row + y_step][a_col + x_step]
    second = lines[a_row - y_step][a_col - x_step]
    if (first == "M" and second == "S") or (first == "S" and second == "M"):
        third = lines[a_row + y_perp][a_col + x_perp]
        fourth = lines[a_row - y_perp][a_col - x_perp]
        if (third == "M" and fourth == "S") or (third == "S" and fourth == "M"):
            xmases += 1
    return xmases


def main(my_file: Path, inp: int) -> None:
    lines = get_data_lines(my_file)
    x_info = collect_x_info(lines)
    a_coords = collect_a_coords(lines)
    xmases = [xmases_number(lines, x_coors, steps) for x_coors, steps in x_info.items()]
    xed_mases = [xed_mases_number(lines, a_col, a_row) for a_col, a_row in a_coords]

    print(f"input {inp}:", sum(xmases), sum(xed_mases))


if __name__ == "__main__":
    root = Path(__file__).parent
    prefix = Path(__file__).name.split("_")[0]
    for inpt, filename in enumerate([f"{prefix}_inp.txt", f"{prefix}_input.txt"], 1):
    # for inpt, filename in enumerate([f"{prefix}_inp.txt"], 1):
        if (root / filename).exists():
            main(root / filename, inpt)

