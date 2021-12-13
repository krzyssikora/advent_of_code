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
    my_number = ""
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
