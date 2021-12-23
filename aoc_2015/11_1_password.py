def next_word(word):
    word_ords = [ord(character) for character in word]
    new_word_ords = list()
    go_left = False
    while True:
        if len(word_ords) == 0:
            break
        last = word_ords.pop()
        last += 1
        if last > 122:
            last = 97
            go_left = True
        new_word_ords = [last] + new_word_ords
        if not go_left:
            new_word_ords = word_ords + new_word_ords
            break
        go_left = False
    new_word = ""
    for elt in new_word_ords:
        new_word += chr(elt)
    return new_word


def check_increasing_triple(word):
    # Passwords must include one increasing straight of at least three letters,
    # like abc, bcd, cde, and so on, up to xyz. They cannot skip letters; abd doesn't count.
    found = False
    position = 2
    order_1 = ord(word[position - 2])
    order_2 = ord(word[position - 1])
    order_3 = ord(word[position])
    length = len(word)
    while True:
        if order_3 - order_2 == order_2 - order_1 == 1:
            found = True
            break
        position += 1
        if position >= length:
            break
        order_1, order_2, order_3 = order_2, order_3, ord(word[position])
    return found


def check_forbidden_chars(word):
    # Passwords may not contain the letters i, o, or l, as these letters can be mistaken
    # for other characters and are therefore confusing.
    if "i" in word or "l" in word or "o" in word:
        return False
    else:
        return True


def check_doubles(word):
    # Passwords must contain at least two different, non-overlapping pairs of letters, like aa, bb, or zz.
    found = 0
    position = 1
    length = len(word)
    while True:
        if word[position] == word[position - 1]:
            found += 1
            position += 3
            if found == 2:
                if word[position - 4] == word[position - 5]:
                    found -= 1
                else:
                    break
        else:
            position += 1
        if position >= length:
            break
    if found == 2:
        return True
    else:
        return False


def remove_forbidden_chars(word):
    lst = list()
    for character in ["i", "l", "o"]:
        pos = word.find(character)
        if pos >= 0:
            lst.append(pos)
    if len(lst) == 0:
        return word
    else:
        pos = min(lst)
        order = ord(word[pos]) + 1
        if order > 122:
            order = 97
        return word[:pos] + chr(order) + "a" * (len(word) - pos)



def is_correct(word):
    return check_forbidden_chars(word) and check_doubles(word) and check_increasing_triple(word)


def main():
    current_password = "vzbxkghb"
    current_password = "vzbxxyzz"
    current_password = remove_forbidden_chars(current_password)
    while True:
        current_password = next_word(current_password)
        if is_correct(current_password):
            break
    print(current_password)


if __name__ == "__main__":
    main()
