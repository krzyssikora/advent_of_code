import numpy as np
from collections import defaultdict
from pathlib import Path
import heapq


DIRECTIONS = ['N', 'E', 'S', 'W']
DIR_VECTORS = {
    'N': (-1, 0),
    'E': (0, 1),
    'S': (1, 0),
    'W': (0, -1)
}


def get_data_lines(my_file: Path) -> list:
    with open(my_file) as f:
        lines = f.readlines()
    return [line.strip('\n').strip() for line in lines]


def get_maze(lines):
    start, end = None, None
    maze = np.array([list(line) for line in lines])
    rows, cols = maze.shape
    for row in range(rows):
        for col in range(cols):
            if maze[row, col] == "S":
                start = (row, col)
                maze[row, col] = "."
            elif maze[row, col] == "E":
                end = (row, col)
                maze[row, col] = "."
    return maze, start, end


def turn_left(dr):
    return DIRECTIONS[(DIRECTIONS.index(dr) - 1) % 4]


def turn_right(dr):
    return DIRECTIONS[(DIRECTIONS.index(dr) + 1) % 4]


def best_maze_score(maze, start, end):
    nrows, ncols = maze.shape
    # visited = {}  # {(row, col, direction): min_cost}
    min_cost = {}
    previous = defaultdict(list)
    final_states = []  # (cost, row, col, direction)

    # Priority queue: (cost, row, col, direction)
    heap = []
    heapq.heappush(heap, (0, start[0], start[1], 'E'))
    min_cost[(start[0], start[1], 'E')] = 0

    while heap:
        cost, row, col, direction = heapq.heappop(heap)
        current = (row, col, direction)

        if (row, col) == end:
            if not final_states or cost == final_states[0][0]:
                final_states.append((cost, row, col, direction))
            elif cost < final_states[0][0]:
                # current final_states are not final
                final_states = [(cost, row, col, direction)]
            continue

        # Skip if we already have a better cost
        if min_cost.get(current, float('inf')) < cost:
            continue

        # Move forward
        drow, dcol = DIR_VECTORS[direction]
        new_row, new_col = row + drow, col + dcol
        if 0 <= new_row < nrows and 0 <= new_col < ncols and maze[new_row, new_col] == '.':
            new_state = (new_row, new_col, direction)
            new_cost = cost + 1
            if new_cost < min_cost.get(new_state, float('inf')):
                min_cost[new_state] = new_cost
                previous[new_state] = [current]
                heapq.heappush(heap, (new_cost, new_row, new_col, direction))
            elif new_cost == min_cost.get(new_state):
                previous[new_state].append(current)

        # Turn left
        new_direction = turn_left(direction)
        new_state = (row, col, new_direction)
        new_cost = cost + 1000
        if new_cost < min_cost.get(new_state, float('inf')):
            min_cost[new_state] = new_cost
            previous[new_state] = [current]
            heapq.heappush(heap, (new_cost, row, col, new_direction))
        elif new_cost == min_cost.get(new_state):
            previous[new_state].append(current)

        # Turn right
        new_direction = turn_right(direction)
        new_state = (row, col, new_direction)
        new_cost = cost + 1000
        if new_cost < min_cost.get(new_state, float('inf')):
            min_cost[new_state] = new_cost
            previous[new_state] = [current]
            heapq.heappush(heap, (new_cost, row, col, new_direction))
        elif new_cost == min_cost.get(new_state):
            previous[new_state].append(current)

    # Reconstruct all paths from final_states
    all_paths = []

    def backtrack(state, path):
        row, col, direction = state
        if (row, col, direction) == (start[0], start[1], 'E'):
            path.append(start)
            all_paths.append(path[::-1])
            return
        for prev in previous[state]:
            backtrack(prev, path + [(row, col)])

    if final_states:
        for cost, row, col, direction in final_states:
            backtrack((row, col, direction), [(row, col)])
        return final_states[0][0], all_paths
    else:
        return -1, []


def main(my_file: Path, inp: int) -> None:
    lines = get_data_lines(my_file)
    maze, start, end = get_maze(lines)
    score, paths = best_maze_score(maze, start, end)
    places_visited = set()
    for p in paths:
        places_visited |= set(p)

    print(f"input {inp}:", score, len(places_visited))


if __name__ == "__main__":
    root = Path(__file__).parent
    prefix = Path(__file__).name.split("_")[0]
    for inpt, filename in enumerate([f"{prefix}_in.txt", f"{prefix}_inp.txt", f"{prefix}_input.txt"], 1):
        if (root / filename).exists():
            main(root / filename, inpt)
