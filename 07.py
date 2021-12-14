import fileinput
import statistics


def crab_positions():
    return list(map(int, next(fileinput.input()).split(',')))


def find_alignment(positions):
    mid = int(statistics.median(positions))
    return sum(abs(x - mid) for x in positions)


def find_alignment2(positions):
    # the best position must be near the arithmetic mean
    avg = round(sum(positions) / len(positions))
    progression_sum = lambda n: (1 + n) * n // 2
    return min(
        sum(progression_sum(abs(x - y)) for x in positions)
        for y in (avg - 1, avg, avg + 1)
    )

data = crab_positions()
print(find_alignment(data))
print(find_alignment2(data))

