from pathlib import Path
import re


def get_data_lines(my_file: Path) -> list:
    with open(my_file) as f:
        lines = f.readlines()
    return [line.strip('\n').strip() for line in lines]


def sum_of_products(line: str) -> int:
    pattern = r"mul\((\d+),(\d+)\)"
    products_added = 0
    for m in re.findall(pattern, line):
        n1, n2 = list(map(int, m))
        products_added += n1 * n2
    return products_added


def conditional_sum_of_products(line: str) -> int:
    def get_conditional_idx(strt: int) -> tuple[int, int]:
        posp = line.find("do()", start + 1)
        posn = line.find("don't()", start + 1)
        if posp == -1:
            posp = len(line)
        if posn == -1:
            posn = len(line)
        if posp < posn:
            return posp, 1
        elif posp > posn:
            return posn, 0
        else:
            return posn, -1

    start = 0
    end, nxt_factor = get_conditional_idx(start)
    cur_factor = 1
    products_added = 0
    while True:
        if cur_factor == -1:
            break
        if cur_factor == 1:
            products_added += sum_of_products(line[start: end])
        start = end
        cur_factor = nxt_factor
        end, nxt_factor = get_conditional_idx(start)
    return products_added


def main(my_file: Path, inp: int) -> None:
    lines = get_data_lines(my_file)
    products_added = sum_of_products("".join(lines))
    conditional_products_added = conditional_sum_of_products("".join(lines))

    print(f"input {inp}:", products_added, conditional_products_added)


if __name__ == "__main__":
    root = Path(__file__).parent
    prefix = Path(__file__).name.split("_")[0]
    for inp, filename in enumerate([f"{prefix}_inp.txt", f"{prefix}_inp2.txt", f"{prefix}_input.txt"], 1):
        if (root / filename).exists():
            main(root / filename, inp)

