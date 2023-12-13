from collections import deque


pipe_dirs = {
    '-': [(0, -1), (0, 1)],
    '|': [(-1, 0), (1, 0)],
    'L': [(-1, 0), (0, 1)],
    'J': [(-1, 0), (0, -1)],
    '7': [(1, 0), (0, -1)],
    'F': [(1, 0), (0, 1)],
    '.': [],
    'S': [(-1, 0), (1, 0), (0, -1), (0, 1)]}


def create_grid(raw_string: str):
    grid = []
    for row in raw_string.splitlines():
        grid.append([c for c in row])
    return grid


def find_loop(grid: list[list[str]]):
    n_rows, n_cols = len(grid), len(grid[0])
    for row, col in [[r, c] for r in range(n_rows) for c in range(n_cols)]:
        if grid[row][col] == 'S':
            S = [row, col]
            break

    for new_dir in pipe_dirs['S']:
        out_dir = new_dir
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
                    out_dir2 = (-new_dir[0], -new_dir[1])
                    grid[S[0]][S[1]] = find_S_type(out_dir, out_dir2)
                    return [seen, grid]
                else:
                    break
            else:
                new_dir = [d for d in pipe_dirs[grid[pos[0]][pos[1]]]
                           if d != (-new_dir[0], -new_dir[1])][0]
                seen.append(pos)


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


def find_S_type(od1, od2):
    for key in pipe_dirs.keys():
        if key != 'S':
            if od1 in pipe_dirs[key] and od2 in pipe_dirs[key]:
                return key


def solve(s):
    grid = create_grid(s)
    n_row, n_col = len(grid), len(grid[0])
    loop, grid = find_loop(grid)
    count = 0
    for r in range(n_row):
        crossings = 0
        for c in range(n_col):
            if [r, c] in loop:
                if grid[r][c] in ['|', 'L', 'J']:
                    crossings += 1
            else:
                if crossings % 2 == 1:
                    count += 1
    return count


with open('inputs/day10', 'r') as f:
    s = f.read()
    print(solve(s))
