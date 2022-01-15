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


def choices_given_size_0(weights, capacity, size):
    ret_list = list()
    weights.sort(reverse=True)
    if len(weights) < size or weights[0] > capacity or weights[0] * size < capacity:
        return None
    if size == 1:
        pos = 0
        while True:
            if pos >= len(weights) or weights[pos] < capacity:
                return None
            if weights[pos] == capacity:
                return [{weights[pos]}]
            pos += 1
    for weight in weights:
        temp_weights = weights.copy()
        temp_weights.remove(weight)

        temp_choices = choices_given_size_0(temp_weights, capacity - weight, size - 1)
        if temp_choices:
            for temp_choice in temp_choices:
                new_set = {weight}.union(temp_choice)
                if new_set not in ret_list:
                    ret_list.append(new_set)
    return ret_list


def choices_given_size(weights, capacity, size):
    values_choices = choices_by_size(capacity, size, weights)
    ret_list = list()
    for value, choice in values_choices:
        ret_list.append(set(choice))
    return ret_list


def choices_by_size(capacity, size, weights):
    weights.sort(reverse=True)
    if capacity < 0:
        return None
    elif capacity == 0:
        if size == 0:
            return [[0, []]]
        else:
            return None
    elif size == 0:  # but capacity > 0, so no chance to find exact choice
        return None
    ret_list = list()
    max_value = 0
    for weight in weights:
        # weights_without_weight = weights.copy()
        # weights_without_weight.remove(weight)
        weights_after_weight = weights[weights.index(weight) + 1:].copy()
        # result = choices_by_size(capacity - weight, size - 1, weights_without_weight)
        result = choices_by_size(capacity - weight, size - 1, weights_after_weight)
        if result is not None:
            for value, choice in result:
                if capacity >= value + weight >= max_value:
                    max_value = value + weight
                    max_choice = [weight] + choice
                    ret_list.append([max_value, max_choice])
    return ret_list


def choices_with_quantum_entanglement(choices):
    ret_list = list()
    for choice in choices:
        ret_list.append([list(choice), quantum_entanglement(choice)])
    ret_list.sort(key=lambda x: x[1])
    return ret_list


def find_splits(weights, capacity, groups):
    """
    Returns the split such that the first three subsets are chosen in a way that they:
    * sum up to capacity
    * are shortest possible
    * out of the shortest - the product is the smalles
    """
    sizes = [1 for _ in range(groups)]  # size in sizes denotes the length of a chosen list
    steps = [0 for _ in range(groups)]  # step in steps denotes the index of a choice from lists at the same position
    not_in_use = [True for _ in range(groups)]  # True means we should search for choices
    size_index = 0
    all_choices = [list() for _ in range(groups)]
    weights_not_used = set(weights.copy())
    weights_used = set()
    choices = list()
    choice = [list(), None]
    while True:
        if size_index >= groups:
            if len(weights_not_used) == 0:
                # return all_choices
                the_choice = list()
                for ind in range(4):
                    the_choice.append(all_choices[ind][steps[ind]])
                return the_choice
            print("not found")
            return None
        size = sizes[size_index]
        if size + groups - 1 > len(weights):
            if size_index > 0:
                sizes[size_index] = 1
                steps[size_index] = 0
                not_in_use[size_index] = True
                size_index -= 1
                steps[size_index] += 1
                weights_not_used = weights_not_used.union(choice[0])
                weights_used = weights_used.difference(choice[0])
                continue
            # go back with size_index
            print("not found")
            return None
        if not_in_use[size_index]:
            choices = choices_given_size(list(weights_not_used), capacity, sizes[size_index])
            if choices is None or len(choices) == 0:
                size += 1
                sizes[size_index] = size
                continue
            not_in_use[size_index] = False
            choices = choices_with_quantum_entanglement(choices)
            all_choices[size_index] = choices
        step = steps[size_index]
        if step >= len(choices):
            steps[size_index] = 0
            not_in_use[size_index] = True
            continue
        choice = choices[step]
        weights_used = weights_used.union(choice[0])
        weights_not_used = weights_not_used.difference(choice[0])
        size_index += 1


def main(my_file):
    weights = get_weights(my_file)
    weights.sort(reverse=True)
    compartments = 4
    group_capacity = sum(weights) // compartments
    answers = find_splits(weights, group_capacity, compartments)
    for answer in answers:
        print(answer[0])
    print(answers[0][1])


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "24_input.txt"
    main(filename)
