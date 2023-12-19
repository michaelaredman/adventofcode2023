import re

example = """R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)"""


def raw_to_instructions(s: str):
    d, l = [], []
    for line in s.splitlines():
        h = re.search(r".+\(\#(\w+)\)", line).group(1)
        d.append({0: 'R', 1: 'D', 2: 'L', 3: 'U'}[int(h[-1])])
        l.append(int(h[0:-1], 16))
    return list(zip(d, l))


d_to_dir = {'L': (0, -1), 'R': (0, 1), 'U': (-1, 0), 'D': (1, 0)}


def instructions_to_coordinates(instructions: list[tuple[str, int]]):
    coords = [(0, 0)]
    p = (0, 0)
    for d, l in instructions:
        dir = d_to_dir[d]
        p = (p[0] + dir[0]*l, p[1] + dir[1]*l)
        coords.append(p)
    return coords


def ins_to_integer_boundary_points(instructions: list[tuple[str, int]]):
    integer_boundary_points = 0
    for d, l in instructions:
        integer_boundary_points += l
    return integer_boundary_points


def shoelace(coords: list[tuple[int, int]]) -> int:
    left_to_right = 0
    right_to_left = 0
    for i in range(len(coords)-1):
        left_to_right += coords[i][0]*coords[i+1][1]
        right_to_left += coords[i+1][0]*coords[i][1]
    return abs(left_to_right - right_to_left)/2


def picks_theorem(instructions: list[tuple[str, int]]):
    coords = instructions_to_coordinates(instructions)
    A = shoelace(coords)
    b = ins_to_integer_boundary_points(instructions)
    # A = i + b/2 - 1
    i = A + 1 - b/2
    total_area = i + b
    return total_area


with open('inputs/day18', 'r') as f:
    s = f.read()
    ins = raw_to_instructions(s)
    print('Part 2: ', picks_theorem(ins))
