with open("input.txt") as f:
    first = second = third = 0
    count_to_three = 0
    count = 0
    lines = f.readlines()
    for line in lines:
        next = int(line)
        count_to_three += 1
        if count_to_three > 3:
            if next > first:
                count += 1
        first, second, third = second, third, next
    print(count)
