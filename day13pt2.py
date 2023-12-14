
def check_vertical(grid: list[list[str]], after_col: int) -> bool:
    n_row, n_col = len(grid), len(grid[0])
    left, right = after_col, after_col + 1
    smudge = 0
    while True:
        if left < 0 or right >= n_col:
            break
        for r in range(n_row):
            if grid[r][left] != grid[r][right]:
                if smudge:
                    return False
                smudge += 1
        left -= 1
        right += 1
    return bool(smudge)


def check_horizontal(grid: list[list[str]], after_row: int) -> bool:
    n_row, n_col = len(grid), len(grid[0])
    top, bottom = after_row, after_row + 1
    smudge = 0
    while True:
        if top < 0 or bottom >= n_row:
            break
        for c in range(n_col):
            if grid[top][c] != grid[bottom][c]:
                if smudge:
                    return False
                smudge += 1
        top -= 1
        bottom += 1
    return bool(smudge)


def find_reflection(grid: list[list[str]]) -> tuple[int, int]:
    n_row, n_col = len(grid), len(grid[0])
    for r in range(n_row - 1):
        if check_horizontal(grid, r):
            return (r + 1, 0)
    for c in range(n_col - 1):
        if check_vertical(grid, c):
            return (0, c + 1)
    assert False


example = """#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#"""


def summarize(s: str):
    raw_grids = s.split('\n\n')
    totals = (0, 0)
    for raw_grid in raw_grids:
        grid = [c for c in raw_grid.splitlines()]
        a = find_reflection(grid)
        print(a)
        totals = (totals[0] + a[0], totals[1] + a[1])
    return totals[0] * 100 + totals[1]


print(summarize(example))

with open('inputs/day13', 'r') as f:
    s = f.read()
    print(summarize(s))
