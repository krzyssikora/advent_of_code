from pathlib import Path


def get_data_lines(my_file: Path) -> list:
    with open(my_file) as f:
        lines = f.readlines()
    return [line.strip('\n').strip() for line in lines]


def is_safe(line: list[int]) -> bool:
    diff = line[1] - line[0]
    if diff > 0:
        increasing = True
    elif diff < 0:
        increasing = False
    else:
        return False
    for idx in range(len(line) - 1):
        left, right = line[idx], line[idx + 1]
        if (increasing and 1 <= right - left <= 3) or (not increasing and -3 <= right - left <= -1):
            continue
        return False
    return True


def is_almost_safe(line: list[int]) -> bool:
    for idx in range(len(line)):
        new_line = line[:idx] + line[idx + 1:]
        if is_safe(new_line):
            return True
    return False


def main(my_file: Path, inp: int) -> None:
    lines = get_data_lines(my_file)
    lines = [list(map(int, line.split())) for line in lines]
    safe_no = sum([1 if is_safe(line) else 0 for line in lines])
    almost_safe_no = sum([1 if is_almost_safe(line) else 0 for line in lines])

    print(f"input {inp}:", safe_no, almost_safe_no)


if __name__ == "__main__":
    root = Path(__file__).parent
    prefix = Path(__file__).name.split("_")[0]
    for inp, filename in enumerate([f"{prefix}_inp.txt", f"{prefix}_input.txt"], 1):
        if (root / filename).exists():
            main(root / filename, inp)

