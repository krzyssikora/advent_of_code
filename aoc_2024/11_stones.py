from collections import defaultdict
from pathlib import Path


def get_data_lines(my_file: Path) -> list:
    with open(my_file) as f:
        lines = f.readlines()
    return [line.strip('\n').strip() for line in lines]


def get_numbers(lines):
    numbers = list(map(int, lines[0].split(" ")))
    dd = defaultdict(int)
    for number in numbers:
        dd[number] += 1
    return dd


def blink_number(number: int) -> list[int]:
    if number == 0:
        return [1]
    string = str(number)
    length = len(string)
    if length % 2 == 0:
        str1 = string[:length // 2]
        str2 = string[length // 2:]
        return [int(str1), int(str2)]
    return [number * 2024]


def blink_numbers(input_numbers: dict) -> dict:
    output_numbers = defaultdict(int)
    for number, freq in input_numbers.items():
        numbers = blink_number(number)
        for n in numbers:
            output_numbers[n] += freq
    return output_numbers


def blink_numbers_n_times(numbers: dict, times: int) -> dict:
    for _ in range(times):
        numbers = blink_numbers(numbers)
    return numbers


def main(my_file: Path, inp: int) -> None:
    lines = get_data_lines(my_file)
    numbers = get_numbers(lines)
    numbers_1 = blink_numbers_n_times(numbers.copy(), 25)
    numbers_2 = blink_numbers_n_times(numbers.copy(), 75)

    print(f"input {inp}:", sum(numbers_1.values()), sum(numbers_2.values()))


if __name__ == "__main__":
    root = Path(__file__).parent
    prefix = Path(__file__).name.split("_")[0]
    for inpt, filename in enumerate([f"{prefix}_inp.txt", f"{prefix}_input.txt"], 1):
        if (root / filename).exists():
            main(root / filename, inpt)
