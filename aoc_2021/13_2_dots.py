import sys


def get_list_from_data(my_file):
    points = list()
    folds = list()
    with open(my_file) as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip("\n")
            if line.startswith("fold"):
                folds.append([line[11], int(line[13:])])
            elif line != "":
                coordinates = line.split(",")
                points.append([int(float(coordinates[0])), int(float(coordinates[1]))])
    return points, folds


def make_horizontal_fold(points, y):
    return_points = list()
    for point in points:
        if point[1] < y:
            return_points.append(point)
        else:
            new_point = [point[0], 2 * y - point[1]]
            if new_point not in points:
                return_points.append(new_point)
    return return_points


def make_vertical_fold(points, x):
    return_points = list()
    for point in points:
        if point[0] < x:
            return_points.append(point)
        else:
            new_point = [2 * x - point[0], point[1]]
            if new_point not in points:
                return_points.append(new_point)
    return return_points


def draw_code(points):
    x_s, y_s = zip(*points)
    columns = max(x_s) + 1
    rows = max(y_s) + 1
    for row in range(rows):
        for column in range(columns):
            if [column, row] in points:
                print("#", end=" ")
            else:
                print(".", end=" ")
        print()


def main(my_file):
    points, folds = get_list_from_data(my_file)
    for fold in folds:
        if fold[0] == "x":
            points = make_vertical_fold(points, fold[1])
        elif fold[0] == "y":
            points = make_horizontal_fold(points, fold[1])
        else:
            points = []
    draw_code(points)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "13_input.txt"
    main(filename)
