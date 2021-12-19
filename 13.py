import fileinput

dots = []
insts = []

src = fileinput.input()
for l in src:
    l = l.strip()
    if not l:
        break
    dots.append(tuple(map(int, l.split(','))))

for l in src:
    axy, v = l.strip().rsplit('=')
    insts.append((axy[-1], int(v)))


def fold(dots, inst):
    axis, val = inst
    swap = axis == 'y'
    dots = [(y, x) if swap else (x, y) for x, y in dots]

    for i in range(len(dots)):
        x, y = dots[i]
        if x < val:
            continue 
        new_x = 2 * val - x
        dots[i] = new_x, y

    return list(set((y, x) if swap else (x, y) for x, y in dots))


def print_paper(dots):
    n = max(dots, key=lambda x: x[0])[0] + 1
    m = max(dots, key=lambda x: x[1])[1] + 1
    dots = set(dots)
    for j in range(m):
        for i in range(n):
            c = '.'
            if (i, j) in dots:
                c = '\33[48;2;54;2;89m#\33[0m'
            print(c, end='')
        print(' ')

for inst in insts:
    dots = fold(dots, inst)
print_paper(dots)

