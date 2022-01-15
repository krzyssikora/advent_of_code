import sys


def get_weights(my_file):
    with open(my_file) as f:
        values = list(map(int, f.read().strip("\n").split("\n")))
    return values


def quantum_entanglement(weights):
    product = 1
    for weight in weights:
        product *= weight
    return product


def smallest_choice(weights, capacity):
    ret_list = list()
    # greedy algorithm, does not have to be correct
    for weight in weights:
        if weight <= capacity:
            ret_list.append(weight)
            capacity -= weight
    return ret_list


def main(my_file):
    weights = get_weights(my_file)
    weights.sort(reverse=True)
    compartments = 3
    group_capacity = sum(weights) // compartments
    if compartments * group_capacity != sum(weights):
        quit()
    choice = list()
    current_weights = weights.copy()
    for _ in range(compartments):
        current = smallest_choice(current_weights, group_capacity)
        print(sum(current), len(current), quantum_entanglement(current))
        choice.append(current)
        current_weights = sorted(list(set(current_weights).difference(set(current))), reverse=True)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "24_input.txt"
    main(filename)
