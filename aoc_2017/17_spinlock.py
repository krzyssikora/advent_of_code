def insertion(state, steps, value):
    new_position = steps % len(state)
    state = state[new_position:] + state[:new_position] + [value]
    return state


def value_following_zero(steps, value, current_position):
    ret_value = None
    new_position = (current_position + steps) % value + 1
    if new_position == 1:
        ret_value = value
    return ret_value, new_position


def main():
    steps = 370
    state = [0]
    for value in range(1, 2018):
        state = insertion(state, steps, value)
    print("part 1:", state[0])
    current_position = 0
    my_value = None
    for value in range(1, 50000001):
        ret_value, current_position = value_following_zero(steps, value, current_position)
        if ret_value:
            my_value = ret_value
    print("part 2:", my_value)


if __name__ == "__main__":
    main()
