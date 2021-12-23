def get_options():
    options = dict()
    for i in range(1, 4):
        for j in range(1, 4):
            for k in range(1, 4):
                options[i + j + k] = options.get(i + j + k, 0) + 1
    return options


def main():
    states = dict()  # (pos0, score0, pos1, score1, turn)
    states[(4, 0, 1, 0, 0)] = 1
    players_wins = dict()
    options = get_options()
    while True:
        current_states = dict()
        for state, frequency in states.items():
            pos0, score0, pos1, score1, turn = state
            for result, many in options.items():
                if turn == 0:
                    new_pos0 = (pos0 - 1 + result) % 10 + 1
                    new_score0 = score0 + new_pos0
                    if new_score0 >= 21:
                        players_wins[0] = players_wins.get(0, 0) + frequency * many
                    else:
                        new_state = (new_pos0, new_score0, pos1, score1, 1 - turn)
                        current_states[new_state] = current_states.get(new_state, 0) + frequency * many
                elif turn == 1:
                    new_pos1 = (pos1 - 1 + result) % 10 + 1
                    new_score1 = score1 + new_pos1
                    if new_score1 >= 21:
                        players_wins[1] = players_wins.get(1, 0) + frequency * many
                    else:
                        new_state = (pos0, score0, new_pos1, new_score1, 1 - turn)
                        current_states[new_state] = current_states.get(new_state, 0) + frequency * many
        if len(current_states) == 0:
            break
        states.clear()
        states.update(current_states)
    print("Player 1:", players_wins.get(0, 0))
    print("Player 2:", players_wins.get(1, 0))


if __name__ == "__main__":
    main()
