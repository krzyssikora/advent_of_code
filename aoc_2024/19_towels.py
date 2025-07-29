import sys
from pathlib import Path
sys.setrecursionlimit(10**6)


def get_data_lines(my_file: Path) -> list:
    with open(my_file) as f:
        lines = f.readlines()
    return [line.strip('\n').strip() for line in lines]


def get_patterns_and_designes(lines):
    patterns = lines[0].split(", ")
    designs = lines[2:]
    return patterns, designs


def possible_designs(patterns, designs):
    designs_number = 0
    possible_ways = 0
    cache = {}
    for idx, design in enumerate(designs, 1):
        if number := number_of_ways(patterns, design, cache):
            designs_number += 1
            possible_ways += number
    return designs_number, possible_ways


def number_of_ways(patterns, design, cache=None):
    if cache is None:
        cache = {}
    if design in cache:
        return cache[design]
    number = 0
    if design == "":
        number = 1
    for pattern in patterns:
        if design.startswith(pattern):
            number += number_of_ways(patterns, design[len(pattern):], cache)
    cache[design] = number
    return number


def main(my_file: Path, inp: int) -> None:
    lines = get_data_lines(my_file)
    patterns, designs = get_patterns_and_designes(lines)
    patterns.sort(key=len, reverse=True)
    designs_number, possible_ways = possible_designs(patterns, designs)
    print(f"input {inp}:", designs_number, possible_ways)


if __name__ == "__main__":
    root = Path(__file__).parent
    prefix = Path(__file__).name.split("_")[0]
    for inpt, filename in enumerate([f"{prefix}_inp.txt", f"{prefix}_input.txt"], 1):
        if (root / filename).exists():
            main(root / filename, inpt)
