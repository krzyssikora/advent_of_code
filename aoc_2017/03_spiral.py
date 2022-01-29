import math


def manhattan(number):
    if number == 1:
        return 0
    base = math.floor(math.sqrt(number - 1))
    if base % 2 == 0:
        base -= 1
    remainder = (number - base ** 2) % (base + 1)
    if remainder > (base + 1) // 2:
        return remainder
    else:
        return base - remainder + 1


def coordinates(number):
    if number == 1:
        return 0, 0
    base = math.floor(math.sqrt(number))
    if base % 2 == 0:
        base -= 1
    # base is the base of the largest full square around 1 such that the number is not in it
    remainder = (number - base ** 2) % (base + 1)
    turns = (number - base ** 2) // (base + 1)
    if turns == 0 and remainder == 0:
        return (base - 1) // 2, -(base - 1) // 2
    elif turns == 0:
        return (base + 1) // 2, -(base + 1) // 2 + remainder
    elif turns == 1:
        return (base + 1) // 2 - remainder, (base + 1) // 2
    elif turns == 2:
        return -(base + 1) // 2, (base + 1) // 2 - remainder
    elif turns == 3:
        return -(base + 1) // 2 + remainder, -(base + 1) // 2


def exceeding_number(number):
    values = {(0, 0): 1}
    idx = 2
    while True:
        x, y = coordinates(idx)
        value = 0
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if dx == dy == 0:
                    continue
                value += values.get((x + dx, y + dy), 0)
        values[(x, y)] = value
        if value >= number:
            return value
        idx += 1


def main():
    print("part 1:", manhattan(325489))
    print("part 2:", exceeding_number(325489))


if __name__ == "__main__":
    main()
