from dataclasses import dataclass, astuple
from collections import defaultdict
from typing import Type
import re


@dataclass
class Part:
    x: int
    m: int
    a: int
    s: int

    def __iter__(self):
        return iter(astuple(self))


class Workflow:

    def __init__(self, ruleset_str: str):
        self.ruleset = []
        rule_list = ruleset_str.split(',')
        for rule in rule_list:
            if ':' in rule:
                condition, destination = rule.split(':')
                self.ruleset.append((condition, destination))
            else:
                self.ruleset.append(("True", rule))

    def __call__(self, part: Part):
        x, m, a, s = part
        for rule in self.ruleset:
            condition, destination = rule
            if eval(condition):
                return destination
        assert False

    def __repr__(self) -> str:
        return self.ruleset.__repr__()


type System = defaultdict[str, Type[Workflow]]

example = """px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}"""


def parse(input: str):
    rules_str, parts_str = input.split('\n\n')
    parts = []
    system: System = {}

    for part in parts_str.splitlines():
        x, m, a, s = re.findall(r"{x=(\d+),m=(\d+),a=(\d+),s=(\d+)}", part)[0]
        parts.append(Part(int(x), int(m), int(a), int(s)))
    for ruleset in rules_str.splitlines():
        name, ruleset_str = re.findall(r"(\w+){(.+)}", ruleset)[0]
        system[name] = Workflow(ruleset_str)

    return system, parts


def solve(input: str):
    A = []
    R = []
    system, ps = parse(input)
    for p in ps:
        w = system['in']
        d = w(p)
        while True:
            if d == 'A':
                A.append(p)
                break
            elif d == 'R':
                R.append(p)
                break
            else:
                w = system[d]
                d = w(p)
    return A


Ae = solve(example)
c = 0
for ae in Ae:
    c += sum(ae)
print("Part 1 example:", c)

with open('inputs/day19', 'r') as f:
    s = f.read()
    A = solve(s)
    count = 0
    for a in A:
        count += sum(a)
    print("Part 1:", count)
