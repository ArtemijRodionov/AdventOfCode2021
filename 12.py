import fileinput
from collections import defaultdict


def cave_map():
    res = defaultdict(set)
    for x in fileinput.input():
        v1, v2 = x.strip().split('-')
        res[v1].add(v2)
        res[v2].add(v1)
    return res


def traverse(g, check, path, visited):
    if check(path, visited):
        return 

    if path[-1] == 'end':
        yield path[:]
        return

    for x in g[path[-1]]:
        if x == 'start':
            continue

        visited[x] += 1
        path.append(x)
        yield from traverse(g, check, path, visited)
        path.pop()
        visited[x] -= 1


def second(paths, visited):
    two = 0
    for k, v in visited.items():
        if not k.islower():
            continue

        if v == 2:
            two += 1
        if v > 2 or two > 1:
            return True


def first(path, visited):
    return path[-1].islower() and visited[path[-1]] > 1


def solve(m):
    print(len(list(traverse(m, first, ['start'], defaultdict(int)))))
    print(len(list(traverse(m, second, ['start'], defaultdict(int)))))

data = cave_map()
solve(data)
