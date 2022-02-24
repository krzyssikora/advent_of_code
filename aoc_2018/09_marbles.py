from collections import defaultdict, deque


def make_move(circle, scores, move_number, players):
    player = move_number % players + 1
    if move_number % 23 == 0:
        circle.rotate(7)
        scores[player] += move_number + circle.pop()
        circle.rotate(-1)
    else:
        circle.rotate(-1)
        circle.append(move_number)
    return circle, scores


def play_game(players, marbles):
    circle = deque([0])
    scores = defaultdict(int)
    for m in range(1, marbles + 1):
        circle, scores = make_move(circle, scores, m, players)
    return max(scores.values())


def main():
    players, marbles = 426, 72058
    print("part 1:", play_game(players, marbles))
    marbles *= 100
    print("part 2:", play_game(players, marbles))


if __name__ == "__main__":
    main()
