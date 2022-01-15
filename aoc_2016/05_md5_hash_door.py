import hashlib


def part_1(hex_input):
    length = 0
    counter = 0
    password = ""
    while True:
        length += 1
        for number in range(10 ** (length - 1), 10 ** length):
            my_number = hex_input + "0" * (length - len(str(number))) + str(number)
            md5_hash = hashlib.md5(my_number.encode()).hexdigest()
            if md5_hash.startswith("00000"):
                counter += 1
                password += md5_hash[5]
                print(counter, password)
                if counter == 8:
                    break
        if counter == 8:
            break
    return password


def part_2(hex_input):
    length = 0
    counter = 0
    password = "________"
    while True:
        length += 1
        for number in range(10 ** (length - 1), 10 ** length):
            my_number = hex_input + "0" * (length - len(str(number))) + str(number)
            md5_hash = hashlib.md5(my_number.encode()).hexdigest()
            if md5_hash.startswith("00000") and md5_hash[5].isdigit():
                position = int(md5_hash[5])
                if position > 7 or password[position] != "_":
                    continue
                counter += 1
                password = password[:position] + md5_hash[6] + password[position + 1:]
                print(counter, password)
                if counter == 8:
                    break
        if counter == 8:
            break
    return password


def main():
    # hex_input = "abc"
    hex_input = "ugkcyxxp"
#    print(part_1(hex_input))
    print(part_2(hex_input))


if __name__ == "__main__":
    main()
