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


def main():
    my_file = "09_input.txt"
    height_map = change_data_into_list(my_file)
    total_risk_level = 0
    for row in range(len(height_map)):
        for column in range(len(height_map[0])):
            total_risk_level += risk_level(height_map, row, column)
    print(total_risk_level)


if __name__ == "__main__":
    main()
