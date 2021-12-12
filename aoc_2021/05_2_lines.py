input_data = "input.txt"

# load lines into a list with elts:
# [(x1,y1), (x2, y2)]
lines = list()
max_x = 0
max_y = 0
with open(input_data) as f:
    rows = f.readlines()
    for row in rows:
        row_points = row.split("->")
        point0 = row_points[0].strip("\n").strip().split(",")
        point1 = row_points[1].strip("\n").strip().split(",")
        x1, y1 = int(point0[0]), int(point0[1])
        x2, y2 = int(point1[0]), int(point1[1])
        lines.append([(x1, y1), (x2, y2)])
        if x1 > max_x:
            max_x = x1
        if x2 > max_x:
            max_x = x2
        if y1 > max_y:
            max_y = y1
        if y2 > max_y:
            max_y = y2

# make empty map of vents
vents = [[0 for _ in range(max_x + 1)] for _ in range(max_y + 1)]
maximum_x, maximum_y = max_x, max_y

# add lines data to the map of vents
for line in lines:
    x1, y1 = line[0]
    x2, y2 = line[1]
    if x1 == x2:
        # vertical lines
        max_y, min_y = max(y1, y2), min(y1, y2)
        for y in range(min_y, max_y + 1):
            vents[y][x1] += 1
    elif y1 == y2:
        # horizontal lines
        max_x, min_x = max(x1, x2), min(x1, x2)
        for x in range(min_x, max_x + 1):
            vents[y1][x] += 1
    else:
        # diagonal lines
        dx, dy = x2 - x1, y2 - y1
        step = dx // dy
        max_x, min_x = max(x1, x2), min(x1, x2)
        if min_x == x1:
            y = y1
        else:
            y = y2
        for x in range(min_x, max_x + 1):
            vents[y][x] += 1
            y += step

# find the number of points with more than 1 vent, replace 0 with "."
count = 0
for x in range(maximum_x + 1):
    for y in range(maximum_y + 1):
        if vents[y][x] > 1:
            count += 1
        elif vents[y][x] == 0:
            vents[y][x] = "."
"""
for line in vents:
    for elt in line:
        print(elt, end="")
    print()
print()
"""
print(count)
