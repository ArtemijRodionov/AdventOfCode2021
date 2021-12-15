import fileinput
import sys
import time
import os

DEBUG = bool(os.environ.get('DEBUG', False))

dij = [(i, j) for i in range(-1, 2) for j in range(-1, 2)]


def energy():
    return [list(map(int, l.strip())) for l in fileinput.input()]


def in_bound(i, n):
    return i >= 0 and i < n

colors = {
    i: ';'.join(x.split(','))
    for i, x in enumerate(reversed(
        """
        171, 71, 188
        158, 63, 177
        145, 56, 166
        132, 48, 155
        119, 40, 144
        106, 33, 133
        93, 25, 122
        80, 17, 111
        67, 10, 100
        54, 2, 89
        """.strip().replace(' ', '').split()
    ))
}
color = lambda x: "\33[48;2;" + str(colors[x]) + "m" + str(x) + "\33[0m"

def print_grid(grid):
    if not DEBUG: 
        return
    time.sleep(0.02)
    os.system('clear')
    print('\n'.join(
        [''.join([color(x) for x in row])
        for row in grid]
    ))


def is_synchronizing(grid):
    return all(x == 0 for row in grid for x in row)
        

def flash(grid, flashed, to_flash, i, j):
    grid[i][j] += 1
    if grid[i][j] <= 9:
        return
    grid[i][j] = 0
    flashed.add((i, j))
    to_flash.append((i, j))

def step(grid):
    to_flash = []
    flashed = set()
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            flash(grid, flashed, to_flash, i, j)
            print_grid(grid)

    while to_flash:
       i, j = ij = to_flash.pop()
       for di, dj in dij:
           i1, j1 = ij1 = i + di, j + dj
           is_ok = in_bound(i1, len(grid)) and in_bound(j1, len(grid[i1]))
           if not is_ok or ij1 == ij or ij1 in flashed:
               continue
           flash(grid, flashed, to_flash, i1, j1)
           print_grid(grid)
    return len(flashed)


def solve(grid):
    xs = [[x for x in xs] for xs in grid]
    flash_count = 0
    for i in range(100):
        flash_count += step(xs)        
    print_grid(xs)
    print(flash_count)
    step_count = 0
    xs = [[x for x in xs] for xs in grid]
    while True:
        if is_synchronizing(xs):
            break
        step(xs)
        step_count += 1
    print_grid(xs)
    print(step_count)

data = energy()
solve(data)

