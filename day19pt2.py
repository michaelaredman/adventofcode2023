from copy import deepcopy
from collections import defaultdict
from typing import Type
import re
import sys


class PartRange:

    def __init__(self, x: tuple = (1, 4000), m: tuple = (1, 4000), a: tuple = (1, 4000), s: tuple = (1, 4000)):
        self.ratings = {'x': x, 'm': m, 'a': a, 's': s}
        self.empty = False

    def split(self, cat, symbol, number):
        r = self.ratings[cat]
        redirect_split, continue_split = deepcopy(self), deepcopy(self)
        if symbol == '<':
            redirect_split.ratings[cat] = (r[0], number-1)
            if r[0] > number-1:
                redirect_split.empty = True
            continue_split.ratings[cat] = (number, r[1])
            if r[1] < number:
                continue_split.empty = True
        else:
            redirect_split.ratings[cat] = (number+1, r[1])
            if r[1] < number+1:
                redirect_split.empty = True
            continue_split.ratings[cat] = (r[0], number)
            if number < r[0]:
                continue_split.empty = True
        return (redirect_split, continue_split)

    def __repr__(self):
        return "PartRange: " + self.ratings.__repr__()

    def ways(self):
        ks = self.ratings.values()
        total = 1
        for k in ks:
            total *= (1 + (k[1] - k[0]))
        return total


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

    def __call__(self, pr: PartRange):
        out = defaultdict(list)
        continue_split = pr
        for rule in self.ruleset:
            s, dest = rule
            if s != 'True':
                cat, symbol, number = re.findall(
                    r"(\w)(>|<)(\d+)", s)[0]
                number = int(number)
                redirect_split, continue_split = continue_split.split(
                    cat, symbol, number)
                if not redirect_split.empty:
                    out[dest] += [redirect_split]
            else:
                if not continue_split.empty:
                    out[dest] += [continue_split]
                else:
                    break
        return out

    def __repr__(self) -> str:
        return "Workflow: " + self.ruleset.__repr__()


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

    for ruleset in rules_str.splitlines():
        name, ruleset_str = re.findall(r"(\w+){(.+)}", ruleset)[0]
        system[name] = Workflow(ruleset_str)

    return system, parts


def find_ranges(system):
    range_list = defaultdict(list)
    range_list['in'] = [PartRange()]
    A, R = [], []
    while range_list:
        for r in range_list:
            if r == 'A':
                A += range_list[r]
                range_list.pop(r)
                break
            elif r == 'R':
                R += range_list[r]
                range_list.pop(r)
                break
            else:
                wf = system[r]
                out = defaultdict(list)
                for t in range_list[r]:
                    additional = wf(t)
                    for k in additional:
                        range_list[k] += additional[k]
                range_list.pop(r)
                break
    return A, R


def count_ways(input):
    system, _ = parse(input)
    A = find_ranges(system)[0]
    count = 0
    for a in A:
        count += a.ways()
    return count


print("Example ways:", count_ways(example))

with open('inputs/day19', 'r') as f:
    s = f.read()
    print('Part 2 ways:', count_ways(s))
