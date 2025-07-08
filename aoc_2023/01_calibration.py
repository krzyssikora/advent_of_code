import sys
import os
import re

digits = {
    'zero': 0,
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
} | {
    str(i): i for i in range(10)
}


def get_data(my_file: str) -> list:
    with open(my_file) as f:
        data = f.read()
    data = data.split('\n')
    data = [st.strip() for st in data if st.strip()]
    return data


def get_calibration_value_1(st: str) -> int:
    digs = re.findall(r'\d', st)
    return int(digs[0] + digs[-1])


def get_calibration_value_2(st: str) -> int:
    positions_1 = {st.find(k): k for k in digits}
    positions_2 = {st.rfind(k): k for k in digits}
    positions_1 = {k: v for k, v in positions_1.items() if k >= 0}
    pos_1 = min(positions_1)
    pos_2 = max(positions_2)
    digit_1 = digits[positions_1[pos_1]]
    digit_2 = digits[positions_2[pos_2]]
    return 10 * digit_1 + digit_2


def get_calibration_values_sum(data: list, part: int) -> int:
    if part == 1:
        return sum(get_calibration_value_1(st) for st in data)
    elif part == 2:
        return sum(get_calibration_value_2(st) for st in data)


def main(my_file: str) -> None:
    data = get_data(my_file)
    for part in [1, 2]:
        print(f'part {part}: {get_calibration_values_sum(data, part)}')


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = f'{os.path.basename(__file__)[:2]}_input.txt'
    main(filename)
