from copy import deepcopy

example = """O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#...."""


def roll_north(grid: list[list[str]]) -> list[list[str]]:
    n_row, n_col = len(grid), len(grid[0])
    for c in range(n_col):
        spaces = 0
        insert_p = None
        for r in range(n_row):
            match grid[r][c]:
                case '#':
                    spaces, insert_p = 0, None
                case '.':
                    spaces += 1
                    if insert_p == None:
                        insert_p = r
                case 'O':
                    if spaces:
                        grid[r][c], grid[insert_p][c] = '.', 'O'
                        insert_p += 1
                    else:
                        spaces, insert_p = 0, None
                case _:
                    assert False
    return grid


def find_tilted(s: str) -> list[list[str]]:
    grid = [[char for char in line] for line in s.splitlines()]
    return roll_north(grid)


def total_load(grid: list[list[str]]) -> int:
    n_row, n_col = len(grid), len(grid[0])
    load, LN = 0, 1
    for r in reversed(range(n_row)):
        for c in range(n_col):
            if grid[r][c] == 'O':
                load += LN
        LN += 1
    return load


print(f"{total_load(find_tilted(example))=}")

with open('inputs/day14', 'r') as f:
    s = f.read()
    print(f"{total_load(find_tilted(s))=}")
