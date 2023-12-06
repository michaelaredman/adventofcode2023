from dataclasses import dataclass
import re


@dataclass
class IntervalPair:
    s_left: int
    s_right: int
    d_left: int
    d_right: int


IntervalList = list[IntervalPair]


def collapse(il1: IntervalList, il2: IntervalList) -> IntervalList:
    il1.sort(key=lambda x: x.d_right)
    il2.sort(key=lambda x: x.s_right)
    i, j = 0, 0
    while i < len(il1) and j < len(il2):
        if il1[i].d_right < il2[j].s_right:
            left_split = IntervalPair(il2[j].s_left, il1[i].d_right,
                                      il2[j].d_left, il2[j].d_left + il1[i].d_right - il2[j].s_left)
            right_split = IntervalPair(il1[i].d_right + 1, il2[j].s_right,
                                       il2[j].d_right - (il2[j].s_right - (il1[i].d_right + 1)), il2[j].d_right)
            il2 = il2[:j] + [left_split, right_split] + il2[(j+1):]
        elif il1[i].d_right > il2[j].s_right:
            left_split = IntervalPair(il1[i].s_left, il1[i].s_left + il2[j].s_right - il1[i].d_left,
                                      il1[i].d_left, il2[j].s_right)
            right_split = IntervalPair(il1[i].s_right - (il1[i].d_right - (il2[j].s_right + 1)), il1[i].s_right,
                                       il2[j].s_right + 1, il1[i].d_right)
            il1 = il1[:i] + [left_split, right_split] + il1[(i+1):]
        else:
            i += 1
            j += 1
    merged = il1
    for i in range(len(il1)):
        merged[i].d_left = il2[i].d_left
        merged[i].d_right = il2[i].d_right
    return merged


def find_intervals(s2r_string: str) -> list[list[int]]:
    intervals = []
    for interval in re.findall(r'\n(.+)', s2r_string):
        intervals.append([int(x) for x in interval.split()])
    return intervals


def interval_overlap_min(left1, right1, left2, right2):
    # (left1, right1) is the location interval
    if right2 < left1 or left2 > right1:
        return None
    elif left2 <= left1:
        return left1
    else:
        return left2


def raw_to_IntervalList(raw_intervals):
    result = []
    for interval in raw_intervals:
        result.append(IntervalPair(interval[1], interval[1] + interval[2] - 1,
                                   interval[0], interval[0] + interval[2] - 1))
    result.sort(key=lambda x: x.s_left)
    if result[0].s_left != 0:
        result.append(IntervalPair(0, result[0].s_left - 1,
                                   0, result[0].s_left - 1))
    result.sort(key=lambda x: x.s_left)
    result.append(IntervalPair(result[-1].s_right + 1, 100000000000,
                               result[-1].s_right + 1, 100000000000))
    result.sort(key=lambda x: x.s_left)
    extra = []
    for i in range(len(result) - 1):
        if result[i].s_right != (result[i + 1].s_left - 1):
            extra.append(IntervalPair(result[i].s_right + 1, result[i + 1].s_left - 1,
                                      result[i].s_right + 1, result[i + 1].s_left - 1))
    result += extra
    result.sort(key=lambda x: x.s_left)
    return IntervalList(result)


with open('inputs/day5', 'r') as f:
    string_input = f.read()
    split_s = re.split(r'\n\n', string_input)
    seed_list = [int(x) for x in re.search(
        r': (.+)', split_s[0]).group(1).split()]
    seed_intervals = []
    i = 0
    while i < len(seed_list):
        start = seed_list[i]
        i += 1
        length = seed_list[i]
        seed_intervals.append([start, start + length - 1])
        i += 1
    a = raw_to_IntervalList(find_intervals(split_s[1]))
    b = raw_to_IntervalList(find_intervals(split_s[2]))
    c = raw_to_IntervalList(find_intervals(split_s[3]))
    d = raw_to_IntervalList(find_intervals(split_s[4]))
    e = raw_to_IntervalList(find_intervals(split_s[5]))
    f = raw_to_IntervalList(find_intervals(split_s[6]))
    g = raw_to_IntervalList(find_intervals(split_s[7]))
    X = collapse(a, b)
    X = collapse(X, c)
    X = collapse(X, d)
    X = collapse(X, e)
    X = collapse(X, f)
    X = collapse(X, g)
    X.sort(key=lambda x: x.d_left)
    for x in X:
        candidates = []
        for interval in seed_intervals:
            if leftmost := interval_overlap_min(x.s_left, x.s_right, interval[0], interval[1]):
                candidates.append(x.d_left + leftmost - x.s_left)
        if candidates:
            print(min(candidates))
            break
