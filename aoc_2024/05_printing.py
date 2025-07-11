from pathlib import Path
from collections import defaultdict


def get_data_lines(my_file: Path) -> list:
    with open(my_file) as f:
        lines = f.readlines()
    return [line.strip('\n').strip() for line in lines]


def ordering_and_updates(lines: list[str]) -> tuple[dict, list[list[int]]]:
    ordering = defaultdict(list)
    updates = []
    for line in lines:
        if "|" in line:
            key, value = line.split("|")
            ordering[int(key)].append(int(value))
        elif line:
            updates.append(list(map(int, line.split(","))))
    return ordering, updates


def get_items_before_and_after(pivot: int, values: list[int], ordering: dict) -> tuple[list, list]:
    preceding, following = [], []
    after_pivot = ordering.get(pivot) or []
    for value in values:
        if value in after_pivot:
            following.append(value)
        else:
            preceding.append(value)
    return preceding, following


def get_sorted_update(update: list[int], ordering: dict) -> list[int]:
    if not update:
        return []
    pivot = update[0]
    preceding, following = get_items_before_and_after(pivot, update[1:], ordering)
    return get_sorted_update(preceding, ordering) + [pivot] + get_sorted_update(following, ordering)


def is_correct_update(ordering:dict, update: list[int]):
    for idx in range(len(update) - 1):
        first = update[idx]
        following = update[idx + 1]
        if following not in (ordering.get(first) or []):
            return False
    return True


def get_sums_of_middle_elements_from_updates(
        ordering: dict,
        updates: list[list[int]],
    ) -> tuple[int, int]:
    correct_middle_added = 0
    incorrect_middle_added = 0
    for update in updates:
        if is_correct_update(ordering, update):
            correct_middle_added += update[(len(update) - 1) // 2]
        else:
            incorrect_middle_added += get_sorted_update(update, ordering)[(len(update) - 1) // 2]
    return correct_middle_added, incorrect_middle_added


def main(my_file: Path, inp: int) -> None:
    lines = get_data_lines(my_file)
    ordering, updates = ordering_and_updates(lines)
    correct, incorrect = get_sums_of_middle_elements_from_updates(ordering, updates)

    print(f"input {inp}:", correct, incorrect)


if __name__ == "__main__":
    root = Path(__file__).parent
    prefix = Path(__file__).name.split("_")[0]
    for inp, filename in enumerate([f"{prefix}_inp.txt", f"{prefix}_input.txt"], 1):
        if (root / filename).exists():
            main(root / filename, inp)

