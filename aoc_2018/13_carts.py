import sys


class Cart:
    """
    which_direction:
        0 = left        (* -1j)
        1 = straight    (-----)
        2 = right       (* 1j )
    """
    def __init__(self, position, direction):
        self.position = position
        self.direction = direction
        self.which_direction = 0
        self.moving = True


def get_carts_and_tracks(my_file):
    with open(my_file) as f:
        lines = f.readlines()
    tracks = dict()
    carts = list()
    directions = {"v": 1j, "^": -1j, ">": 1, "<": -1}
    for y, line in enumerate(lines):
        line = line.strip("\n")
        for x, char in enumerate(line):
            if char in "v^><":
                carts.append(Cart(x + y * 1j, directions[char]))
            elif char in "\\/+":
                tracks[x + y * 1j] = char
    carts.sort(key=lambda c: c.position.real)
    carts.sort(key=lambda c: c.position.imag)
    return carts, tracks


def move_cart(carts, tracks, cart, part):
    cart.position += cart.direction
    # check if collision happened
    for crt_id, crt in enumerate(carts):
        if cart != crt and crt.moving and cart.position == crt.position:
            cart.moving = False
            crt.moving = False
            break
    if cart.moving:
        # change cart's direction
        new_char = tracks.get(cart.position, None)
        if new_char == "\\":
            if cart.direction.real == 0:
                cart.direction *= -1j
            else:
                cart.direction *= 1j
        elif new_char == "/":
            if cart.direction.real == 0:
                cart.direction *= 1j
            else:
                cart.direction *= -1j
        elif new_char == "+":
            directions = {0: -1j, 1: 1, 2: 1j}
            direction = directions[cart.which_direction]
            cart.direction *= direction
            cart.which_direction = (cart.which_direction + 1) % 3
    elif part == 1:
        return str(int(cart.position.real)) + "," + str(int(cart.position.imag))


def display_carts_tracks(carts, tracks):
    dim_x = int(max([track.real for track in tracks])) + 1
    dim_y = int(max([track.imag for track in tracks])) + 1
    carts_pos = dict()
    cart_chars = {1j: "v", -1j: "^", 1: ">", -1: "<"}
    for cart in carts:
        carts_pos[cart.position] = cart_chars[cart.direction]
    for y in range(dim_y):
        for x in range(dim_x):
            if x + y * 1j in carts_pos:
                print(carts_pos[x + y * 1j], end="")
            elif x + y * 1j in tracks:
                print(tracks[x + y * 1j], end="")
            else:
                print(" ", end="")
        print()
    print("-" * dim_x, len(carts))


def part_1(carts, tracks):
    while True:
        for cart in carts:
            if cart.moving:
                result = move_cart(carts, tracks, cart, 1)
                if result:
                    return result
        carts.sort(key=lambda x: x.position.real)
        carts.sort(key=lambda x: x.position.imag)


def part_2(carts, tracks):
    while len(carts) > 1:
        for cart in carts:
            move_cart(carts, tracks, cart, 2)
        carts = [cart for cart in carts if cart.moving]
        carts.sort(key=lambda x: x.position.real)
        carts.sort(key=lambda x: x.position.imag)
    for cart in carts:
        return str(int(cart.position.real)) + "," + str(int(cart.position.imag))


def main(my_file):
    carts, tracks = get_carts_and_tracks(my_file)
    print("part 1:", part_1(carts, tracks))
    carts, tracks = get_carts_and_tracks(my_file)
    print("part 2:", part_2(carts, tracks))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "13_input.txt"
    main(filename)
