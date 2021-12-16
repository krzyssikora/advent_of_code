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
    while True:
        first = packets[position]
        if first != "0":
            position += 5
        else:
            position += 5
            break
    return position


def find_versions(packets, position):
    versions = list()
    version, position = get_bits(packets, position, 3)
    versions.append(version)
    type_id, position = get_bits(packets, position, 3)
    if type_id == 4:
        position = read_literal(packets, position)
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
    versions, position = find_versions(packets, 0)
    print(sum(versions))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "16_input.txt"
    main(filename)
