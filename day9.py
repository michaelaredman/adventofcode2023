
def find_diffs(seq: list[int]) -> (list[int], bool):
    all_zeros = True
    diffs = []
    for i in range(len(seq)-1):
        diff = seq[i+1]-seq[i]
        if diff != 0:
            all_zeros = False
        diffs.append(diff)
    return (diffs, all_zeros)


def predict_next(seq: list[int]) -> list[int]:
    diffs, all_zeros = find_diffs(seq)
    if all_zeros:
        return seq + [seq[-1]]
    else:
        return seq + [seq[-1] + predict_next(diffs)[-1]]


ex1 = [0, 3, 6, 9, 12, 15]
ex2 = [1, 3, 6, 10, 15, 21]
ex3 = [10, 13, 16, 21, 30, 45]

print(predict_next(ex1))
print(predict_next(ex2))
print(predict_next(ex3))

with open('inputs/day9', 'r') as f:
    sum_of_predicted = 0
    s = f.read()
    for line in s.splitlines():
        seq = [int(x) for x in line.split()]
        sum_of_predicted += predict_next(seq)[-1]
    print(sum_of_predicted)
