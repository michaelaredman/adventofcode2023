example = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#....."""


def expand_grid(s: str):
    grid = [[c for c in line] for line in s.splitlines()]
    n_row, n_col = len(grid), len(grid[0])
    expand_row = [True for _ in range(n_row)]
    expand_col = [True for _ in range(n_col)]
    for r in range(n_row):
        for c in range(n_col):
            if grid[r][c] == '#':
                expand_row[r] = False
                expand_col[c] = False
    temp = []
    for r in range(n_row):
        temp.append(grid[r])
        if expand_row[r]:
            temp.append(grid[r])
    grid = temp
    n_row, n_col = len(grid), len(grid[0])
    temp = []
    for r in range(n_row):
        temp_row = []
        for c in range(n_col):
            temp_row.append(grid[r][c])
            if expand_col[c]:
                temp_row.append('.')
        temp.append(temp_row)
    grid = temp
    return grid


def solve(s: str):
    grid = expand_grid(s)
    n_row, n_col = len(grid), len(grid[0])
    P = []
    for r in range(n_row):
        for c in range(n_col):
            if grid[r][c] == '#':
                P.append([r, c])
    total_distance = 0
    for i in range(len(P)):
        for j in range(i, len(P)):
            total_distance += abs(P[i][0] - P[j][0]) + abs(P[i][1] - P[j][1])
    return total_distance


print(expand_grid(example))
print(solve(example))

with open('inputs/day11', 'r') as f:
    s = f.read()
    print(solve(s))
