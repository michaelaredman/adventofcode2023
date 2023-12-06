example = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
"""


def str_to_schematic(string: str) -> list[list]:
    return [[char for char in line] for line in string.splitlines()]


e_schematic = str_to_schematic(example)


def valid(i: int, j: int, nr: int, nc: int):
    return 0 <= i < nr and 0 <= j < nc


def find_adj(arr: list[list[str]]) -> list[list[bool]]:
    row, col = len(arr), len(arr[0])
    adj = [[False for _ in range(col)] for x in range(row)]
    dirs = [(0, 0), (-1, 0), (1, 0), (0, 1), (0, -1),
            (-1, -1), (1, 1), (-1, 1), (1, -1)]
    for i in range(row):
        for j in range(col):
            if (not arr[i][j].isdigit() and arr[i][j] != '.'):
                for dir in dirs:
                    x = i + dir[0]
                    y = j + dir[1]
                    if valid(x, y, row, col):
                        adj[x][y] = True
    return adj


find_adj(e_schematic)


def find_partnumbers(schematic: list[list[str]]) -> list[int]:
    partnumbers = []
    row, col = len(schematic), len(schematic[0])
    adj = find_adj(schematic)
    for i in range(row):
        include = False
        num = ""
        for j in range(col):
            if schematic[i][j].isdigit():
                num += schematic[i][j]
                if adj[i][j]:
                    include = True
            else:
                if num and include:
                    partnumbers.append(int(num))
                num = ""
                include = False
        if num and include:
            partnumbers.append(int(num))
    return partnumbers


# print(find_partnumbers(e_schematic))
# print(sum(find_partnumbers(e_schematic)))


with open('inputs/day3', 'r') as f:
    s = f.read()
    sch = str_to_schematic(s)
    pns = find_partnumbers(sch)
    print(pns)
    # adj = find_adj(sch)
    # for i in range(len(sch)):
    #     for j in range(len(sch[0])):
    #         if (adj[i][j]):
    #             print('\x1b[6;30;42m' + sch[i][j] + '\x1b[0m', end="")
    #         else:
    #             print(sch[i][j], end="")
    #     print()

    print(sum(pns))


def flood_fill(schematic: list[list[str]], i: int, j: int) -> dict[tuple[int, int], int]:
    left, right = j, j
    while (left - 1 >= 0 and schematic[i][left - 1].isdigit()):
        left -= 1
    while (right + 1 < len(schematic[0]) and schematic[i][right + 1].isdigit()):
        right += 1
    num = ""
    for digit in range(left, right+1):
        num += schematic[i][digit]
    return {(i, right): int(num)}


def find_gears(schematic: list[list[str]]) -> list[int]:
    gears = []
    nr, nc = len(schematic), len(schematic[0])
    dirs = [(0, 0), (-1, 0), (1, 0), (0, 1), (0, -1),
            (-1, -1), (1, 1), (-1, 1), (1, -1)]
    for i in range(nr):
        for j in range(nc):
            if (schematic[i][j] == '*'):
                d = dict()
                for dir in dirs:
                    x = i + dir[0]
                    y = j + dir[1]
                    if valid(x, y, nr, nc) and schematic[x][y].isdigit():
                        d.update(flood_fill(schematic, x, y))
                if (len(d) == 2):
                    nums = list(d.values())
                    gears.append(nums[0] * nums[1])
    return gears


print(find_gears(e_schematic))

with open('inputs/day3', 'r') as f:
    s = f.read()
    sch = str_to_schematic(s)
    gears = find_gears(sch)
    print(sum(gears))
