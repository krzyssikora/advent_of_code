from pathlib import Path
from dataclasses import dataclass


@dataclass
class Slot:
    id: int or None
    size: int
    empty: int
    first: int
    last: int  # actually, 1 after last

    def __str__(self):
        slot_type = "file" if self.id else "empty"
        size = f", size: {self.size + self.empty}"
        optional_id = f" (id: {self.id})" if self.id else ""
        return (
            slot_type +
            f": from {self.first} to {self.last}" +
            size +
            optional_id
        )


def get_data_lines(my_file: Path) -> list:
    with open(my_file) as f:
        lines = f.readlines()
    return [line.strip('\n').strip() for line in lines]


def get_disk_map(line):
    disk_map = []
    for idx, char in enumerate(line):
        if idx % 2 == 0:
            # files
            for _ in range(int(char)):
                disk_map.append(idx // 2)
        else:
            # empty
            for _ in range(int(char)):
                disk_map.append("")
    return disk_map


def get_disk_map_2(line):
    disk_map = []
    initial = 0
    for idx, char in enumerate(line):
        val = int(char)
        if idx % 2 == 0:
            # files
            slot_id = idx // 2
            size = val
            empty = 0
        else:
            # empty
            slot_id = None
            size = 0
            empty = val
        first = initial
        last = first + val
        initial = last
        disk_map.append(Slot(slot_id, size, empty, first, last))
    return disk_map


def fragmented_disk(disk_map: list[Slot]):
    for right_idx in range(len(disk_map) - 1, 0, -2):
        for left_idx in range(1, right_idx, 2):
            empty_slot = disk_map[left_idx]
            file_slot = disk_map[right_idx]
            if file_slot.size <= empty_slot.empty:
                file_slot.first = empty_slot.first
                file_slot.last = file_slot.first + file_slot.size
                empty_slot.first = file_slot.last
                empty_slot.empty -= file_slot.size
                break
    return disk_map


def cleaned_disk(disk_map):
    clean_disk = disk_map.copy()
    left = 0
    right = len(disk_map) - 1
    while True:
        while clean_disk[left] != "":
            left += 1
        while clean_disk[right] == "":
            right -= 1
        if left >= right:
            break
        clean_disk[left] = clean_disk[right]
        clean_disk[right] = ""
        left += 1
        right -= 1
    return clean_disk


def disk_map_as_list_of_vals(d_map):
    disk_map = d_map.copy()
    max_last = max(slot.last for slot in disk_map)
    lst = ["."] * max_last
    for slot in disk_map:
        if slot.id is not None:
            for idx in range(slot.first, slot.last):
                lst[idx] = slot.id
    return lst


def get_checksum(disk_map):
    checksum = 0
    for idx, char in enumerate(disk_map):
        if char not in {"", "."}:
            checksum += idx * int(char)
    return checksum


def main(my_file: Path, inp: int) -> None:
    lines = get_data_lines(my_file)
    line = lines[0]
    disk_map = get_disk_map(line)
    clean_disk = cleaned_disk(disk_map)
    checksum = get_checksum(clean_disk)
    # part 2
    disk_map = get_disk_map_2(line)
    fragmented = fragmented_disk(disk_map)
    fr_str = disk_map_as_list_of_vals(fragmented)
    checksum_2 = get_checksum(fr_str)
    print(f"input {inp}:", checksum, checksum_2)


if __name__ == "__main__":
    root = Path(__file__).parent
    prefix = Path(__file__).name.split("_")[0]
    for inpt, filename in enumerate([f"{prefix}_inp.txt", f"{prefix}_input.txt"], 1):
        if (root / filename).exists():
            main(root / filename, inpt)
