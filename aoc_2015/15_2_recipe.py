import sys
import re
import itertools


def get_ingredients(my_file):
    ingredients = dict()
    with open(my_file) as f:
        lines = f.readlines()
        for line in lines:
            ingredient = list(map(int, re.findall(r"([-]*[0-9]+)", line)))
            ingredients[line.split()[0]] = ingredient
    return ingredients


def get_max_value(ingredients):
    properties_num = 4
    names = list(ingredients.keys())
    names_num = len(names)
    indexes_combinations = itertools.combinations(range(1, 101), names_num - 1)
    best_value = 0
    for comb in indexes_combinations:
        tmp_list = [0] + list(comb) + [100]
        amounts = [tmp_list[i + 1] - tmp_list[i] for i in range(names_num)]
        calories = 0
        for i, name in enumerate(names):
            calories += amounts[i] * ingredients[name][-1]
        if calories != 500:
            continue
        properties = [0 for _ in range(properties_num)]
        for i, name in enumerate(names):
            properties = [properties[j] + amounts[i] * ingredients[name][j] for j in range(properties_num)]
        value = 1
        for prop in properties:
            if prop <= 0:
                value = 0
                break
            else:
                value *= prop
        if value > best_value:
            best_value = value
    print(best_value)



def main(my_file):
    ingredients = get_ingredients(my_file)
    print(ingredients)
    get_max_value(ingredients)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "15_input.txt"
    main(filename)