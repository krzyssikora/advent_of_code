import sys


def get_triads(my_file):
    triads = list()
    with open(my_file) as f:
        lines = f.readlines()
        for line in lines:
            triad = list(map(int, line.strip().split()))
            triads.append(triad)
    return triads


def get_triads_2(my_file):
    triads = list()
    with open(my_file) as f:
        while True:
            three_triangles = list()
            for _ in range(3):
                line = f.readline().strip().split()
                three_triangles += list(map(int, line))
            if len(three_triangles) == 0:
                break
            for i in range(3):
                triads.append([three_triangles[i], three_triangles[i + 3], three_triangles[i + 6]])
    return triads


def how_many_triangles(triads):
    many = 0
    for triad in triads:
        if sum(triad) > 2 * max(triad):
            many += 1
    return many


def main(my_file):
    triads = get_triads(my_file)
    print(how_many_triangles(triads))
    triads = get_triads_2(my_file)
    print(how_many_triangles(triads))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "03_input.txt"
    main(filename)
