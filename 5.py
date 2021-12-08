import fileinput
from collections import defaultdict

def readlines():
    result = []
    cast = lambda xs: tuple(map(int, xs.strip().split(',')))
    for line in fileinput.input():
        from_, to = line.split('->')
        result.append((cast(from_), cast(to)))
    return result


def solve(lines):
    coords1 = defaultdict(int)
    coords2 = defaultdict(int)
    for ((x1, y1), (x2, y2)) in lines:
        if y1 == y2:
            for x in range(min(x1, x2), max(x1, x2) + 1):
                coords1[(x, y1)] += 1
                coords2[(x, y1)] += 1
        if x1 == x2:
            for y in range(min(y1, y2), max(y1, y2) + 1):
                coords1[(x1, y)] += 1
                coords2[(x1, y)] += 1
        if abs(x1 - x2) == abs(y1 - y2):
            from_to = zip(
                range(x1, x2 + 1) if x1 < x2 else reversed(range(x2, x1 + 1)),
                range(y1, y2 + 1) if y1 < y2 else reversed(range(y2, y1 + 1)),
            )
            for x, y in from_to:
                coords2[(x, y)] += 1

    print(sum(1 for count in coords1.values() if count > 1))
    print(sum(1 for count in coords2.values() if count > 1))

solve(readlines())

