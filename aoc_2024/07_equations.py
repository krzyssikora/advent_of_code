from pathlib import Path


def get_data_lines(my_file: Path) -> list:
    with open(my_file) as f:
        lines = f.readlines()
    return [line.strip('\n').strip() for line in lines]


def get_data(lines: list[str]) -> dict:
    data = {}
    for line in lines:
        result, inputs = line.split(": ")
        data[int(result)] = list(map(int, inputs.split()))
    return data


def concat(inp1: int, inp2: int) -> int:
    return int(str(inp1) + str(inp2))


def can_be_obtained(result, inputs) -> bool:
    if len(inputs) == 1:
        return result == inputs[0]
    last = inputs[-1]
    if result // last == result / last:
        can_be_obtained_from_product = can_be_obtained(result // last, inputs[:-1])
        if can_be_obtained_from_product:
            return True
    return can_be_obtained(result - last, inputs[:-1])


def can_be_done(result, inputs) -> bool:
    if len(inputs) == 1:
        return result == inputs[0]
    last = inputs[-1]
    if result // last == result / last:
        can_be_done_with_product = can_be_done(result // last, inputs[:-1])
        if can_be_done_with_product:
            return True
    last_len = len(str(last))
    if str(result)[-last_len:] == str(last):
        shortened_result_str = str(result)[:-len(str(last))]
        if shortened_result_str:
            shortened_result = int(shortened_result_str)
            can_be_done_with_concat = can_be_done(shortened_result, inputs[:-1])
            if can_be_done_with_concat:
                return True
    return can_be_done(result - last, inputs[:-1])


def main(my_file: Path, inp: int) -> None:
    lines = get_data_lines(my_file)
    data = get_data(lines)
    calibration_result = 0
    calibration_improvement = 0
    for result, inputs in data.items():
        if can_be_obtained(result, inputs):
            calibration_result += result
        elif can_be_done(result, inputs):
            calibration_improvement += result

    print(f"input {inp}:", calibration_result, calibration_result + calibration_improvement)


if __name__ == "__main__":
    root = Path(__file__).parent
    prefix = Path(__file__).name.split("_")[0]
    for inpt, filename in enumerate([f"{prefix}_inp.txt", f"{prefix}_input.txt"], 1):
        if (root / filename).exists():
            main(root / filename, inpt)
