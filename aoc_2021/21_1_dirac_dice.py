def main():
    starting_positions = [4, 1]
    number_of_rolls = 0
    die_outcomes = [i + 1 for i in range(10)]
    scores = [0, 0]
    while True:
        player = number_of_rolls % 2
        number_of_rolls += 3
        results = [die_outcomes.pop(0) for _ in range(3)]
        die_outcomes += results
        result = sum(results)
        starting_positions[player] = (starting_positions[player] - 1 + result) % 10 +1
        scores[player] += starting_positions[player]
        if scores[player] >= 1000:
            break
    print("number_of_rolls :", number_of_rolls)
    print("losing score    :", scores[number_of_rolls % 2])
    print(number_of_rolls * scores[number_of_rolls % 2])

if __name__ == "__main__":
    main()
