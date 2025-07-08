import sys
import os


def get_data(my_file: str) -> list:
    with open(my_file) as f:
        data = f.read()
    data = data.split('\n')
    data = [st.strip() for st in data if st.strip()]
    return data


def get_index_if_game_possible(game: str, no_red: int, no_green: int, no_blue: int) -> int:
    game_id_str, game_data = game.split(': ')
    game_id = int(game_id_str[5:])
    samples = game_data.split('; ')
    check = {'red': no_red,
             'green': no_green,
             'blue': no_blue}

    for sample in samples:
        colour_values = sample.split(', ')
        for colour_value in colour_values:
            number_str, colour = colour_value.split()
            if int(number_str) > check[colour]:
                return 0
    return game_id


def get_game_power(game: str) -> int:
    game_id_str, game_data = game.split(': ')
    samples = game_data.split('; ')
    minima = {clr: 0 for clr in {'red', 'green', 'blue'}}

    for sample in samples:
        colour_values = sample.split(', ')
        for colour_value in colour_values:
            number_str, colour = colour_value.split()
            minima[colour] = max(int(number_str), minima.get(colour))

    return minima['red'] * minima['green'] * minima['blue']


def get_sum_of_impossible_games_indicies(data: list, no_red: int, no_green: int, no_blue: int) -> int:
    return sum(get_index_if_game_possible(game, no_red, no_green, no_blue) for game in data)


def get_sum_of_game_powers(data: list) -> int:
    return sum(get_game_power(game) for game in data)


def get_part_result(data: list, part: int) -> int:
    if part == 1:
        return get_sum_of_impossible_games_indicies(data, 12, 13, 14)
    elif part == 2:
        return get_sum_of_game_powers(data)


def main(my_file: str) -> None:
    data = get_data(my_file)
    for part in [1, 2]:
        print(f'part {part}: {get_part_result(data, part)}')


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = f'{os.path.basename(__file__)[:2]}_input.txt'
    main(filename)
