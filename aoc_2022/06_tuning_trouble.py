import sys
import os


def get_data_lines(my_file):
    with open(my_file) as f:
        lines = f.readlines()
    return [line.strip('\n').strip() for line in lines]


def get_min_number_of_chars_for_the_marker(string, chars):
    for idx in range(chars, len(string)):
        if len(set(string[idx - chars: idx])) == chars:
            return idx
    return None


def main(my_file):
    test_strings = [
        'mjqjpqmgbljsphdztnvjfqwrcgsmlb',
        'bvwbjplbgvbhsrlpgdmjqwftvncz',
        'nppdvjthqldpwncqszvftbrmjlhg',
        'nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg',
        'zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw'
    ]
    test_1 = [7, 5, 6, 10, 11]
    test_2 = [19, 23, 23, 29, 26]
    print(all(get_min_number_of_chars_for_the_marker(string, 4) == val for string, val in zip(test_strings, test_1)))
    print(all(get_min_number_of_chars_for_the_marker(string, 14) == val for string, val in zip(test_strings, test_2)))
    lines = get_data_lines(my_file)
    string = lines[0]
    print("part 1:", get_min_number_of_chars_for_the_marker(string, 4))
    print("part 2:", get_min_number_of_chars_for_the_marker(string, 14))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = f'{os.path.basename(__file__)[:2]}_input.txt'
    main(filename)
