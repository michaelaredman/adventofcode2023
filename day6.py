example = """Time:      7  15   30
Distance:  9  40  200"""

P1 = """Time:        58     99     64     69
Distance:   478   2232   1019   1071"""


def calculate_ways(S: str):
    ts = [int(x) for x in S.splitlines()[0].split()[1:]]
    recs = [int(x) for x in S.splitlines()[1].split()[1:]]
    result = 1
    for (t, rec) in zip(ts, recs):
        count = 0
        for t_p in range(1, t):
            if (t - t_p) * t_p > rec:
                count += 1
        result *= count

    print(result)


calculate_ways(example)
calculate_ways(P1)

# for pt2, just binary search


def kerning(S: str):
    time = int(''.join(S.splitlines()[0].split()[1:]))
    rec = int(''.join(S.splitlines()[1].split()[1:]))
    count = 0
    for t_p in range(1, time):
        if (time - t_p) * t_p > rec:
            count += 1
    return count


print(kerning(P1))
# 39594072
