import sys


def get_data(my_file):
    with open(my_file) as f:
        packets = f.read().strip("\n")
    return packets


def make_binary(packets):
    bits = ""
    for bit in packets:
        bits += bin(int(bit, 16))[2:].rjust(4, "0")
    return bits


def get_bits(packet, position, bits):
    output = int(packet[position: position + bits], 2)
    return output, position + bits


def read_literal(packets, position):
    binary_value = ""
    while True:
        first = packets[position]
        binary_value += packets[position + 1: position + 5]
        position += 5
        if first == "0":
            break
    decimal_value = int(binary_value, 2)
    return decimal_value, position


def get_value(packets, position):
    value = 0
    version, position = get_bits(packets, position, 3)
    type_id, position = get_bits(packets, position, 3)
    if type_id == 4:
        value, position = read_literal(packets, position)
    else:
        values = list()
        if packets[position] == "0":
            position += 1
            length, position = get_bits(packets, position, 15)
            end_position = position + length
            while True:
                new_value, position = get_value(packets, position)
                values.append(new_value)
                if position == end_position:
                    break
        elif packets[position] == "1":
            position += 1
            subpackets, position = get_bits(packets, position, 11)
            for _ in range(subpackets):
                new_value, position = get_value(packets, position)
                values.append(new_value)
        if type_id == 0:
            value = sum(values)
        elif type_id == 1:
            value = 1
            for elt in values:
                value *= elt
        elif type_id == 2:
            value = min(values)
        elif type_id == 3:
            value = max(values)
        elif type_id == 5:
            value = 1 * (values[0] > values[1])
        elif type_id == 6:
            value = 1 * (values[0] < values[1])
        elif type_id == 7:
            value = 1 * (values[0] == values[1])
    return value, position


def find_versions(packets, position):
    versions = list()
    version, position = get_bits(packets, position, 3)
    versions.append(version)
    type_id, position = get_bits(packets, position, 3)
    if type_id == 4:
        value, position = read_literal(packets, position)
    else:
        if packets[position] == "0":
            position += 1
            length, position = get_bits(packets, position, 15)
            end_position = position + length
            while True:
                new_versions, position = find_versions(packets, position)
                versions += new_versions
                if position == end_position:
                    break
        elif packets[position] == "1":
            position += 1
            subpackets, position = get_bits(packets, position, 11)
            for _ in range(subpackets):
                new_versions, position = find_versions(packets, position)
                versions += new_versions
    return versions, position


def main(my_file):
    packets = make_binary(get_data(my_file))
    value, position = get_value(packets, 0)
    print(value)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "16_input.txt"
    main(filename)
