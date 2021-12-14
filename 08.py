import fileinput
from collections import defaultdict


def entries():
    result = []
    for entry in fileinput.input():
        signal, digits = entry.strip().split(' | ')
        result.append((signal.split(), digits.split()))
    return result


def count_unique_digits(entries):
    unique_segment_count = {2, 3, 4, 7}
    return sum(len(digit) in unique_segment_count for _, digits in entries for digit in digits)


def decode(signal):
    xs = defaultdict(list)
    for d in signal:
        xs[len(d)].append(frozenset(d))
    top = xs[3][0] - xs[2][0]
    mid = next(mid for six in xs[6] if len(mid := ((xs[4][0] ^ xs[2][0]) - six)) == 1)
    l1 = xs[4][0] ^ xs[2][0] ^ mid
    bot = next(bot for six in xs[6] if len(bot := ((l1 | mid | top | xs[2][0]) ^ six)) == 1)
    r2 = next(r2 for five in xs[5] if len(r2 := ((l1 | mid | top | bot) ^ five)) == 1)
    r1 = xs[2][0] ^ r2
    l2 = (top | mid | bot | l1 | r1 | r2) ^ xs[7][0]
    return {
        top | bot | l1  | l2 | r1 | r2: 0,
        r1  | r2: 1,
        top | mid | bot | r1 | l2: 2,
        top | mid | bot | r1 | r2: 3,
        mid | l1  | r1  | r2: 4,
        top | mid | bot | l1 | r2: 5,
        top | mid | bot | l1 | l2 | r2: 6,
        top | r1  | r2: 7,
        top | mid | bot | l1 | r1 | l2 | r2: 8,
        top | mid | bot | l1 | r1 | r2: 9,
    }


def sum_digits(entries):
    result = 0
    for signal, digits in entries:
        term = decode(signal)
        for i, digit in enumerate(reversed(digits)):
            result += term[frozenset(digit)] * 10**i
    return result

data = entries()
print(count_unique_digits(data))
print(sum_digits(data))

