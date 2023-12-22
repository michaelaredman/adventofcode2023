from collections import deque


def find_S(grid: list[list[str]]) -> tuple[int, int]:
    n_row, n_col = len(grid), len(grid[0])
    for r in range(n_row):
        for c in range(n_col):
            if grid[r][c] == 'S':
                return (r, c)
    assert False


def bfs(grid: list[list[str]]) -> int:
    n_row, n_col = len(grid), len(grid[0])
    print(f"{n_row=}")
    print(f"{n_col=}")
    n_steps = 64
    Q = deque()
    S = find_S(grid)
    Q.appendleft((S, 0))
    dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    visited = [[False for _ in range(n_col)] for _ in range(n_row)]
    visited[S[0]][S[1]] = True
    count = 0
    while Q:
        p, steps = Q.pop()
        if steps % 2 == 0:
            count += 1
        for d in dirs:
            p_new = (p[0] + d[0], p[1] + d[1])
            if not (0 <= p_new[0] < n_row and 0 <= p_new[1] < n_col):
                continue
            if not visited[p_new[0]][p_new[1]] and steps+1 <= n_steps and grid[p_new[0]][p_new[1]] in ['.', 'S']:
                Q.appendleft((p_new, steps+1))
                visited[p_new[0]][p_new[1]] = True
    return count


example = """...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
..........."""

# g = [[c for c in line] for line in example.splitlines()]
# print(bfs(g))

with open('inputs/day21', 'r') as f:
    s = f.read()
    grid = [[c for c in line] for line in s.splitlines()]
    print(bfs(grid))
