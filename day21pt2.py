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


total_steps = 26_501_365
side_length = 66

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


def subsquares_reachable(steps: int):
    steps += 1
    return ((steps) * (steps + 1)) // 2

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
# top left
# row range = 0 -> S[0]
# col range = 0 -> S[1] - 1
# bottom left
# row range = S[0] + 1 -> n_row - 1
# col range = 0 -> S[1]
# bottom right
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
                for _ in range(c_min, c_max+1)]
    Q.appendleft((start, 1))
    visited[start[0]][start[1]] = True
    distance[start[0]][start[1]] = 1
    dirs = ((0, 1), (0, -1), (1, 0), (-1, 0))
    while Q:
        p, dist = Q.pop()
        for d in dirs:
            p_new = (p[0] + d[0], p[1] + d[1])
            if not (r_min <= p_new[0] <= r_max and c_min <= p_new[1] <= c_max):
                continue
            if not visited[p_new[0]][p_new[1]] and grid[p_new[0]][p_new[1]] == '.':
                Q.appendleft((p_new, dist+1))
                distance[p_new[0]][p_new[1]] = dist+1
                visited[p_new[0]][p_new[1]] = True
    return distance
