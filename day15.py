import re
part1 = True
part2 = True


def hash(s: str) -> int:
    current_value = 0
    for char in s:
        current_value += ord(char)
        current_value *= 17
        current_value %= 256
    return current_value


if part1:
    with open('inputs/day15', 'r') as f:
        string = f.read()
        string.replace('\n', '')
        values = string.split(sep=',')
        total = 0
        for value in values:
            total += hash(value)
        print(f"{total=}")


def solve(s: str) -> list[dict[str, int]]:
    instructions = s.split(',')
    lenses = [dict() for _ in range(256)]
    for ins in instructions:
        label, sign, lens = re.search(r'(.+)([-=])(.*)', ins).groups()
        box = hash(label)
        if sign == '-':
            if label in lenses[box]:
                lenses[box].pop(label)
        else:
            lenses[box][label] = int(lens)
    return lenses


def focusing_power(boxes: list[dict[str, int]]) -> int:
    total = 0
    for bn, box in enumerate(boxes):
        for slot, lens in enumerate(box):
            total += (bn + 1) * (slot + 1) * (box[lens])
    return total


if part2:
    with open('inputs/day15', 'r') as f:
        string = f.read()
        string.replace('\n', '')
        print(f"{focusing_power(solve(string))=}")
