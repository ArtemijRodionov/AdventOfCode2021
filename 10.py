import fileinput
from collections import defaultdict

def lines():
    return [line.strip() for line in fileinput.input()]

def check(line):
    xs = {'(': ')', '[': ']', '<': '>', '{': '}'}
    prev = [line[0]]
    if prev[0] not in xs:
        return prev
    for x in line[1:]:
        if x in xs:
            prev.append(x)
        elif not prev or xs[prev.pop()] != x:
            return x
    return list(map(xs.get, reversed(prev)))


def solve1(lines):
    cost = {')': 3, ']': 57, '}': 1197, '>': 25137}
    print(sum([
        cost[failed] for l in lines
        if isinstance(failed := check(l), str)
    ]))


def solve2(lines):
    cost = {')': 1, ']': 2, '}': 3, '>': 4}
    result = []
    for l in lines:
        ok = check(l)
        if not isinstance(ok, list):
            continue
        score = 0
        for x in ok:
            score = score * 5 + cost[x]
        result.append(score)
    result.sort()
    print(result[len(result) // 2])

data = lines()
solve1(data)
solve2(data)

