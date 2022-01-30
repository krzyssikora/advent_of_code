import sys


def single_step(bank):
    maximum = max(bank)
    length = len(bank)
    max_pos = bank.index(maximum)
    bank[max_pos] = 0
    last_pos = max_pos + 1 + maximum % length
    many = maximum // length
    for pos in range(max_pos + 1, last_pos):
        bank[pos % length] += many + 1
    for pos in range(last_pos, max_pos + 1 + length):
        bank[pos % length] += many
    return bank


def steps_number(bank):
    banks = {tuple(bank)}
    count = 0
    while True:
        count += 1
        bank = single_step(bank)
        if tuple(bank) in banks:
            break
        else:
            banks.add(tuple(bank))
    return count


def cycles_number(bank):
    banks = [bank.copy()]
    count = 0
    while True:
        count += 1
        bank = single_step(bank)
        if bank in banks:
            break
        else:
            banks.append(bank.copy())
    return count - banks.index(bank)


def main(my_file):
    bank = list(map(int, open(my_file).read().strip().split()))
    print("part 1:", steps_number(bank.copy()))
    print("part 2:", cycles_number(bank.copy()))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "06_input.txt"
    main(filename)
