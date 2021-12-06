with open("input.txt") as f:
    lines = f.readlines()
    depth = 0
    horizontal_position = 0
    aim = 0
    vectors = {"forward":   (1, 0),
               "up":        (0, -1),
               "down":      (0, 1)}
    for line in lines:
        command = line.split(" ")
        vector = vectors.get(command[0])
        magnitude = int(command[1])
        dx, dy = vector[0] * magnitude, vector[1] * magnitude
        aim += dy
        depth += aim * dx
        horizontal_position += dx
#        if depth < 0:
#            depth = 0
    print(depth * horizontal_position)
