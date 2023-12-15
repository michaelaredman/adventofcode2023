from copy import deepcopy
import sys

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


def roll_south(grid: list[list[str]]) -> list[list[str]]:
    n_row, n_col = len(grid), len(grid[0])
    for c in range(n_col):
        spaces = 0
        insert_p = None
        for r in reversed(range(n_row)):
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
                        insert_p -= 1
                    else:
                        spaces, insert_p = 0, None
                case _:
                    assert False
    return grid


def roll_west(grid: list[list[str]]) -> list[list[str]]:
    n_row, n_col = len(grid), len(grid[0])
    for r in range(n_row):
        spaces = 0
        insert_p = None
        for c in range(n_col):
            match grid[r][c]:
                case '#':
                    spaces, insert_p = 0, None
                case '.':
                    spaces += 1
                    if insert_p == None:
                        insert_p = c
                case 'O':
                    if spaces:
                        grid[r][c], grid[r][insert_p] = '.', 'O'
                        insert_p += 1
                    else:
                        spaces, insert_p = 0, None
                case _:
                    assert False
    return grid


def roll_east(grid: list[list[str]]) -> list[list[str]]:
    n_row, n_col = len(grid), len(grid[0])
    for r in range(n_row):
        spaces = 0
        insert_p = None
        for c in reversed(range(n_col)):
            match grid[r][c]:
                case '#':
                    spaces, insert_p = 0, None
                case '.':
                    spaces += 1
                    if insert_p == None:
                        insert_p = c
                case 'O':
                    if spaces:
                        grid[r][c], grid[r][insert_p] = '.', 'O'
                        insert_p -= 1
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


def cycle(grid: list[list[str]]) -> list[list[str]]:
    grid = roll_north(grid)
    grid = roll_west(grid)
    grid = roll_south(grid)
    return roll_east(grid)


def g2h(grid: list[list[str]]):
    return tuple(tuple(row) for row in grid)

#  3 4 6 7 1 2 3 [1] 2 3 1 2 3
# 13 total, n = 12


def cycles(grid: list[list[str]], n: int, track: bool = False) -> list[list[str]]:
    if track:
        seen = {}
        seen.setdefault(None)
        seen[g2h(grid)] = 0
    for i in range(1, n+1):
        grid = cycle(grid)
        if track:
            h = g2h(grid)
            if (seen.get(h)):
                c_length = i - seen[h]
                rem = (n - i) % c_length
                return cycles(grid, rem)
            else:
                seen[h] = i
    return grid


n_cycles = 1000000000

with open('inputs/day14', 'r') as f:
    s = f.read()
    g = [[char for char in line] for line in s.splitlines()]
    final = cycles(g, n_cycles, True)
    print(f"{total_load(final)=}")
