def code_value(position):
    value = 20151125
    for _ in range(position - 1):
        value *= 252533
        value %= 33554393
    return value


def main():
    row, column = 2978, 3083
    position = (row + column) * (row + column + 1) // 2 - column - 1 - 2 * (row - 1)
    print(code_value(position))


if __name__ == "__main__":
    main()
