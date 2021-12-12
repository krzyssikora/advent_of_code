def complementary_characters(my_line):
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
                # incorrect character
                return None
            if brackets.get(previous) == character:
                continue
            else:
                # incorrect character
                return None
    # incomplete line
    return_list = list()
    while True:
        if len(list_of_chars) == 0:
            break
        elt = list_of_chars.pop()
        return_list.append(brackets.get(elt))
    return return_list


def evaluate_completion_score(my_line):
    scores = {")":  1,
              "]":  2,
              "}":  3,
              ">":  4
              }
    completion = complementary_characters(my_line)
    if completion:
        score = 0
        for elt in completion:
            score *= 5
            score += scores.get(elt, 0)
    else:
        score = 0
    return score


def main():
    my_file = "10_input.txt"
    with open(my_file) as f:
        lines = f.readlines()
        all_scores = list()
        for line in lines:
            line = line.strip("\n")
            score = evaluate_completion_score(line)
            if score:
                all_scores.append(score)
    all_scores.sort()
    print(all_scores[(len(all_scores) - 1) // 2])


if __name__ == "__main__":
    main()
