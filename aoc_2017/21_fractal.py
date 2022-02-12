import sys
import math


def get_patterns(my_file):
    # returns a dictionary k:v
    # k - tuple (size / area of a square, number of hashes in the pattern)
    # v - a dictionary key: value
    #   key   - one of flipped / rotated patterns
    #   value - new image
    patterns = dict()
    with open(my_file) as f:
        lines = f.readlines()
        for line in lines:
            before, after = line.strip().split(" => ")
            size = len(before) - before.count("/")
            hashes = before.count("#")
            after = after.replace("/", "")
            for arrangement in arrangements(before):
                if (size, hashes) not in patterns:
                    patterns[(size, hashes)] = dict()
                patterns[(size, hashes)][arrangement] = after
    return patterns


def arrangements(pattern):
    lines = pattern.split("/")
    pattern = pattern.replace("/", "")
    patterns = {pattern}
    # vertical flip |
    patterns.add("".join([line[::-1] for line in lines]))
    # horizontal flip -
    patterns.add("".join(lines[::-1]))
    # rotation 90
    patterns.add("".join("".join([line[i] for line in lines]) for i in range(len(lines) - 1, -1, -1)))
    # rotation 180
    patterns.add("".join([line[::-1] for line in lines[::-1]]))
    # rotation 270
    patterns.add("".join("".join([line[i] for line in lines[::-1]]) for i in range(len(lines))))
    # diagonal flip /
    patterns.add("".join("".join([line[i] for line in lines[::-1]]) for i in range(len(lines) - 1, -1, -1)))
    # diagonal flip \
    patterns.add("".join("".join([line[i] for line in lines]) for i in range(len(lines))))
    return patterns


def display_pattern(pattern):
    dim = int(math.sqrt(len(pattern)))
    for row in range(dim):
        print(pattern[row * dim: (row + 1) * dim])
    print()


def cut_into_pieces(fractal, length, dim):
    pieces = list()
    for row in range(dim):
        for column in range(dim):
            piece = ""
            for r in range(length):
                for c in range(length):
                    piece += fractal[(length * row + r) * dim * length + (length * column + c)]
            pieces.append(piece)
    return pieces


def collect_pieces(pieces, length, dim):
    fractal = ""
    for row_batch in range(dim):
        for row in range(length):
            # row_number = (row_batch * length + row)
            for piece in range(dim):
                fractal += pieces[row_batch * dim + piece][row * length: (row + 1) * length]
    return fractal


def enhance(fractal, patterns):
    length = len(fractal)
    # length of side of each piece
    if length % 2 == 0:
        length = 2
    else:
        length = 3
    dim = int(math.sqrt(len(fractal))) // length
    # number of pieces along a side
    size = length ** 2
    small_fractals = cut_into_pieces(fractal, length, dim)
    small_new_fractals = list()
    for small_fractal in small_fractals:
        hashes = small_fractal.count("#")
        small_new_fractals.append(patterns.get((size, hashes)).get(small_fractal))
    length += 1
    return collect_pieces(small_new_fractals, length, dim)


def main(my_file):
    patterns = get_patterns(my_file)
    fractal = ".#...####"
    for i in range(5):
        fractal = enhance(fractal, patterns)
    print("part 1:", fractal.count("#"))
    for i in range(18 - 5):
        fractal = enhance(fractal, patterns)
    print("part 2:", fractal.count("#"))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "21_input.txt"
    main(filename)
