def change_data_into_list(my_file):
    return_list = list()
    with open(my_file) as f:
        lines = f.readlines()
        for line in lines:
            line_list = list()
            line = line.strip("\n")
            for elt in line:
                line_list.append(int(elt))
            return_list.append(line_list)
    return return_list


def risk_level(my_map, row, column):
    # returns map value +1 for low points (lower than any of the adjacent)
    # returns 0 elsewhere
    rows = len(my_map)
    columns = len(my_map[0])
    is_low = True
    if row > 0:
        is_low = is_low and my_map[row - 1][column] > my_map[row][column]
    if row < rows - 1:
        is_low = is_low and my_map[row + 1][column] > my_map[row][column]
    if column > 0:
        is_low = is_low and my_map[row][column - 1] > my_map[row][column]
    if column < columns - 1:
        is_low = is_low and my_map[row][column + 1] > my_map[row][column]
    if is_low:
        return my_map[row][column] + 1
    else:
        return 0


def find_low_points(my_map):
    rows = len(my_map)
    columns = len(my_map[0])
    return_list = list()
    for row in range(rows):
        for column in range(columns):
            if risk_level(my_map, row, column) > 0:
                return_list.append([row, column])
    return return_list


def find_basin(my_map, row, column, my_basin):
    def merge_basins(basin_1, basin_2):
        basin = basin_1.copy()
        for point in basin_2:
            if point in basin:
                continue
            else:
                basin.append(point)
        return basin

    my_basin.append([row, column])
    rows = len(my_map)
    columns = len(my_map[0])
    for shift in {-1, 1}:
        if row + shift in range(0, rows):
            if [row + shift, column] not in my_basin and my_map[row + shift][column] < 9:
                my_basin = merge_basins(my_basin, find_basin(my_map, row + shift, column, my_basin))
        if column + shift in range(0, columns):
            if [row, column + shift] not in my_basin and my_map[row][column + shift] < 9:
                my_basin = merge_basins(my_basin, find_basin(my_map, row, column + shift, my_basin))
    return my_basin


def main():
    my_file = "09_input.txt"
    height_map = change_data_into_list(my_file)
    low_points = find_low_points(height_map)
    basins = list()
    for point in low_points:
        basins.append(len(find_basin(height_map, point[0], point[1], [])))
    basins.sort(reverse=True)
    print(basins[0] * basins[1] * basins[2])


if __name__ == "__main__":
    main()
