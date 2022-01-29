def check_a_against_commands(a):
    # the commands output binary form of a + 2572 in reverse order infinitely
    binary = bin(a + 2572)[:1:-1]
    if len(binary) % 2 == 0:
        firsts = binary[::2]
        seconds = binary[1::2]
        first = firsts[0]
        second = seconds[0]
        if all([k == first for k in firsts]) and all([k == second for k in seconds]) and first != second:
            return a
    return False


def main():
    a = 1
    while True:
        if check_a_against_commands(a):
            print("smallest a is", a)
            break
        a += 1


if __name__ == "__main__":
    main()
