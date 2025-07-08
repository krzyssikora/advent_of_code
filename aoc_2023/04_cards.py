import sys
import os
from collections import defaultdict


def get_data(my_file: str) -> list:
    with open(my_file) as f:
        data = f.read()
    data = data.split('\n')
    data = [st.strip() for st in data if st.strip()]
    return data


def get_cards(data: list) -> list:
    cards = list()
    for line in data:
        card_no, cards_data = line.split(': ')
        win_str, have_str = cards_data.split(' | ')
        win = set(map(int, win_str.split()))
        have = set(map(int, have_str.split()))
        cards.append((win, have))
    return cards


def get_points_from_cards(cards: list) -> int:
    total = 0
    for win, have in cards:
        if n := len(have.intersection(win)):
            total += 2 ** (n-1)
    return total


def get_new_cards_number(cards: list) -> int:
    new_cards = {i: 1 for i in range(1, len(cards) + 1)}
    for idx, cards_info in enumerate(cards):
        card_number = idx + 1
        win, have = cards_info
        if n := len(have.intersection(win)):
            for k in range(card_number + 1, card_number + n + 1):
                new_cards[k] += new_cards.get(card_number, 0)
    return sum(new_cards.values())


def get_part_result(data: list, part: int) -> int:
    cards = get_cards(data)
    if part == 1:
        return get_points_from_cards(cards)
    elif part == 2:
        return get_new_cards_number(cards)


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
