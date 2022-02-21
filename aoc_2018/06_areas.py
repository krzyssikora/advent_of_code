import sys


def get_coordinates(my_file):
    with open(my_file) as f:
        lines = f.readlines()
    coordinates = list()
    for line in lines:
        coordinates.append(tuple(map(int, line.strip().split(", "))))
    return coordinates


def manhattan_distance(point_1, point_2):
    x1, y1 = point_1
    x2, y2 = point_2
    return abs(x1 - x2) + abs(y1 - y2)


def infinite_areas(coordinates, extremes, closest):
    x_min, x_max, y_min, y_max = extremes
    infinite = set()
    for point in coordinates:
        idx = coordinates.index(point)
        x, y = point
        if closest[x_min, y] == idx or closest[x, y_min] == idx or \
                closest[x_max, y] == idx or closest[x, y_max] == idx:
            infinite.add(idx)
    return infinite


def get_distances(coordinates, extremes):
    # returns a dictionary
    # key = tuple coordinates of a point
    # value = index of closest point or -1 if either more thn 1 closest point or area is infinite
    closest_points = dict()
    x_min, x_max, y_min, y_max = extremes
    for x in range(x_min, x_max + 1):
        for y in range(y_min, y_max + 1):
            min_dist = min([manhattan_distance((x, y), (xx, yy)) for (xx, yy) in coordinates])
            closest_point = -1
            for n, (xx, yy) in enumerate(coordinates):
                dist = manhattan_distance((x, y), (xx, yy))
                if dist == min_dist:
                    if closest_point == -1:
                        closest_point = n
                    else:
                        closest_point = -1
                        break
            closest_points[x, y] = closest_point
    # reject infinite areas
    infinite = infinite_areas(coordinates, extremes, closest_points)
    points_to_consider = list(closest_points.values())
    points_to_consider = filter(lambda pp: pp != -1, points_to_consider)
    for point in infinite:
        points_to_consider = filter(lambda pp: pp != point, points_to_consider)
    freqs = dict()
    for point in list(points_to_consider):
        if point not in infinite:
            freqs[point] = freqs.get(point, 0) + 1
    return max(freqs.values())


def get_extremes(coordinates):
    x_min, x_max, y_min, y_max = 2000, -2000, 2000, -2000
    for point in coordinates:
        x, y = point
        if x < x_min:
            x_min = x
        elif x > x_max:
            x_max = x
        if y < y_min:
            y_min = y
        elif y > y_max:
            y_max = y
    return x_min, x_max, y_min, y_max


def safe_region(coordinates, extremes, size=10000):
    x_min, x_max, y_min, y_max = extremes
    counter = 0
    for x in range(x_min, x_max + 1):
        for y in range(y_min, y_max + 1):
            if sum([manhattan_distance(point, (x, y)) for point in coordinates]) < size:
                counter += 1
    return counter


def main(my_file):
    coordinates = get_coordinates(my_file)
    extremes = get_extremes(coordinates)
    print("part 1:", get_distances(coordinates, extremes))
    print("part 2:", safe_region(coordinates, extremes))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "06_input.txt"
    main(filename)
