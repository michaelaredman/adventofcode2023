from collections import deque

example = """-L|F7
7S-7|
L|7||
-L-J|
L|-JF"""

example2 = """FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L"""

example3 = """.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ..."""

pipe_dirs = {
    '-': [(0, -1), (0, 1)],
    '|': [(-1, 0), (1, 0)],
    'L': [(-1, 0), (0, 1)],
    'J': [(-1, 0), (0, -1)],
    '7': [(1, 0), (0, -1)],
    'F': [(1, 0), (0, 1)],
    '.': [],
    'S': [(-1, 0), (1, 0), (0, -1), (0, 1)]}

# for all directions around S
#     follow the pipes
#     if we return to S then we have our path
#     remeber to save the sequence of locations we find on our path


def create_grid(raw_string: str):
    grid = []
    for row in raw_string.splitlines():
        grid.append([c for c in row])
    return grid


def dfs(pos: tuple[int, int], grid: list[list[str]]):
    pass


def find_loop(grid: list[list[str]]) -> list[tuple[int, int]]:
    n_rows, n_cols = len(grid), len(grid[0])
    for row, col in [[r, c] for r in range(n_rows) for c in range(n_cols)]:
        if grid[row][col] == 'S':
            S = [row, col]

    for new_dir in pipe_dirs['S']:
        seen = [S]
        pos = S
        while True:
            pos = [pos[0] + new_dir[0], pos[1] + new_dir[1]]
            # oob check
            if not (0 <= pos[0] < n_rows and 0 <= pos[1] < n_cols):
                break
            # check if the new position could have accepted us
            if (-new_dir[0], -new_dir[1]) not in pipe_dirs[grid[pos[0]][pos[1]]]:
                break
            if pos in seen:
                if pos == S:
                    return seen
                else:
                    break
            else:
                new_dir = [d for d in pipe_dirs[grid[pos[0]][pos[1]]]
                           if d != (-new_dir[0], -new_dir[1])][0]
                seen.append(pos)


def flood_fill(point: list[int, int],
               grid: list[list[str]],
               loop: list[list[int, int]]):
    n_row, n_col = len(grid), len(grid[0])
    seen = []
    seen.append(point)
    dirs = [[-1, 0], [1, 0], [0, 1], [0, -1]]
    q = deque()
    q.append(point)
    while len(q):
        p = q.pop()
        for dir in dirs:
            new_p = [p[0] + dir[0], p[1] + dir[1]]
            # oob or in loop or seen then dont add to queue
            if new_p in loop or new_p in seen \
                    or not (0 <= new_p[0] < n_row and 0 <= new_p[1] < n_col):
                continue
            seen.append(new_p)
            q.append(new_p)
    return seen


def count_inside(grid: list[list[str]], loop: list[list[str, str]]):
    n_row, n_col = len(grid), len(grid[0])
    outside = {}

    outside = flood_fill([0, 0], grid, loop)

    count = 0
    for row in range(n_row):
        for col in range(n_col):
            if [row, col] not in outside and [row, col] not in loop \
                    and grid[row][col] == '.':
                count += 1
    return count

# print(find_farthest(create_grid(example)))


# with open('inputs/day10', 'r') as f:
#     s = f.read()
#     loop = find_loop(create_grid(s))
#     print(count_inside(create_grid(s), loop))

loop = find_loop(create_grid(example3))
print(count_inside(create_grid(example3), loop))


def print_grid(grid, loop):
    warn = '\033[93m'
    endw = '\033[0m'
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if [row, col] in loop:
                print(f"{warn}{grid[row][col]}{endw}", end='')
            else:
                print(f"{grid[row][col]}", end='')
        print()


print_grid(create_grid(example3), find_loop(create_grid(example3)))
