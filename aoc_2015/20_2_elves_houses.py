import primefac
import math

"""
Now:
Elf no 1 delivers to 1, 2, ..., 50
Elf no 2 delivers to 2, 4, ..., 100
Elf no 3 delivers to 3, 6, ..., 150
...
Elf no k delivers to k, 2k, ..., 50k

240 = (2 ** 4)(3 ** 1)(5 ** 1)
factors: 
1, 3, 5, 15,
2, 6, 10, 30,
4, 12, 20, 60
8, 24, 40, 120
16, 48, 80, 240 
Elves not delivering:
1, 2, 3, 4 
"""


def get_factors(factorization):
    num_factors = 1
    for freq in factorization.values():
        num_factors *= (freq + 1)
    factors = [1]
    for prime, freq in factorization.items():
        tmp_factors = factors.copy()
        for i in range(freq):
            factors += [old * prime ** (i + 1) for old in tmp_factors]
    return sorted(factors, reverse=True)


def sum_of_factors(number):
    # returns sum of factors
    prime_factors = list(primefac.primefac(number))
    factorization = dict()
    for factor in prime_factors:
        if factor not in factorization:
            factorization[factor] = prime_factors.count(factor)
    factors = get_factors(factorization)
    factors_sum = 0
    stop = math.ceil(number / 50)
    for factor in factors:
        if factor < stop:
            break
        factors_sum += factor
    return factors_sum


def main(inp_number):
    inp_number = math.ceil(inp_number / 11)
    number = 665280  # answer from part 1
    while True:
        sf = sum_of_factors(number)
        if sf >= inp_number:
            print(number)
            break
        number += 1


if __name__ == "__main__":
    main(29000000)
