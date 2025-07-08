import sys
import os
import re
from collections import defaultdict


class RegexEqual(str):
    def __eq__(self, pattern):
        return bool(re.search(pattern, self))


class Grid:
    def __init__(self):
        self.numbers: dict = {}
        self.symbols: set = set()
        self.gears: set = set()

        self.value: None or int = None
        self.initial: None or tuple = None
        self.neighbours: set = set()

        self.non_parts = defaultdict(int)

    def finish_value(self, row: int, column: int) -> None:
        self.neighbours |= {(row - 1, column), (row, column), (row + 1, column)}
        self.numbers[self.initial] = {
            'value': self.value,
            'neighbours': self.neighbours
        }
        self.neighbours = set()
        self.value = None
        self.initial = None

    def adapt_element(self, row: int, column: int, element: str) -> None:
        match RegexEqual(element):
            case r'\.':
                if self.value:
                    self.finish_value(row, column)
            case r'\d':
                if self.value:
                    self.neighbours |= {(row - 1, column), (row + 1, column)}
                else:
                    self.initial = (row, column)
                    self.neighbours |= {(row - 1, column - 1), (row, column - 1), (row + 1, column - 1),
                                        (row - 1, column), (row + 1, column)}
                    self.value = 0
                self.value = 10 * self.value + int(element)
            case r'\*':
                if self.value:
                    self.finish_value(row, column)
                self.symbols.add((row, column))
                self.gears.add((row, column))
            case _:
                if self.value:
                    self.finish_value(row, column)
                self.symbols.add((row, column))

    def get_sum_of_part_numbers(self) -> int:
        total = 0
        for initial, data_dict in self.numbers.items():
            if self.symbols.intersection(data_dict['neighbours']):
                total += data_dict['value']
            else:
                self.non_parts[data_dict['value']] += 1
        return total

    def get_sum_of_gear_ratios(self) -> int:
        total = 0
        for gear in self.gears:
            numbers_close = [num for num in self.numbers if gear in self.numbers[num]['neighbours']]
            if len(numbers_close) != 2:
                continue
            total += self.numbers[numbers_close[0]]['value'] * self.numbers[numbers_close[1]]['value']
        return total


def get_data(my_file: str) -> list:
    with open(my_file) as f:
        data = f.read()
    data = data.split('\n')
    data = [st.strip() for st in data if st.strip()]
    return data


def get_grid(data: list) -> Grid:
    grid = Grid()
    for row, line in enumerate(data):
        line += '.'
        for column in range(len(line)):
            element = line[column]
            grid.adapt_element(row, column, element)
    return grid


def get_part_result(data: list, part: int) -> int:
    grid = get_grid(data)
    if part == 1:
        return grid.get_sum_of_part_numbers()
    elif part == 2:
        return grid.get_sum_of_gear_ratios()


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
