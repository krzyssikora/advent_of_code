import re
from pathlib import Path

import numpy as np


def get_data_lines(my_file: Path) -> list:
    with open(my_file) as f:
        lines = f.readlines()
    return [line.strip('\n').strip() for line in lines]


def get_boxes(lines):
    boxes = []
    for idx in range((len(lines) + 1) // 4):
        pattern = "^Button {letter}: X\+(\d+), Y\+(\d+)$"

        line_1 = lines[4 * idx]
        m = re.match(pattern.format(letter="A"), line_1)
        x_1, y_1 = list(map(int, m.groups()))

        line_2 = lines[4 * idx + 1]
        m = re.match(pattern.format(letter="B"), line_2)
        x_2, y_2 = list(map(int, m.groups()))

        line_3 = lines[4 * idx + 2]
        m = re.match("^Prize: X=(\d+), Y=(\d+)$", line_3)
        v_1, v_2 = list(map(int, m.groups()))

        boxes.append({
            "matrix": np.array([[x_1, x_2], [y_1, y_2]]),
            "vector": np.array([[v_1], [v_2]])
        })
    return boxes


def get_tokens_to_winn_all(boxes):
    tokens_1 = 0
    tokens_2 = 0
    for box in boxes:
        m = box['matrix']
        v_1 = box['vector']
        v_2 = v_1 + np.array([[10000000000000], [10000000000000]])
        n = np.linalg.inv(m)
        res_1 = np.round(np.matmul(n, v_1), 0)
        res_2 = np.round(np.matmul(n, v_2), 0)
        check_1 = np.round(np.matmul(m, res_1), 0)
        if (check_1 == v_1).all():
            tokens_1 += np.matmul(np.array([3, 1]), res_1)[0]
        check_2 = np.round(np.matmul(m, res_2), 0)
        if (check_2 == v_2).all():
            tokens_2 += np.matmul(np.array([3, 1]), res_2)[0]
    return int(tokens_1), int(tokens_2)


def main(my_file: Path, inp: int) -> None:
    lines = get_data_lines(my_file)
    boxes = get_boxes(lines)
    tokens = get_tokens_to_winn_all(boxes)

    print(f"input {inp}:", tokens)


if __name__ == "__main__":
    root = Path(__file__).parent
    prefix = Path(__file__).name.split("_")[0]
    for inpt, filename in enumerate([f"{prefix}_inp.txt", f"{prefix}_input.txt"], 1):
        if (root / filename).exists():
            main(root / filename, inpt)
