import sys


def get_steps_and_sequences(my_file):
    # returns:
    #   steps - a set of all possible steps
    #   sequences - a dictionary:
    #       key - step, value - set of steps that must be completed before the step
    steps = set()
    sequences = dict()
    with open(my_file) as f:
        lines = f.readlines()
        for line in lines:
            before, after = line.strip().split()[1:8:6]
            steps = steps.union({before, after})
            if after in sequences:
                sequences[after].add(before)
            else:
                sequences[after] = {before}
    steps = sorted(list(steps))
    return steps, sequences


def get_sequence(sequences, steps, length, sequence=""):
    chars_to_use = steps.copy()
    while True:
        if len(sequence) == length:
            return sequence
        if len(chars_to_use) == 0:
            return None
        new_sequence = None
        for char in chars_to_use:
            if char not in sequences or len(sequences[char].difference(set(sequence))) == 0:
                new_chars_to_use = chars_to_use.copy()
                new_chars_to_use.remove(char)
                new_sequence = get_sequence(sequences, new_chars_to_use, length, sequence + char)
                if new_sequence is None:
                    continue
                else:
                    break
        return new_sequence


def get_the_job_done_00(sequences, sequence, workers_number):
    workers = [0 for _ in range(workers_number)]
    steps_in_progress = [None for _ in range(workers_number)]
    time = 0
    completed = set()
    while True:
        idx = 0
        if len(completed) == len(sequence):
            break
        step = sequence[idx]
        while step in completed:
            idx += 1
            if idx >= len(sequence):
                print("I ran out of the sequence!!!")
                quit()
            step = sequence[idx]
        required = sequences.get(step, set()).difference(completed)
        if required:
            # required must finish first
            pass
        else:
            # assign the step to a free worker
            free_worker = workers.index(0)
            steps_in_progress[free_worker] = step
            workers[free_worker] = 61 + ord(step) - ord("A")
            # pass the time so that at least one worker is free
            time_elapsed = min(workers)
            while time_elapsed:
                workers_done = set(filter(lambda i: workers[i] == time_elapsed, range(workers_number)))
                workers = [t - time_elapsed for t in workers]
                time += time_elapsed
                for worker in workers_done:
                    completed.add(steps_in_progress[worker])
                    steps_in_progress[worker] = None
            idx += 1
        if idx >= len(sequence):
            print("finishing off")
            last_period = max(workers)
            if last_period:
                for worker_id in range(workers_number):
                    if workers[worker_id]:
                        completed.add(steps_in_progress[worker_id])


def get_the_job_done(sequences, steps, workers_number):
    workers = [0 for _ in range(workers_number)]
    steps_in_progress = [None for _ in range(workers_number)]
    completed = set()
    time = 0
    # cut this
    # completed = {'A', 'C', 'F', 'B'}
    # steps = ["D", "E"]
    # cut this
    while True:
        if len(steps) == 0 and all(worker == 0 for worker in workers):
            break
        possible_steps = [step for step in steps if len(sequences.get(step, set()).difference(completed)) == 0]
        possible_steps.sort(reverse=True)
        while possible_steps:
            step = possible_steps.pop()
            # assign the step to a free worker
            if 0 not in workers:
                break
            steps.remove(step)
            free_worker = workers.index(0)
            steps_in_progress[free_worker] = step
            workers[free_worker] = ord(step) - 4
            possible_steps = [step for step in steps if len(sequences.get(step, set()).difference(completed)) == 0]
            possible_steps.sort(reverse=True)
        # pass the time so that at least one worker is free
        time_elapsed = min(workers)
        if time_elapsed > 0:
            while time_elapsed:
                workers_done = set(filter(lambda w: workers[w] == time_elapsed, range(workers_number)))
                workers = [t - time_elapsed for t in workers]
                time += time_elapsed
                for worker in workers_done:
                    completed.add(steps_in_progress[worker])
                    steps_in_progress[worker] = None
                time_elapsed = min(workers)
        elif max(workers) > 0:
            for i in range(workers_number):
                workers[i] = max(workers[i] - 1, 0)
                if workers[i] == 0:
                    if steps_in_progress[i]:
                        completed.add(steps_in_progress[i])
                        steps_in_progress[i] = None
            time += 1
    return time


def main(my_file):
    steps, sequences = get_steps_and_sequences(my_file)
    print("part 1:", get_sequence(sequences, steps, len(steps)))
    print("part 2:", get_the_job_done(sequences, steps, 5))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "07_input.txt"
    main(filename)
