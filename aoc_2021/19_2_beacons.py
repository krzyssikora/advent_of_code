import itertools
import re
import sys


class Scanner:
    def __init__(self, ident, ):
        self.ident = ident
        self.beacons = list()
        self.distances = list()
        self.axis_number = (0, 1, 2)
        self.axis_sign = 0  # binary number: 7 = change all signs, 4 change first, 2 change second...
        self.shift = [0, 0, 0]
        self.ref_scanner = None

    def get_distances(self):
        # or rather Manhattan distance components
        self.distances = list()
        for i in range(len(self.beacons)):
            distances = list()
            b1 = self.beacons[i]
            for j in range(len(self.beacons)):
                if i != j:
                    b2 = self.beacons[j]
                    distance = [abs(b1[0] - b2[0]), abs(b1[1] - b2[1]), abs(b1[2] - b2[2])]
                    distances.append(distance)
            distances.sort(key=lambda x: x[0])
            self.distances.append(distances)

    def common_beacons(self, other: "Scanner"):
        minimum_number = 12
        orders = list(itertools.permutations([0, 1, 2]))  # permutations to change axes
        common_beacons = dict()
        for permutation in orders:
            for i in range(len(self.distances)):
                for j in range(len(other.distances)):
                    many = 0
                    for k in range(len(self.distances[i])):
                        if [self.distances[i][k][permutation[_]] for _ in range(3)] in other.distances[j]:
                            many += 1
                        if many >= minimum_number - 1:
                            common_beacons[i] = j
                            self.axis_number = permutation
                            break
                    if i in common_beacons:
                        break
            if len(common_beacons) >= minimum_number:
                break
        # now checking shifts
        print("common_beacons:", common_beacons)
        shifts = [list() for _ in range(8)]
        for my_ind in common_beacons:
            other_ind = common_beacons[my_ind]
            b1 = self.beacons[my_ind]
            b2 = other.beacons[other_ind]
            for ap in range(8):  # ap = axis positive; same as self. axis_sign
                shift = [b2[i] - b1[self.axis_number[i]] * (-1) ** (ap & 2 ** (2 - i) == 0) for i in range(3)]
                if shift not in shifts[ap]:
                    shifts[ap].append(shift)
        for shift in shifts:
            if len(shift) == 1:
                self.shift = shift[0]
                self.axis_sign = shifts.index(shift)
                self.ref_scanner = other.ident
                print(self.ident, "refers to  : ", self.ref_scanner)
                return True
        return False

    def change_beacon_to_other(self, beacon):
        # changes beacon's coordinates ot the ones with respect to scanner self.ref_scanner
        shift = self.shift
        shifted_beacon = beacon.copy()
        # firstly rotate axes
        shifted_beacon = [- shifted_beacon[self.axis_number[i]] for i in range(3)]
        # secondly, change signs on axes
        for i in range(3):
            if (2 ** (2-i)) & self.axis_sign:
                shifted_beacon[i] *= -1
        # thirdly, add shift
        shifted_beacon = [shifted_beacon[i] + shift[i] for i in range(3)]
        return shifted_beacon


def get_scanners_from_data(my_file):
    scanners = list()
    with open(my_file) as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            if len(line) > 0:
                if line.startswith("---"):
                    beacons = list()
                    ident = int(re.search(r"[0-9]+", line).group())
                    new_scanner = Scanner(ident)
                    scanners.append(new_scanner)
                    new_scanner.beacons = beacons
                else:
                    beacons.append([int(_) for _ in line.split(",")])
    return scanners


def find_beacons(my_file):
    scanner_positions = [[0, 0, 0]]
    max_manhattan_distance = 0
    scanners = get_scanners_from_data(my_file)
    for scanner in scanners:
        scanner.get_distances()
    master_scanner = Scanner(len(scanners))
    master_scanner.beacons = master_scanner.beacons + scanners[0].beacons
    master_scanner.get_distances()
    print("Beacons in master:", len(master_scanner.beacons))
    scanners_to_align = [i for i in range(len(scanners))]
    scanners_to_align.remove(0)
    while True:
        if len(scanners_to_align) == 0:
            break
        current_scanner_id = scanners_to_align[0]
        current_scanner = scanners[current_scanner_id]
        print("scanners to align:", scanners_to_align, current_scanner.ident, current_scanner_id)
        print("checking match of", current_scanner_id, "with", master_scanner.ident)
        there_is_a_match = current_scanner.common_beacons(master_scanner)
        print(there_is_a_match)
        if there_is_a_match:
            new_position = current_scanner.shift
            for position in scanner_positions:
                distance = sum([abs(position[_] - new_position[_]) for _ in range(3)])
                if distance > max_manhattan_distance:
                    max_manhattan_distance = distance
            scanner_positions.append(new_position)
            print("scanner number", len(scanner_positions) - 1, " is at", current_scanner.shift)
            scanners_to_align.remove(current_scanner_id)
            current_beacons = list()
            for beacon in current_scanner.beacons:
                current_beacons.append(current_scanner.change_beacon_to_other(beacon))
            for beacon in current_beacons:
                if beacon not in master_scanner.beacons:
                    master_scanner.beacons.append(beacon)
            master_scanner.get_distances()
            print("Beacons in master:", len(master_scanner.beacons))
        else:
            scanners_to_align.remove(current_scanner_id)
            scanners_to_align.append(current_scanner_id)
    print(len(scanner_positions))
    for scanner in scanner_positions:
        print(scanner)
    print(max_manhattan_distance)


def main(my_file):
    find_beacons(my_file)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        filename = sys.argv[1]
    elif len(sys.argv) == 3:
        filename = ""
    else:
        filename = "19_input.txt"
    main(filename)
