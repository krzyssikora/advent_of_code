def make_step(recipes, elves):
    recipes += list(map(int, list(str(recipes[elves[0]] + recipes[elves[1]]))))
    for i in range(2):
        elves[i] = (elves[i] + 1 + recipes[elves[i]]) % len(recipes)
    return recipes, elves


def part_1(length=793061):
    recipes = [3, 7]
    elves = [0, 1]
    while True:
        if len(recipes) >= length + 10:
            break
        recipes, elves = make_step(recipes, elves)
    return "".join(map(str, recipes[length: length + 10]))


def part_2(inp_string="793061"):
    recipes = [3, 7]
    elves = [0, 1]
    start = 0
    while True:
        new_string = "".join(map(str, recipes[start:]))
        position = new_string.find(inp_string)
        if position >= 0:
            position += start
            break
        else:
            start = max(len(recipes) - len(inp_string) - 1, 0)
        recipes, elves = make_step(recipes, elves)
    return position


def main():
    print("part 1:", part_1())
    print("part 2:", part_2())


if __name__ == "__main__":
    main()
