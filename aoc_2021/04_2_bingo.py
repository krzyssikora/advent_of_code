input_data = "input.txt"
# import random_numbers and boards
with open(input_data) as f:
    first_line = f.readline().strip("\n").split(",")
    random_numbers = [int(x) for x in first_line]
    boards = list()
    board = list()
    lines = f.readlines()
    for line in lines:
        line = line.strip("\n")
        if len(line) > 0:
            board_row = line.split()
            board.append([int(x) for x in board_row])
        else:
            if len(board) > 0:
                boards.append(board)
            board = list()
    if len(board) > 0:
        boards.append(board)

boards_won = list()

numbers_chosen = [[[0 for _ in range(5)] for _ in range(5)] for _ in range(len(boards))]
while True:
    won = False
    if len(boards_won) == len(boards):
        break
    number_chosen = random_numbers.pop(0)
    for board_number in range(len(boards)):
        # tick chosen number in all boards
        for i in range(5):
            for j in range(5):
                if boards[board_number][i][j] == number_chosen:
                    numbers_chosen[board_number][i][j] += 1
        # check if there is a row ticked:
        for i in range(5):
            won = True
            for j in range(5):
                won = won and (numbers_chosen[board_number][i][j] > 0)
            if won:
                if board_number not in boards_won:
                    boards_won.append(board_number)
                break
        if won:
            if len(boards_won) == len(boards):
                break
            else:
                continue
        # check if there is a column ticked
        for j in range(5):
            won = True
            for i in range(5):
                won = won and (numbers_chosen[board_number][i][j] > 0)
            if won:
                if board_number not in boards_won:
                    boards_won.append(board_number)
                break
        if won:
            if len(boards_won) == len(boards):
                break
            else:
                continue
    if won:
        won = False
        if board_number not in boards_won:
            boards_won.append(board_number)

#board_number = boards_left[0]
sum_board = 0
for i in range(5):
    for j in range(5):
        if numbers_chosen[board_number][i][j] == 0:
            sum_board += boards[board_number][i][j]
print(number_chosen * sum_board)