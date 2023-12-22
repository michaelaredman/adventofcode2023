from collections import deque
from math import inf
# the grid is split into four equally sized regions
# find distance to every point in the four regions

# each copy of the grid is split as follows
#  -------------------
#  |        :        |
#  |   2    :    1   |
#  |        :        |
#  |- - - - S - - - -|
#  |        :        |
#  |   3    :    4   |
#  |        :        |
#  -------------------

# 1 =======

# pattern A:
# for reaching 1 from the lower left, the count is:
# sum_{rs = 0}^steps 1 +  (steps - rs)
# = (steps + 1) + (steps + 1)*steps - 1/2 * (steps) * (steps + 1)
# = steps + 1 + steps^2 + steps - 1/2 steps^2 - 1/2 steps
# = 1/2 steps^2
# also need the zero term!
# ---> a step is 2 * side_length

# we want the sum of this up to the:
# (total_steps - dist_to_point_from_corner) // (side_length * 2)
# symmetry gives us the similar terms

# now we just need the other ones

#  pattern B:
# 1 from lower right is simply
# (total_steps - dist_to_point_from_corner - side_length) // (side_length * 2)
# count is the same

# pattern C:
# exact same as pattern B for 1 for upper left

#  pattern D:
# upper right is the same but with
#  (total_steps - dist_to_point_from_corner - side_length*2) // (side_length * 2)

# by symmetry the rest are the same but the relevant corner is rotated clockwise

# 2 =======
#


# count[i] = number of subsquares of a given pattern and corner reachable in i (side_length*2) steps
# these are ust triangle numbers! e.g. for those lower-left 1s reachable by four steps from the origin
# 4
# 3 4
# 2 3 4
# 1 2 3 4
# 0 1 2 3 4

# we add one to steps as we start with the first subsquare accessible

# I have not counted the middle tram lines, so should i consider the tramline to the left of each subsquare as part of the square?
# - then add the S positions
# -> S positions are an even number away so we can ignore them!


def subsquares_reachable(steps: int, first):
    # if odd then return the squares, if even then return the oblong numbers
    if first:
        return (steps + 1) * (steps + 1)
    else:
        return ((steps) * (steps + 1))

# sum(count[:(k+1)]) is the total number of these identical pattern and corners reachable from the zeroth case of this pattern
# in k steps

# so, for each subsquare we calculate the distance to each point from each of the four corners

# we order the corners as we have ordered the subsquares: (top right, top left, bottom left, bottom right)

# get the start square for each corner
# get the bounds for each subsquare

# first find S
# top right (1)
# row range = 0 -> S[0] - 1
# col range = S[1] -> n_col - 1
# top left (2)
# row range = 0 -> S[0]
# col range = 0 -> S[1] - 1
# bottom left (3)
# row range = S[0] + 1 -> n_row - 1
# col range = 0 -> S[1]
# bottom right (4)
# row range = S[0] -> n_row - 1
# col range = S[1] + 1 -> n_col - 1


def bfs(grid: list[list[str]],
        r_min: int, r_max: int,
        c_min: int, c_max: int,
        start: tuple[int, int]):
    visited = [[False for _ in range(c_min, c_max+1)]
               for _ in range(r_min, r_max+1)]
    Q = deque()
    distance = [[inf for _ in range(c_min, c_max+1)]
                for _ in range(r_min, r_max+1)]
    Q.appendleft((start, 1))
    visited[start[0] - r_min][start[1] - c_min] = True
    distance[start[0] - r_min][start[1] - c_min] = 1
    dirs = ((0, 1), (0, -1), (1, 0), (-1, 0))
    while Q:
        p, dist = Q.pop()
        for d in dirs:
            p_new = (p[0] + d[0], p[1] + d[1])
            if not (r_min <= p_new[0] <= r_max and c_min <= p_new[1] <= c_max):
                continue
            if not visited[p_new[0] - r_min][p_new[1] - c_min] and grid[p_new[0]][p_new[1]] == '.':
                Q.appendleft((p_new, dist+1))
                distance[p_new[0] - r_min][p_new[1] - c_min] = dist+1
                visited[p_new[0] - r_min][p_new[1] - c_min] = True
    return distance


