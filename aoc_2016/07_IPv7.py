import sys


def get_ips(my_file):
    ips = list()
    with open(my_file) as f:
        lines = f.readlines()
        for line in lines:
            ip = {"inner": list(), "outer": list()}
            line = line.split("[")
            ip["outer"].append(line[0])
            for i in range(1, len(line)):
                inner, outer = line[i].split("]")
                ip["inner"].append(inner)
                ip["outer"].append(outer.strip())
            ips.append(ip)
    return ips


def is_abba(string):
    for pos in range(len(string) - 3):
        if string[pos] != string[pos + 1] and string[pos] == string[pos + 3] and string[pos + 1] == string[pos + 2]:
            return True
    return False


def all_aba(str_list):
    abas = list()
    for string in str_list:
        for pos in range(len(string) - 2):
            if string[pos] != string[pos + 1] and string[pos] == string[pos + 2]:
                abas.append(string[pos: pos + 3])
    return abas


def reverse_aba(aba):
    return aba[1] + aba[0] + aba[1]


def supports_tls(ip):
    for inner in ip["inner"]:
        if is_abba(inner):
            return False
    for outer in ip["outer"]:
        if is_abba(outer):
            return True
    return False


def main(my_file):
    ips = get_ips(my_file)
    print("part 1")
    counter = 0
    for ip in ips:
        if supports_tls(ip):
            counter += 1
    print(counter)
    print("part 2")
    counter = 0
    for ip in ips:
        abas_in = all_aba(ip["inner"])
        abas_out = all_aba(ip["outer"])
        for aba_out in abas_out:
            if reverse_aba(aba_out) in abas_in:
                counter += 1
                break
    print(counter)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "07_input.txt"
    main(filename)
