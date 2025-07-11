from pathlib import Path
from collections import defaultdict


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
    return antennas


def main(my_file: Path, inp: int) -> None:
    lines = get_data_lines(my_file)
    antennas = get_antennas(lines)


    print(f"input {inp}:", )


if __name__ == "__main__":
    root = Path(__file__).parent
    prefix = Path(__file__).name.split("_")[0]
    for inpt, filename in enumerate([f"{prefix}_inp.txt", f"{prefix}_input.txt"], 1):
        if (root / filename).exists():
            main(root / filename, inpt)
