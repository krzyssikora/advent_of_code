import datetime


def elves_to_remove(elves):
    elves_left = len(elves)
    initial = 0
    removed = set()
    num_removed = 0
    opposite = (initial + elves_left // 2) % elves_left
    while True:
        if opposite >= elves_left or initial >= elves_left or elves_left <= 1:
            break
        elf_removed = elves[opposite + num_removed]
        num_removed += 1
        removed.add(elf_removed)
        elves_left -= 1
        if opposite > initial:
            initial = initial + 1
        opposite = initial + elves_left // 2
    initial = initial % elves_left
    if elves[initial] in removed:
        initial += 1
    return removed, initial


def removing_opposite(elves_number):
    elves = [_ for _ in range(elves_number)]
    while len(elves) > 1:
        to_remove, initial = elves_to_remove(elves)
        initial = elves[initial]
        elves = sorted(list(set(elves).difference(to_remove)))
        initial = elves.index(initial)
        elves = elves[initial:] + elves[:initial]
    return elves.pop() + 1


def cut_list(elves_number):
    elves = [_ for _ in range(elves_number)]
    initial = 0
    while len(elves) > 1:
        leftover = len(elves) % 2
        elves = elves[initial::2]
        initial = (initial + leftover) % 2
    return elves.pop() + 1


def main(elves_number):
    t0 = datetime.datetime.now()
    print("part 1:", cut_list(elves_number))
    t1 = datetime.datetime.now()
    print(t1 - t0)
    t0 = datetime.datetime.now()
    print("part 2:", removing_opposite(elves_number))
    t1 = datetime.datetime.now()
    print(t1 - t0)


if __name__ == "__main__":
    main(3005290)
