import re

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
        if matches.group(1)[2] == 'A':
            print(matches.group(1))
        adj[matches.group(1)] = [matches.group(2), matches.group(3)]

    length = 0
    node = 'AAA'
    for c in repeat_string_gen(directions):
        node = adj[node][0 if c == 'L' else 1]
        length += 1
        if node == 'ZZZ':
            break
    return length


print(find_path_length(example2))

with open('inputs/day8', 'r') as f:
    s = f.read()
    print(find_path_length(s))
