import sys

# part 1
# A X rock
# B Y paper
# C Z scissors

shape_win = {
    'X': 1,
    'Y': 2,
    'Z': 3,
}

outcome_win = {
    'X': {
        'A': 3,
        'B': 0,
        'C': 6
    },
    'Y': {
        'A': 6,
        'B': 3,
        'C': 0
    },
    'Z': {
        'A': 0,
        'B': 6,
        'C': 3
    }
}

# part 2
# X lose
# Y draw
# Z win

result_win = {
    'X': 0,
    'Y': 3,
    'Z': 6
}

shape_from_result_win = {
    'X': {
        'A': 3,
        'B': 1,
        'C': 2
    },
    'Y': {
        'A': 1,
        'B': 2,
        'C': 3
    },
    'Z': {
        'A': 2,
        'B': 3,
        'C': 1
    }
}


def get_data_lines(my_file):
    with open(my_file) as f:
        lines = f.readlines()
    return [line.strip() for line in lines]


def get_my_score_1(lines):
    score = 0
    for line in lines:
        his, mine = line.strip('\n').split()
        score += shape_win[mine] + outcome_win[mine][his]
    return score


def get_my_score_2(lines):
    score = 0
    for line in lines:
        his, mine = line.strip('\n').split()
        score += result_win[mine] + shape_from_result_win[mine][his]
    return score


def main(my_file):
    lines = get_data_lines(my_file)

    print("part 1:", get_my_score_1(lines))
    print("part 2:", get_my_score_2(lines))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "02_input.txt"
    main(filename)
