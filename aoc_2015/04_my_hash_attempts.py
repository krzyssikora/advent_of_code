def binary_string(input_string):
    ret_string = ""
    for character in input_string:
        char_string = bin(ord(character))[2:]

        ret_string += "0" * (8 - len(char_string)) + char_string  # + "\n"
    return ret_string


def indices(first, step):
    return [(step * i + first) % 16 for i in range(16)]


def get_constants():
    import math
    # values K1, K2, ..., K64
    # k_value[i] = K(i + 1)
    k_values = [hex(int(abs(math.sin(i + 1) * 2 ** 32)))[2:] for i in range(64)]
    # values S1, S2, ..., S64
    # s_values[i] = S(i + 1)
    s_values = list()
    for i in range(16):
        s_values.append((i % 4) * 5 + 7)
    for i in range(16):
        r = i % 4
        s_values.append((r + 2) * (r + 5) // 2)
    for i in range(16):
        r = i % 4
        s_values.append(-r ** 3 + 2 * r ** 2 + 6 * r + 4)
    for i in range(16):
        r = i % 4
        s_values.append((r + 4) * (r + 3) // 2)
    return k_values, s_values


def a_function(vec_b, vec_c, vec_d, round_index):
    int_b, int_c, int_d = int(vec_b, 16), int(vec_c, 16), int(vec_d, 16)
    if round_index == 0:
        return hex((int_b & int_c) | (~int_b & int_d))
    elif round_index == 1:
        return hex((int_b & int_d) | (int_c & ~int_d))
    elif round_index == 2:
        return hex(int_b ^ int_c ^ int_d)
    elif round_index == 3:
        return hex(int_c ^ (int_b | ~int_d))
    else:
        return None


def add_modulo(hex_1, hex_2):
    int_1, int_2 = int(hex_1, 16), int(hex_2, 16)
    return hex((int_1 + int_2) % (2 ** 32))


def get_hash(input_string):
    # change into binary with padding
    binary = binary_string(input_string) + "1"
    length = len(binary)
    remainder = length % 512
    if remainder <= 448:
        padding_length = 448 - remainder
    else:
        padding_length = 960 - remainder
    ending = bin(length - 1)[2:]
    ending = "0" * (64 - len(ending)) + ending
    binary += "0" * padding_length + ending
    # words of 32 bits in hexadecimal: values M0, M1, M2, ...
    # m_value[i] = Mi
    m_values = list()
    for i in range(len(binary) // 32):
        m_values.append(hex(int(binary[32 * i: 32 * (i + 1)], 2))[2:])
    vector_a, vector_b, vector_c, vector_d = "01234567", "89abcdef", "fedcba98", "76543210"
    k_values, s_values = get_constants()
    rounds = [[0, 1], [1, 5], [5, 3], [0, 7]]
    for round_index in range(4):
        m_indices = indices(rounds[round_index][0], rounds[round_index][1])
        for i in range(16):
            m_index = m_indices[i]
            value = add_modulo(vector_a, a_function(vector_b, vector_c, vector_d, round_index))
            value = add_modulo(m_values[m_index], value)
            value = add_modulo(k_values[16 * round_index + i], value)
            # shift by S
            binary = bin(int(value, 16))[2:]
            if len(binary) < 32:
                binary = "0" * (32 - len(binary)) + binary
            shift = s_values[16 * round_index + i]
            value = hex(int(binary[shift:] + binary[:shift], 2))
            value = add_modulo(vector_b, value)[2:]
            vector_a, vector_b, vector_c, vector_d = vector_d, value, vector_b, vector_c
    vector_a, vector_b, vector_c, vector_d = \
        add_modulo(vector_a, "01234567")[2:], add_modulo(vector_b, "89abcdef")[2:], \
        add_modulo(vector_c, "fedcba98")[2:], add_modulo(vector_d, "76543210")[2:]
    return vector_a + vector_b + vector_c + vector_d


def hex_append(hex_number, decimal, length):
    decimal_string = str(decimal)
    decimal_string = hex_number + "0" * (length - len(decimal_string)) + decimal_string
    return decimal_string


def check_hex_number(input_string):
    import hashlib
    hashed = hashlib.md5(input_string.encode()).hexdigest()
    correct = True
    for i in range(6):
        correct = correct and (hashed[i] == "0")
    return correct


def main():
    length = 0
    input_hex = "bgvyzdsv"
    found = False
    while True:
        length += 1
        print("length:", length)
        for number in range(10 ** (length - 1), 10 ** length):
            my_number = hex_append(input_hex, number, length)
            if check_hex_number(my_number):
                found = True
                break
        if found:
            break
    print(my_number)


if __name__ == "__main__":
    main()
