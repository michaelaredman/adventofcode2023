from enum import Enum
from functools import cmp_to_key


class HandType(Enum):
    FiveOfKind = 7
    FourOfKind = 6
    FullHouse = 5
    ThreeOfKind = 4
    TwoPair = 3
    OnePair = 2
    HighCard = 1


def hand_type(hand: str) -> HandType:
    card_count = {c: 0 for c in ['A', 'K', 'Q', 'J', 'T', '9', '8',
                                 '7', '6', '5', '4', '3', '2']}
    for card in hand:
        card_count[card] += 1
    card_count = sorted(card_count.items(), key=lambda x: -x[1])
    card, count = card_count[0]
    if count == 5:
        return HandType.FiveOfKind
    elif count == 4:
        return HandType.FourOfKind
    elif count == 3:
        card, count = card_count[1]
        if count == 2:
            return HandType.FullHouse
        else:
            return HandType.ThreeOfKind
    elif count == 2:
        card, count = card_count[1]
        if count == 2:
            return HandType.TwoPair
        else:
            return HandType.OnePair
    else:
        return HandType.HighCard


card_rank = {'A': 14, 'K': 13, 'Q': 12, 'J': 11, 'T': 10, '9': 9, '8': 8,
             '7': 7, '6': 6, '5': 5, '4': 4, '3': 3, '2': 2}


def compare_hands(hand1: str, hand2: str) -> int:
    # -1 when hand1 <= hand2, 1 when hand1 > hand2
    ht1, ht2 = hand_type(hand1), hand_type(hand2)
    if ht1 == ht2:
        for card1, card2 in zip(hand1, hand2):
            if card_rank[card1] != card_rank[card2]:
                return 1 if card_rank[card1] > card_rank[card2] else -1
    else:
        return 1 if ht1.value > ht2.value else -1
    return -1


example = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""


def total_winnings(s: str) -> int:
    hands_bids = [(hand.split()[0], int(hand.split()[1]))
                  for hand in s.splitlines()]

    hands, bids = zip(
        *sorted(hands_bids, key=lambda hb: cmp_to_key(compare_hands)(hb[0])))

    total = 0
    for i, bid in enumerate(bids):
        total += (i + 1) * bid
    return total


print(total_winnings(example))

with open('inputs/day7', 'r') as f:
    s = f.read()
    print(total_winnings(s))
