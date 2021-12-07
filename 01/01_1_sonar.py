with open("input.txt") as f:
    previous = None
    count = 0
    lines = f.readlines()
    for line in lines:
        next = int(line)
        if previous is None:
            previous = next
            continue
        if next > previous:
            count += 1
        previous = next
    print(count)
