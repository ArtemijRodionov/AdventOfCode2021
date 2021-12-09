import fileinput
from collections import defaultdict

def fish_days():
    return list(map(int, next(fileinput.input()).strip().split(',')))

def solve(days, simulation_days):
    idx = {d: 1 for d in days}
    for _ in range(simulation_days):
        newborn = 0
        new_idx = defaultdict(int) 
        for days, count in idx.items():
            days_left = days - 1
            if days_left < 0:
                days_left = 6
                newborn += count
            new_idx[days_left] += count
        if newborn:
            new_idx[8] += newborn
        idx = new_idx
    print(sum(idx.values()))

current_days = fish_days()
solve(current_days, 80)
solve(current_days, 256)
