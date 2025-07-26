import os
import re
from pathlib import Path
from dataclasses import dataclass
import numpy as np


@dataclass
class Robot:
    x: int
    y: int
    dx: int
    dy: int

    def __str__(self):
        return f"({self.x}, {self.y}) >> [{self.dx}, {self.dy}]"

    def move_n(self, n: int, max_x: int, max_y: int):
        self.x = (self.x + n * self.dx) % max_x
        self.y = (self.y + n * self.dy) % max_y


def get_data_lines(my_file: Path) -> list:
    with open(my_file) as f:
        lines = f.readlines()
    return [line.strip('\n').strip() for line in lines]


def get_robots(lines):
    robots = []
    pattern = r"^p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)$"
    for line in lines:
        m = re.match(pattern, line)
        x, y, dx, dy = list(map(int, m.groups()))
        robot = Robot(x, y, dx, dy)
        robots.append(robot)
    return robots


def get_safety_factor(robots, max_x, max_y):
    # move robots
    for robot in robots:
        robot.move_n(100, max_x, max_y)

    # count robots in quadrants
    quadrants = {q: 0 for q in ["TL", "TR", "BL", "BR"]}
    mid_x = (max_x - 1) // 2
    mid_y = (max_y - 1) // 2
    for robot in robots:
        if robot.x == mid_x or robot.y == mid_y:
            continue
        vertical = "T" if robot.y < mid_y else "B"
        horizontal = "L" if robot.x < mid_x else "R"
        quadrants[vertical + horizontal] += 1
    # for robot in robots:
    #     print(robot)
    # print(quadrants)
    # get safety factor
    safety_factor = 1
    for v in quadrants.values():
        safety_factor *= v

    return safety_factor


def display_grid(robots, max_x, max_y):
    grid = np.array([
        [0 for _ in range(max_x)] for __ in range(max_y)
    ])
    for robot in robots:
        grid[robot.y, robot.x] += 1

    string = ""
    for row in range(max_y):
        for col in range(max_x):
            value = grid[row, col]
            char = "." if value == 0 else "X" if value > 9 else str(value)
            string += char
        string += "\n"
    print(string)


def max_consecutive_run(lst):
    if not lst:
        return 0

    max_run = 1
    current_run = 1

    for i in range(1, len(lst)):
        if lst[i] == lst[i - 1] + 1:
            current_run += 1
            max_run = max(max_run, current_run)
        else:
            current_run = 1

    return max_run


def check_line(robots, max_x, max_y):
    many = 6
    for y in range(max_y // 2):
        y_robots = [r for r in robots if r.y == y]
        if len(y_robots) < many:
            continue
        xs = [r.x for r in y_robots]
        xs.sort()
        if max_consecutive_run(xs) >= many:
            return True
    return False



def part_2(robots, max_x, max_y):
    steps = 0
    while True:
        if steps % 1000 == 0:
            print(steps)
        for robot in robots:
            robot.move_n(1, max_x, max_y)
        steps += 1
        if check_line(robots, max_x, max_y):
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"step {steps}")
            display_grid(robots, max_x, max_y)
            a = input()
            if a != "":
                quit()


def main(my_file: Path, inp: int) -> None:
    lines = get_data_lines(my_file)
    robots = get_robots(lines)
    max_x = 101 if inp == 2 else 11
    max_y = 103 if inp == 2 else 7
    safety_factor = get_safety_factor(robots, max_x, max_y)
    print(f"input {inp}:", safety_factor)

    robots = get_robots(lines)
    part_2(robots, max_x, max_y)


if __name__ == "__main__":
    root = Path(__file__).parent
    prefix = Path(__file__).name.split("_")[0]
    # for inpt, filename in enumerate([f"{prefix}_inp.txt", f"{prefix}_input.txt"], 1):
    for inpt, filename in enumerate([f"{prefix}_input.txt"], 2):
        if (root / filename).exists():
            main(root / filename, inpt)