def find_S(grid: list[list[str]]) -> tuple[int, int]:
    n_row, n_col = len(grid), len(grid[0])
    for r in range(n_row):
        for c in range(n_col):
            if grid[r][c] == 'S':
                return (r, c)
    assert False


def print_matrix(grid):
    warn = '33[93m'
    endw = '33[0m'
    blue = '33[94m'
    cyan = '33[96m'
    green = '33[92m'
    fail = '33[91m'
    bold = '33[1m'
    underline = '33[4m'
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            print(f"{grid[row][col]} ", end='')
        print()


def solve(grid: list[list[str]]):
    total_steps = 26_501_365
    n_row, n_col = len(grid), len(grid[0])
    side_length = (n_row + 1) // 2
    full_length = n_row
    S = find_S(grid)
    bounds_list = [(0, S[0] - 1, S[1], n_col - 1),
                   (0, S[0], 0, S[1] - 1),
                   (S[0] + 1, n_row - 1, 0, S[1]),
                   (S[0], n_row - 1, S[1] + 1, n_col - 1)]
    corners_list = [[(0, n_col - 1), (0, S[1]),
                     (S[0] - 1, S[1]), (S[0] - 1, n_col - 1)],  # TR, TL, BL, BR
                    [(0, 0), (S[0], 0),
                     (S[0], S[1] - 1), (0, S[1] - 1)],  # TL, BL, BR, TR
                    [(n_row - 1, 0), (n_row - 1, S[1]),
                     (S[0] + 1, S[1]), (S[0] + 1, 0)],  # BL, BR, TR, TL
                    [(n_row - 1, n_col - 1), (S[0], n_col - 1),
                     (S[0], S[1] + 1), (n_row - 1, S[1] + 1)]  #  BR, TR, TL, BL
                    ]
    # distance for a subsquare from a given corner: D[subsquare][corner][r][c]
    D = []
    for i, bounds in enumerate(bounds_list):
        D_i = []
        for corner in corners_list[i]:
            D_i.append(bfs(grid, *bounds, corner))
        D.append(D_i)
    total_reachable = 0
    for subsquare in range(4):
        for corner in range(4):
            distances = D[subsquare][corner]
            n_row, n_col = len(distances), len(distances[0])
            # loop through distancess follows:
            # for corner 0: include full range
            # for 1 and 2: include anticlockwise edge
            # for 3: inclulde only the enclosed region
            for row in range(n_row):
                for col in range(n_col):
                    if distances[row][col] != inf:
                        ns = num_steps(
                            corner, distances[row][col], total_steps, full_length)
                        if ns % 2 == 0:
                            first, second = ns//2, ns//2
                        else:
                            first, second = 1 + ns//2, ns//2
                        if corner in [0, 2, 3]:
                            # take evens first
                            if distances[row][col] == 0:
                                total_reachable += subsquares_reachable(
                                    first, True)
                            else:
                                total_reachable += subsquares_reachable(
                                    second, False)
                        else:
                            # take odds first
                            if distances[row][col] == 1:
                                total_reachable += subsquares_reachable(
                                    first, True)
                            else:
                                total_reachable += subsquares_reachable(
                                    second, False)
    total_reachable += 4 * (total_steps // full_length) * \
        (1 + (total_steps // full_length))
    return total_reachable

# true = 622926941971282


def num_steps(x: int, point_offset: int, total_steps: int, full_length: int):
    match x:
        # pattern D: top right for 1
        case 0:
            return (total_steps - point_offset - full_length) // (full_length)
        # pattern C: top left for 1
        case 1:
            return (total_steps - point_offset - full_length//2) // (full_length)
        # pattern A: bottom left for 1
        case 2:
            return (total_steps - point_offset) // (full_length)
        # pattern B: bottom right for 1
        case 3:
            return (total_steps - point_offset - full_length//2 - 1) // (full_length)
        case _:
            assert False


with open('inputs/day21', 'r') as f:
    s = f.read()
    grid = [[c for c in line] for line in s.splitlines()]
    print(solve(grid))
