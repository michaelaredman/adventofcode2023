import heapq
from heapq import heappop, heappush
from math import inf
from collections import defaultdict


def construct_graph(grid: list[list[int]]) -> dict[tuple[int, int, int],
                                                   dict[tuple[int, int, int], int]]:
    n_row, n_col = len(grid), len(grid[0])
    graph = defaultdict(dict)
    for r in range(n_row):
        for c in range(n_col):
            weight = 0
            Ds = range(1, 11)
            for v_d in Ds:
                if r + v_d >= n_row:
                    break
                weight += grid[r + v_d][c]
                if v_d >= 4:
                    graph[(r, c, 0)] |= {(r + v_d, c, 1): weight}
            weight = 0
            for v_d in Ds:
                if r - v_d < 0:
                    break
                weight += grid[r - v_d][c]
                if v_d >= 4:
                    graph[(r, c, 0)] |= {(r - v_d, c, 1): weight}
            weight = 0
            for v_h in Ds:
                if c + v_h >= n_col:
                    break
                weight += grid[r][c + v_h]
                if v_h >= 4:
                    graph[(r, c, 1)] |= {(r, c + v_h, 0): weight}
            weight = 0
            for v_h in Ds:
                if c - v_h < 0:
                    break
                weight += grid[r][c - v_h]
                if v_h >= 4:
                    graph[(r, c, 1)] |= {(r, c - v_h, 0): weight}
    return graph


def dijkstras(grid: list[list[int]], graph):
    n_row, n_col = len(grid), len(grid[0])
    visited = [[[False, False] for _ in range(n_col)] for _ in range(n_row)]
    d = [[[inf, inf] for _ in range(n_col)] for _ in range(n_row)]
    pq = []
    heappush(pq, (grid[0][0], (0, 0, 0)))
    heappush(pq, (grid[0][0], (0, 0, 1)))
    d[0][0][0], d[0][0][1] = 0, 0
    while pq:
        my_d, node = heappop(pq)
        visited[node[0]][node[1]][node[2]] = True
        for dest, edge_weight in graph[node].items():
            if visited[dest[0]][dest[1]][dest[2]]:
                continue
            updated_distance = d[node[0]][node[1]][node[2]] + edge_weight
            if updated_distance < d[dest[0]][dest[1]][dest[2]]:
                d[dest[0]][dest[1]][dest[2]] = updated_distance
                heappush(pq, (updated_distance, dest))
    return d


def min_heat(d):
    return min(d[-1][-1][0], d[-1][-1][1])


example = """2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533"""

# g = [[int(x) for x in line] for line in example.splitlines()]

# print(min_heat(dijkstras(g, construct_graph(g))))

with open('inputs/day17', 'r') as f:
    s = f.read()
    grid = [[int(x) for x in line] for line in s.splitlines()]
    graph = construct_graph(grid)
    result = min_heat(dijkstras(grid, graph))
    print(result)
