import re
import sys
from math import lcm

example = """RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)"""

example2 = """LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)"""


def repeat_string_gen(s: str) -> str:
    while True:
        for c in s:
            yield c


def find_path_length(input: str) -> int:
    directions, adj_str = input.split('\n\n')

    pattern = re.compile(r'(\w+) = \((\w+), (\w+)\)')
    adj = dict()
    for node_dest in adj_str.splitlines():
        matches = pattern.search(node_dest)
        adj[matches.group(1)] = [matches.group(2), matches.group(3)]
        if matches.group(1)[2] == 'A':
            print(matches.group(1))

    for n in ['DRA', 'AAA', 'CMA', 'MNA', 'NJA', 'RVA']:
        cycle_length(n, adj, directions)
        print('='*30)
    # length = 0
    # node = 'AAA'
    # for c in repeat_string_gen(directions):
    #     node = adj[node][0 if c == 'L' else 1]
    #     length += 1
    #     if node == 'ZZZ':
    #         break
    # return length


# offset = num steps to get to z ender
# (steps - offset_i) % cycle_length_i == x_(i,j) for all i for some j
# where x_(i, 0) == 0 for all i
# chinese remainder theorem over combinations of x_(i,j)?

def cycle_length(node, adj: dict[str, list[str, str]], directions) -> int:
    i = 0
    valid = dict()
    CL = dict()
    for c in repeat_string_gen(directions):
        node = adj[node][0 if c == 'L' else 1]
        i += 1
        if node[2] == 'Z':
            if (node not in valid):
                valid[node] = i
            elif (node not in CL):
                CL[node] = i - valid[node]
            else:
                print(valid)
                print(CL)
                return (valid, CL)


# loljk the problem statement is garbage
nums = [20777, 18673, 13939, 17621, 19199, 12361]
print(f"{lcm(*nums)}")

# print(find_path_length(example2))
with open('inputs/day8', 'r') as f:
    s = f.read()
    print(find_path_length(s))
