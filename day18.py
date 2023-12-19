import re
from collections import deque

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


def grid_dimensions(seq: list[list[str, int]]):
    max_left, max_right = 0, 0
    max_up, max_down = 0, 0
    i, j = 0, 0
    for d, l in seq:
        match d:
            case 'L':
                j -= l
            case 'R':
                j += l
            case 'U':
                i -= l
            case 'D':
                i += l
        max_left = min(j, max_left)
        max_right = max(j, max_right)
        max_up = min(i, max_up)
        max_down = max(i, max_down)
    return [max_left, max_right, max_up, max_down]

# stolen from stackexchange


def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


def parse_input(s: str):
    d, l, c = [], [], []
    for line in s.splitlines():
        m = re.search(r'(\w) (\d+) \(#(\w+)\)', line)
        d.append(m.group(1)), l.append(int(m.group(2))
                                       ), c.append(hex_to_rgb(m.group(3)))
    return list(zip(d, l, c))


d_to_dir = {'L': (0, -1), 'R': (0, 1), 'U': (-1, 0), 'D': (1, 0)}


def create_grid(g_dims: list[int], instructions):
    max_left, max_right, max_up, max_down = g_dims
    n_row, n_col = max_down - max_up + 1, max_right - max_left + 1
    print(f"{n_row=}")
    print(f"{n_col=}")
    P = [-max_up, -max_left]
    print(f"{P=}")
    grid = [['.' for _ in range(n_col)] for _ in range(n_row)]
    grid[P[0]][P[1]] = '#'
    for d, l, c in instructions:
        dir = d_to_dir[d]
        for step in range(l):
            P = [P[0] + dir[0], P[1] + dir[1]]
            grid[P[0]][P[1]] = '#'
    return grid


# p_input = parse_input(example)
# print(grid_dimensions([[d, l] for d, l, _ in p_input]))

# new_grid = create_grid(grid_dimensions([[d, l] for d, l, _ in p_input]),
#                        p_input)
# for line in new_grid:
#     for c in line:
#         print(c, sep='', end='')
#     print()

dirs = [(0, 1), (0, -1), (-1, 0), (1, 0)]


def fill_lava(grid: list[list[str]]):
    n_row, n_col = len(grid), len(grid[0])
    outside = [[False for _ in range(n_col)] for _ in range(n_row)]
    for row in [0, n_row-1]:
        for col in range(n_col):
            if grid[row][col] != '#' and not outside[row][col]:
                q = deque()
                q.append([row, col])
                while q:
                    p = q.pop()
                    if grid[p[0]][p[1]] != '#' and not outside[p[0]][p[1]]:
                        outside[p[0]][p[1]] = '#'
                        for dir in dirs:
                            p_next = [p[0] + dir[0], p[1] + dir[1]]
                            if 0 <= p_next[0] < n_row and 0 <= p_next[1] < n_col:
                                q.append(p_next)
    for row in range(n_row):
        for col in [0, n_col - 1]:
            if grid[row][col] != '#' and not outside[row][col]:
                q = deque()
                q.append([row, col])
                while q:
                    p = q.pop()
                    if grid[p[0]][p[1]] != '#' and not outside[p[0]][p[1]]:
                        outside[p[0]][p[1]] = True
                        for dir in dirs:
                            p_next = [p[0] + dir[0], p[1] + dir[1]]
                            if 0 <= p_next[0] < n_row and 0 <= p_next[1] < n_col:
                                q.append(p_next)
    for r in range(n_row):
        for c in range(n_col):
            if not outside[r][c]:
                grid[r][c] = '#'
    return grid


def count_lava(grid):
    n_row, n_col = len(grid), len(grid[0])
    count = 0
    for r in range(n_row):
        for c in range(n_col):
            if grid[r][c] == '#':
                count += 1
    return count


# print()

# filled_grid = fill_lava(new_grid)
# for line in filled_grid:
#     for c in line:
#         print(c, sep='', end='')
#     print()

# print(f"{count_lava(filled_grid)=}")

with open('inputs/day18', 'r') as f:
    s = f.read()
    parsed_input = parse_input(s)
    grid_d = grid_dimensions([(d, l) for d, l, _ in parsed_input])
    grid = create_grid(grid_d, parsed_input)
    f_grid = fill_lava(grid)
    print(f"{count_lava(f_grid)=}")
