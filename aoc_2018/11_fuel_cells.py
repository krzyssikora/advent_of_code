import numpy as np


def power(x, y, serial_number=7989):
    return ((x + 1 + 10) * ((x + 1 + 10) * (y + 1) + serial_number)) % 1000 // 100 - 5


def get_triples(grid):
    triples = np.zeros((298, 298))
    for x in range(298):
        for y in range(298):
            triples[x, y] += np.sum(grid[x: x + 3, y: y + 3])
    return triples


def get_squares(grid):
    """unnecessary anymore"""
    squares = np.zeros((300, 300, 300))
    squares[:300, :300, 1] = grid
    for size in range(2, 301):
        for x in range(300):
            if x + size >= 300:
                break
            for y in range(300):
                if y + size >= 300:
                    break
                squares[x, y, size] = \
                    squares[x, y, size - 1] \
                    + np.sum(grid[x: x + size, y + size - 1]) \
                    + np.sum(grid[x + size - 1, y: y + size - 1])
    return squares


def get_part_2_faster(grid):
    squares = np.zeros((300, 300, 300))
    squares[:300, :300, 1] = grid
    best_max_value = np.max(grid)
    max_size = 1
    for size in range(2, 301):
        for x in range(300):
            if x + size >= 300:
                break
            for y in range(300):
                if y + size >= 300:
                    break
                squares[x, y, size] = \
                    squares[x, y, size - 1] \
                    + np.sum(grid[x: x + size, y + size - 1]) \
                    + np.sum(grid[x + size - 1, y: y + size - 1])
        max_value = np.max(squares[:, :, size])
        if max_value > best_max_value:
            best_max_value = max_value
            max_size = size
        elif max_value < best_max_value:
            break
    pos = np.where(squares == best_max_value)
    return pos[0][0] + 1, pos[1][0] + 1, max_size


def get_max(squares):
    max_value = np.max(squares)
    tmp = np.where(squares == max_value)
    ret = list()
    for i in range(2):
        ret.append(tmp[i][0] + 1)
    if np.ndim(squares) > 2:
        ret.append(tmp[2][0])
    return tuple(ret)


def main():
    grid = np.fromfunction(power, (300, 300))
    print("part 1:", get_max(get_triples(grid)))
    print("part 2:", get_part_2_faster(grid))
    """squares = get_squares(grid)
    print("part 2:", get_max(squares))"""


if __name__ == "__main__":
    main()
