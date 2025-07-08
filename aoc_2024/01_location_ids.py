from pathlib import Path
from collections import Counter


def get_data_lines(my_file: Path) -> list:
    with open(my_file) as f:
        lines = f.readlines()
    return [line.strip('\n').strip() for line in lines]


def get_difference(left: list[int], right: list[int]) -> int:
    diff = 0
    for ll, rr in zip(left, right):
        diff += abs(ll - rr)
    return diff


def get_similarity(left: list[int], right: list[int]) -> int:
    sim = 0
    ldict = Counter(left)
    rdict = Counter(right)
    for key, value in ldict.items():
        sim += key * value * rdict.get(key, 0)
    return sim


def main(my_file: Path, inp: int) -> None:
    lines = get_data_lines(my_file)
    left, right = [], []
    for line in lines:
        ll, rr = list(map(int, line.split("   ")))
        left.append(ll)
        right.append(rr)
    left.sort()
    right.sort()
    diff = get_difference(left, right)
    sim = get_similarity(left, right)

    print(f"input {inp}:", diff, sim)


if __name__ == "__main__":
    root = Path(__file__).parent
    prefix = Path(__file__).name.split("_")[0]
    for part, filename in enumerate([f"{prefix}_inp.txt", f"{prefix}_input.txt"], 1):
        if (root / filename).exists():
            main(root / filename, part)
