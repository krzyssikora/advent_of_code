import sys


def get_row(my_file):
    with open(my_file) as f:
        line = f.read().strip()
        line = line.replace(".", "1").replace("^", "0")
        row = list(map(int, line))
    return row


def next_row(previous):
    row = [previous[1]]
    for idx in range(1, len(previous) - 1):
        if previous[idx - 1] == previous[idx + 1]:
            row.append(1)
        else:
            row.append(0)
    row.append(previous[-2])
    return row

def get_map(row, count):
    rows = [row]
    for _ in range(count - 1):
        row = next_row(row)
        rows.append(row)
    return rows


def main(my_file):
    row = get_row(my_file)
    rows = get_map(row, 400000)
    total = 0
    for r in rows:
        total += sum(r)
    print(total)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "18_input.txt"
    main(filename)
