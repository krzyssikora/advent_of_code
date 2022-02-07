import itertools


def next_value(generator, value):
    # factor_a, factor_b = 16807, 48271
    factor = {"a": 16807, "b": 48271}.get(generator)
    divisor = 2147483647
    while True:
        value = (value * factor) % divisor
        yield value


def next_value_2(generator, value):
    validator = {"a": 4, "b": 8}.get(generator)
    factor = {"a": 16807, "b": 48271}.get(generator)
    divisor = 2147483647
    while True:
        value = (value * factor) % divisor
        while value % validator:
            value = (value * factor) % divisor
        yield value


def judges_count(part, a=289, b=629):
    if part == 1:
        return sum(map(lambda x: x[0] & 0xFFFF == x[1] & 0xFFFF,
                       itertools.islice(zip(next_value("a", a), next_value("b", b)), 40000000)))
    elif part == 2:
        return sum(map(lambda x: x[0] & 0xFFFF == x[1] & 0xFFFF,
                       itertools.islice(zip(next_value_2("a", a), next_value_2("b", b)), 5000000)))


def main():
    for part in {1, 2}:
        print(f"part {part}:", judges_count(part))


if __name__ == "__main__":
    main()
