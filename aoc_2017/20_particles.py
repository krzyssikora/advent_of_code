import sys
import re


def get_data(my_file):
    pattern = f"p=<([ ]*[-]*[0-9]+),([ ]*[-]*[0-9]+),([ ]*[-]*[0-9]+)>, " \
              f"v=<([ ]*[-]*[0-9]+),([ ]*[-]*[0-9]+),([ ]*[-]*[0-9]+)>, " \
              f"a=<([ ]*[-]*[0-9]+),([ ]*[-]*[0-9]+),([ ]*[-]*[0-9]+)>"
    data = list()
    with open(my_file) as f:
        lines = f.readlines()
        for line in lines:
            matches = list(map(int, re.findall(pattern, line.strip())[0]))
            if len(matches) > 0:
                data.append({"p": matches[:3],
                             "v": matches[3:6],
                             "a": matches[6:]})
    return data


def make_step(particle):
    for i in range(3):
        particle["v"][i] += particle["a"][i]
        particle["p"][i] += particle["v"][i]
    return particle


def approximate_steps(particle, time):
    # not necessary, but works for part 1, too :)
    return sum([abs(particle["p"][i] + particle["v"][i] * time + 0.5 * particle["a"][i] * time ** 2) for i in range(3)])


def distance(tpl):
    # manhattan distance of a tuple from (0,0,0)
    return abs(tpl[0]) + abs(tpl[1]) + abs(tpl[2])


def lowest_value(data, indicator="a"):
    minimum = None
    closest = -1
    for i in range(len(data)):
        if minimum is None or distance(data[i][indicator]) < minimum:
            minimum = distance(data[i][indicator])
            closest = i
    return closest


def collisions(data):
    to_consider = set(_ for _ in range(len(data)))
    collided = set()
    while True:
        if len(to_consider) == 0:
            break
        particle_id = to_consider.pop()
        particle = data[particle_id]
        position = particle["p"]
        new_collisions = set()
        for idx in to_consider:
            if data[idx]["p"] == position:
                new_collisions.add(idx)
        if len(new_collisions) > 0:
            new_collisions.add(particle_id)
            to_consider = to_consider.difference(new_collisions)
            collided = collided.union(new_collisions)
    return collided


def main(my_file):
    data = get_data(my_file)
    lowest_acceleration = distance(data[lowest_value(data, "a")]["a"])
    suspects = list(filter(lambda x: (distance(x["a"]) == lowest_acceleration), data))
    print("part 1:", data.index(suspects[lowest_value(suspects, "v")]))
    particles_number = len(data)
    without_collision = 0
    while True:
        if without_collision >= 100:  # arbitrary value, 10 is enough
            break
        for i in range(particles_number):
            data[i] = make_step(data[i])
        collided = collisions(data)
        if len(collided) > 0:
            queue = sorted(list(collided), reverse=True)
            for idx in queue:
                data.pop(idx)
        if len(data) < particles_number:
            particles_number = len(data)
            without_collision = 0
        else:
            without_collision += 1
    print("part 2:", len(data))



if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "20_input.txt"
    main(filename)
