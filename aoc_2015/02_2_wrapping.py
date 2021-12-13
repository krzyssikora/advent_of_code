import sys


def get_dimensions_from_file(my_file):
    with open(my_file) as f:
        lines = f.readlines()
        all_dimensions = list()
        for line in lines:
            dimensions = list()
            dim_string = line.strip("\n").split("x")
            for elt in dim_string:
                dimensions.append(int(elt))
            all_dimensions.append(dimensions)
    return all_dimensions


def box_area(dim_list):
    a1 = dim_list[0] * dim_list[1]
    a2 = dim_list[0] * dim_list[2]
    a3 = dim_list[1] * dim_list[2]
    return 2 * (a1 + a2 + a3) + min(a1, a2, a3)


def box_ribbon_length(dim_list):
    vol = dim_list[0] * dim_list[1] * dim_list[2]
    length = (sum(dim_list)  - max(dim_list)) * 2
    return length + vol


def total_ribbon_length(box_list):
    total_length = 0
    for box in box_list:
        total_length += box_ribbon_length(box)
    return total_length


def total_area_of_boxes(box_list):
    total_area = 0
    for box in box_list:
        total_area += box_area(box)
    return total_area


def main(my_file):
    boxes = get_dimensions_from_file(my_file)
    print(total_ribbon_length(boxes))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "02_input.txt"
    main(filename)
