def line_to_input(line: str):
    row, groups = line.split()
    row = [c for c in row]
    groups = [int(x) for x in groups.split(',')]
    return row, groups


def count_ways(line: str, groups: list[int]):
    n_springs, n_groups = len(line), len(groups)
    dp = [[[0 for _ in range(groups[group] + 1)]
           for group in range(n_groups)]
          for spring in range(n_springs)]
    match line[0]:
        case '.': dp[0][0][0] = 1
        case '#': dp[0][0][1] = 1
        case '?': dp[0][0][0], dp[0][0][1] = 1, 1
        case _: assert False

    for c in range(1, n_springs):
        match line[c]:
            case '.':
                for group in range(n_groups):
                    dp[c][group][0] = dp[c-1][group][0]
                    if group > 0:
                        dp[c][group][0] += dp[c-1][group-1][-1]
                if dp[c-1][-1][-1] > 0:
                    dp[c][-1][-1] = max(dp[c][-1][-1], dp[c-1][-1][-1])
            case '#':
                for group in range(n_groups):
                    for H in range(1, groups[group] + 1):
                        dp[c][group][H] = dp[c-1][group][H-1]
            case '?':
                for group in range(n_groups):
                    dp[c][group][0] = dp[c-1][group][0]
                    if group > 0:
                        dp[c][group][0] += dp[c-1][group-1][-1]
                    for H in range(1, groups[group] + 1):
                        dp[c][group][H] = dp[c-1][group][H - 1]
                if dp[c-1][-1][-1] > 0:
                    dp[c][-1][-1] = dp[c][-1][-1] + dp[c-1][-1][-1]
            case _:
                assert False
    return dp[-1][-1][-1]


def total_ways(s: str) -> int:
    total = 0
    for line in s.splitlines():
        total += count_ways(*line_to_input(line))
    return total


def five_times(line, groups):
    new_line = line.copy()
    new_groups = groups.copy()
    for i in range(1, 5):
        new_line += ['?'] + line
        new_groups += groups
    return new_line, new_groups


def total_unfolded(s: str) -> int:
    total = 0
    for line in s.splitlines():
        total += count_ways(*(five_times(*line_to_input(line))))
    return total


with open('inputs/day12', 'r') as f:
    s = f.read()
    print(total_ways(s))
    print(f"{total_unfolded(s)=}")
