import fileinput
import heapq

import numpy as np

f = fileinput.input()
grid = np.array([list(map(int, l.strip())) for l in f])
dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def neighbors(xs, point):
    x, y = point
    m, n = len(xs[0]), len(xs)
    return [
        (xt, yt) for xd, yd in dirs
        if 0 <= (xt := x + xd) < m
        and 0 <= (yt := y + yd) < n
    ]


def find(xs):
    start = 0, 0
    goal = len(xs[0]) - 1, len(xs) - 1
    path = [(0, start)]
    costs = {start: 0}
    
    while path:
        _, prev = heapq.heappop(path)
        for cur in neighbors(xs, prev):
            x, y = cur
            cost = costs[prev] + xs[y][x]
            if cost < costs.get(cur, float('inf')):
                costs[cur] = cost
                heapq.heappush(path, (cost, cur))

    return costs.get(goal, -1)


def inc(xs, i):
    new_xs = xs + i
    new_xs[new_xs >= 10] += 1
    new_xs %= 10
    return new_xs


def expand_grid(xs, size):
    row = np.concatenate([inc(xs, i) for i in range(size)]).T
    return np.concatenate([inc(row, i) for i in range(size)]).T

print(find(grid))
print(find(expand_grid(grid, 5)))

