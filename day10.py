
example = """-L|F7
7S-7|
L|7||
-L-J|
L|-JF"""

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


eg = create_grid(example)
for line in eg:
    print(line)


def find_farthest(grid: list[list[str]]) -> list[tuple[int, int]]:
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
                    print(seen)
                    return len(seen)//2
                else:
                    break
            else:
                new_dir = [d for d in pipe_dirs[grid[pos[0]][pos[1]]]
                           if d != (-new_dir[0], -new_dir[1])][0]
                seen.append(pos)


# print(find_farthest(create_grid(example)))

with open('inputs/day10', 'r') as f:
    s = f.read()
    print(find_farthest(create_grid(s)))
