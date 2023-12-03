input = """1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
"""


def calibration(input: str) -> int:
    total = 0
    for line in input.splitlines():
        left = 0
        right = len(line) - 1
        while (ord(line[left]) < 48 or ord(line[left]) > 57):
            left += 1
        while (ord(line[right]) < 48 or ord(line[right]) > 57):
            right -= 1
        total += int(line[left] + line[right])
    return total


print(calibration(input))

with open('inputs/day1', 'r') as f:
    x = f.read()
    print(calibration(x))


class TrieNode():
    def __init__(self):
        self.children = {}
        self.EOW = False
        self.val = None


class Trie():

    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str, val):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.EOW = True
        node.val = val

    def find(self, string: str, pos: int):
        if string[pos].isdigit():
            return int(string[pos])
        node = self.root
        for char in string[pos:]:
            if char in node.children:
                node = node.children[char]
                if node.EOW == True:
                    return node.val
            else:
                return False
        return False


elf_trie = Trie()
elf_trie.insert('zero', 0)
elf_trie.insert('one', 1)
elf_trie.insert('two', 2)
elf_trie.insert('three', 3)
elf_trie.insert('four', 4)
elf_trie.insert('five', 5)
elf_trie.insert('six', 6)
elf_trie.insert('seven', 7)
elf_trie.insert('eight', 8)
elf_trie.insert('nine', 9)


def complex_calibration(input: str):
    total = 0
    for line in input.splitlines():
        first = -1
        last = 0
        for i in range(len(line)):
            res = elf_trie.find(line, i)
            if res and first == -1:
                first = res
                last = res
            elif res:
                last = res
        total += int(str(first) + str(last))
    print(total)


test = """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen"""

complex_calibration(test)

with open('inputs/day1', 'r') as f:
    x = f.read()
    complex_calibration(x)
