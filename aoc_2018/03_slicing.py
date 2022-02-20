import sys
import re


def get_claims(my_file):
    with open(my_file) as f:
        lines = f.readlines()
    pattern = r"#([0-9]+) @ ([0-9]+),([0-9]+): ([0-9]+)x([0-9]+)"
    claims = dict()
    for line in lines:
        idx, x, y, dx, dy = map(int, re.findall(pattern, line)[0])
        claims[idx] = (x, y, x + dx, y + dy)
    return claims


def is_empty(claim):
    x1, y1, x2, y2 = claim
    return x1 == x2 or y1 == y2


def intersect_ranges(a1, b1, a2, b2):
    return a2 < b1 and a1 < b2


def intersect_claims(claim_1, claim_2):
    return intersect_ranges(claim_1[0], claim_1[2], claim_2[0], claim_2[2]) and \
           intersect_ranges(claim_1[1], claim_1[3], claim_2[1], claim_2[3])


def cut_claims(claim_1, claim_2):
    if not intersect_claims(claim_1, claim_2):
        return [claim_1], None
    x11, y11, x12, y12 = claim_1
    x21, y21, x22, y22 = claim_2
    # cut claim_2 to boundaries of claim_1
    x21, y21 = max(x11, x21), max(y11, y21)
    x22, y22 = min(x12, x22), min(y12, y22)
    # now claim_1 is within claim_2
    claims = {
        (x11, y11, x22, y21),
        (x22, y11, x12, y22),
        (x21, y22, x12, y12),
        (x11, y21, x21, y12)
    }
    single_claims = {claim for claim in claims if not is_empty(claim)}
    intersection = (x21, y21, x22, y22)
    if is_empty(intersection):
        intersection = None
    return single_claims, intersection


def add_claim(singles, doubles, new_claim):
    new_singles = set()
    while True:
        if len(singles) == 0:
            new_singles.add(new_claim)
            break
        single = singles.pop()
        tmp_singles, intersection = cut_claims(single, new_claim)
        new_singles = new_singles.union(tmp_singles)
        if intersection:
            doubles.add(intersection)
    return new_singles, doubles


def arrange_doubles(doubles):
    arranged_doubles = set()
    for double in doubles:
        if len(arranged_doubles) == 0:
            arranged_doubles.add(double)
        else:
            new_doubles = [double]
            new_differences = set()
            for ok_double in arranged_doubles:
                for tmp_double in new_doubles:
                    difference, intersection = cut_claims(tmp_double, ok_double)
                    new_differences = new_differences.union(difference)
                new_doubles = set()
                for elt in new_differences:
                    if elt not in new_doubles:
                        new_doubles.add(elt)
                if len(new_differences) == 0:
                    break
                new_differences = set()
            for elt in new_doubles:
                if elt not in arranged_doubles:
                    arranged_doubles.add(elt)
    return arranged_doubles


def not_overlapping(claims):
    many = len(claims)
    potential = set()
    for i in range(1, many + 1):
        promising = True
        for j in range(1, many + 1):
            if i == j:
                continue
            if intersect_claims(claims[i], claims[j]):
                promising = False
                break
        if promising:
            potential.add(i)
    if len(potential) == 1:
        return potential.pop()
    else:
        return potential


def find_doubles(claims):
    singles = set()
    doubles = set()
    while True:
        if len(claims) == 0:
            break
        claim = claims.pop(min(claims, key=claims.get))
        singles, doubles = add_claim(singles, doubles, claim)
    print("doubles found, now they need to be simplified")
    doubles = arrange_doubles(doubles)
    area = 0
    for double in doubles:
        area += (double[2] - double[0]) * (double[3] - double[1])
    return area


def main(my_file):
    claims = get_claims(my_file)
    print("part 1:", find_doubles(claims.copy()))
    print("part 2:", not_overlapping(claims))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "03_input.txt"
    main(filename)
