def illegal_character(my_line):
    brackets = {"(": ")",
                "[": "]",
                "{": "}",
                "<": ">"
                }
    list_of_chars = list()
    for character in my_line:
        if character in brackets:
            list_of_chars.append(character)
        else:
            if list_of_chars:
                previous = list_of_chars.pop()
            else:
                return character  # case like "())"
            if brackets.get(previous) == character:
                continue
            else:
                return character  # case like "(]"
    return ""


def evaluate_illegal_score(my_line):
    scores = {")":  3,
              "]":  57,
              "}":  1197,
              ">":  25137
              }
    illegal = illegal_character(my_line)
    if illegal:
        score = scores.get(illegal, 0)
    else:
        score = 0
    return score


def main():
    my_file = "10_input.txt"
    with open(my_file) as f:
        lines = f.readlines()
        total = 0
        for line in lines:
            total += evaluate_illegal_score(line)
    print(total)


if __name__ == "__main__":
    main()
