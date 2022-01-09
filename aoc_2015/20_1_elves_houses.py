import primefac


def sum_of_factors(number):
    prime_factors = list(primefac.primefac(number))
    factorization = dict()
    for factor in prime_factors:
        if factor not in factorization:
            factorization[factor] = prime_factors.count(factor)
    factors_sum = 1
    for factor, power in factorization.items():
        tmp_sum = 0
        for n in range(power + 1):
            tmp_sum += factor ** n
        factors_sum *= tmp_sum
    return factors_sum


def main(inp_number):
    inp_number //= 10
    number = inp_number // 5
    while True:
        sf = sum_of_factors(number)
        print(number, sf)
        if sf >= inp_number:
            print(number)
            break
        number += 1


if __name__ == "__main__":
    main(29000000)
