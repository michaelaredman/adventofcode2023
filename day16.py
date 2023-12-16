import sys
import itertools
sys.setrecursionlimit(10000)

beam_dir2 = {
    '.': {(0, 1): [(0, 1)],
          (0, -1): [(0, -1)],
          (1, 0): [(1, 0)],
          (-1, 0): [(-1, 0)]},
    '/': {(0, 1): [(-1, 0)],
          (0, -1): [(1, 0)],
          (1, 0): [(0, -1)],
          (-1, 0): [(0, 1)]},
    '\\': {(0, 1): [(1, 0)],
           (0, -1): [(-1, 0)],
           (1, 0): [(0, 1)],
           (-1, 0): [(0, -1)]},
    '|': {(0, 1): [(-1, 0), (1, 0)],
          (0, -1): [(-1, 0), (1, 0)],
          (1, 0): [(1, 0)],
          (-1, 0): [(-1, 0)]},
    '-': {(1, 0): [(0, 1), (0, -1)],
          (-1, 0): [(0, 1), (0, -1)],
          (0, 1): [(0, 1)],
          (0, -1): [(0, -1)]}
}

D = [(1, 0), (0, 1), (-1, 0), (0, -1)]
beam_dir = {
    '.': {(r, c): [(r, c)] for r, c in D},
    '/': {(r, c): [(-c, -r)] for r, c in D},
    '\\': {(r, c): [(c, r)] for r, c in D},
    '|': {(0, 1): [(-1, 0), (1, 0)], (0, -1): [(-1, 0), (1, 0)],
          (1, 0): [(1, 0)], (-1, 0): [(-1, 0)]},
    '-': {(1, 0): [(0, 1), (0, -1)], (-1, 0): [(0, 1), (0, -1)],
          (0, 1): [(0, 1)], (0, -1): [(0, -1)]}
}


def energized(grid: list[list[chr]], p=(0, 0), d=(0, 1)) -> int:
    n_row, n_col = len(grid), len(grid[0])
    global E
    E = [[0 for _ in range(n_col)] for _ in range(n_row)]
    global seen
    seen = set()
    path(p, d, grid)
    return E


def path(p: tuple[int, int], d: tuple[int, int], grid: list[list[chr]]):
    if (p, d) in seen:
        return
    seen.add((p, d))
    E[p[0]][p[1]] = 1
    object_map = beam_dir[grid[p[0]][p[1]]]
    new_directions = object_map[d]
    for new_d in new_directions:
        new_p = (p[0] + new_d[0], p[1] + new_d[1])
        if 0 <= new_p[0] < len(grid) and 0 <= new_p[1] < len(grid[0]):
            path(new_p, new_d, grid)


def solve(s: str, p=(0, 0), d=(0, 1)) -> int:
    grid = [[chr for chr in line] for line in s.splitlines()]
    e_grid = energized(grid, p, d)
    return sum(sum(row) for row in e_grid)


example = """.|...\\....
|.-.\\.....
.....|-...
........|.
..........
.........\\
..../.\\\\..
.-.-/..|..
.|....-|.\\
..//.|...."""


def find_maximum(s: str):
    grid = [[chr for chr in line] for line in s.splitlines()]
    n_row, n_col = len(grid), len(grid[0])
    left_wall = zip(
        (tuple(p) for p in zip(range(n_row), itertools.repeat(0))),
        itertools.repeat((0, 1)))
    right_wall = zip(
        (tuple(p) for p in zip(range(n_row), itertools.repeat(n_col-1))),
        itertools.repeat((0, -1)))
    top_wall = zip(
        (tuple(p) for p in zip(itertools.repeat(0), range(n_col))),
        itertools.repeat((1, 0)))
    bottom_wall = zip(
        (tuple(p) for p in zip(itertools.repeat(n_row-1), range(n_col))),
        itertools.repeat((-1, 0)))
    max_energy = 0
    for p, d in itertools.chain(left_wall, right_wall, top_wall, bottom_wall):
        max_energy = max(max_energy, solve(s, p, d))
    return max_energy


print("Part 1 example:", solve(example))
print('Part 2 example:', find_maximum(example))

with open('inputs/day16', 'r') as f:
    s = f.read()
    print("Part 1:", solve(s))
    print("Part 2:", find_maximum(s))
