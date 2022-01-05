import fileinput
from collections import Counter
from functools import cache

f = fileinput.input()
template = next(f).strip()
pairs = dict(
    xs for pair in f
    if len(xs := pair.strip().split(' -> ')) == 2
)


@cache
def unfold_pair(pair, level):
    if level <= 0:
        return Counter(pair[0])
    l, r = pair
    t = pairs[pair]
    return unfold_pair(l + t, level - 1) + unfold_pair(t + r, level - 1)


def unfold(template, level):
    result = Counter(template[-1])
    for i in range(1, len(template)):
        result += unfold_pair(template[i-1] + template[i], level)
    return result


def result(xs):
    common = xs.most_common()
    return common[0][1] - common[-1][1]

print(result(unfold(template, 10)))
print(result(unfold(template, 40)))

