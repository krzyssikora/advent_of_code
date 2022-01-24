import sys
import re


def get_discs(my_file):
    discs = list()
    with open(my_file) as f:
        lines = f.readlines()
        for line in lines:
            values = re.findall("([0-9]+)", line)
            discs.append(list(map(int, [values[1], values[3]])))
    return discs


def get_equations(discs):
    # equation = [a, b] means that x is congruent to b mod a
    equations = list()
    for i, disc in enumerate(discs):
        equations.append([disc[0], (-disc[1] - i - 1) % disc[0]])
    return equations


def solve_two_equations(equation_1, equation_2):
    # https://en.wikipedia.org/wiki/Chinese_remainder_theorem#Computation
    a1, b1 = equation_1
    a2, b2 = equation_2
    gcd, n, m = extended_euclids_algorithm(a1, a2)
    x = b2 * n * a1 + b1 * m * a2
    if 2 * abs(x) < a1 * a2:
        if x < 0:
            x += a1 * a2
        elif x > 0:
            x -= a1 * a2
    return a1 * a2, x


def solve_equations(equations):
    equation_1 = equations.pop()
    while True:
        if len(equations) == 0:
            break
        equation_2 = equations.pop()
        equation_1 = solve_two_equations(equation_1, equation_2)
    return equation_1[1] % equation_1[0]


def extended_euclids_algorithm(a, b):
    # https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm
    r = [a, b]
    s = [1, 0]
    t = [0, 1]
    idx = 2
    while True:
        q = r[idx - 2] // r[idx - 1]
        new_r = r[idx - 2] - q * r[idx - 1]
        if new_r == 0:
            break
        r.append(new_r)
        s.append(s[idx - 2] - q * s[idx - 1])
        t.append(t[idx - 2] - q * t[idx - 1])
        idx += 1
    return r[-1], s[-1], t[-1]


def main(my_file):
    discs = get_discs(my_file)
    equations = get_equations(discs)
    print(f"part 1: {solve_equations(equations)}")
    equations = get_equations(discs)
    equations.append([11, 11 - 7])
    print(equations)
    print(f"part 2: {solve_equations(equations)}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "15_input.txt"
    main(filename)
