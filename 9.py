import fileinput
from functools import cache


def heighmap():
    return [list(map(int, row.strip())) for row in fileinput.input()]


def mm(i, xs):
    return min(max(i, 0), len(xs) - 1)


def lowpoints(heighmap):
    points = []
    for i, row in enumerate(heighmap):
        for j, x in enumerate(row):
            if all(
                x < heighmap[i1][j1]
                for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]
                if (i1 := mm(i + di, heighmap), j1 := mm(j + dj, row)) != (i, j)
            ):
                points.append((i, j))
    return points


def solve1(heighmap):
    points = lowpoints(heighmap)
    print(sum(heighmap[x][y] + 1 for x, y in points))


def print_heighmap(heighmap, lowest, basins):
    nc = '\033[0m'
    pc = f"\033[0;35m{{}}{nc}".format
    bc = f"\033[0;36m{{}}{nc}".format
    m = [[str(x) for x in xs] for xs in heighmap]
    for i, j in lowest:
        m[i][j] = pc(m[i][j])
    for basin in basins:
        for i, j in basin:
            m[i][j] = bc(m[i][j])
    print('\n'.join(''.join(xs) for xs in m))


def find_basin(heighmap, i, j):
    x = heighmap[i][j]
    result = {(i, j)}
    for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        i1, j1 = mm(i + di, heighmap), mm(j + dj, heighmap[i])
        x1 = heighmap[i1][j1]
        if (i, j) != (i1, j1) and x1 != 9 and x1 - x >= 1:
            result |= find_basin(heighmap, i1, j1)
    return result


def solve2(heighmap):
    lowest = lowpoints(heighmap)
    basins = [find_basin(heighmap, i, j) for i, j in lowest]
    #print_heighmap(heighmap, lowest, basins)

    result = 1
    for size in sorted(map(len, basins), key=lambda x: -x)[:3]:
        result *= size
    print(result)

data = heighmap()
solve1(data)
solve2(data)

