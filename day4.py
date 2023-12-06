import re


def find_numbers(line: str) -> tuple[list[int], list[int]]:
    matches = re.search(r": (.+) \| (.+)", line)
    winning, numbers = matches.group(1).split(), matches.group(2).split()
    winning, numbers = [int(x) for x in winning], [int(x) for x in numbers]
    return (winning, numbers)


def card_points(line: str) -> int:
    winning, numbers = find_numbers(line)
    count = sum(bool(w) for w in numbers if w in set(winning))
    if count:
        return 1 << (count - 1)
    else:
        return 0


example = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""


for line in example.splitlines():
    print(card_points(line))

with open('inputs/day4', 'r') as f:
    total_points = 0
    for line in f:
        total_points += card_points(line)
    print(total_points)


def total_cards(cards_str: str) -> int:
    cards = cards_str.splitlines()
    N = len(cards)
    card_count = [1 for _ in range(N)]
    for i in range(N):
        winning, numbers = find_numbers(cards[i])
        w_count = sum(bool(w) for w in numbers if w in set(winning))
        for k in range(1, w_count + 1):
            card_count[i + k] += card_count[i]
    return sum(card_count)


print(total_cards(example))

with open('inputs/day4', 'r') as f:
    card_str = f.read()
    print(total_cards(card_str))
