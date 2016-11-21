from case_generator import generate_boards
from cdfs_box import cdfs as cdfs_box
from cdfs_rows import cdfs as cdfs_rows
from game import Game
import time


def simple_check():
    boards = generate_boards(int(1e2), 15)
    cdfs = cdfs_rows
    for size, l, b in boards:
        print(b)
        print(l)
        for i in l[0]:
            if len(i) == 0:
                i.append(0)
        for i in l[1]:
            if len(i) == 0:
                i.append(0)
        sol = cdfs(size, l[0], l[1])
        g = Game(b)
        print('\n-------Solution--------\n{}\n----------------\n'.format(sol))


def check_with_time(count=int(1e2), size=15):
    boards = generate_boards(count, size)
    idx = 0
    with open('test_cases/run', 'r') as f:
        run = int(f.read())
    with open('test_cases/run', 'w') as f:
        f.write(str(run + 1))

    for size, l, b in boards:
        density = calc_density(l[0], size)
        with open('test_cases/{}_{}_case'.format(run, idx), 'w') as f:
            f.write('{}\n{}\n{}\n{}'.format(size, l[0], l[1], density))
        for i in l[0]:
            if len(i) == 0:
                i.append(0)
        for i in l[1]:
            if len(i) == 0:
                i.append(0)
        t1 = time.time()
        sol1 = cdfs_box(size, l[0], l[1])
        tt = time.time() - t1
        t2 = time.time()
        sol2 = cdfs_rows(size, l[0], l[1])
        tt2 = time.time() - t2

        with open('test_cases/{}_{}_result'.format(run, idx), 'w') as f:
            f.write('{}\n{}'.format(str(tt), str(tt2)))

        if sol1 is None or sol2 is None:
            print('ERROR - solution not found')

        print('Case {}:\nDensity {}\nFijando casillas {}\nFijando filas {}\n'.format(idx, density, tt, tt2))
        idx += 1


def calc_density(restrictions, width):
    return sum([sum(x) for x in restrictions]) / (width * width) * 100


if __name__ == '__main__':
    check_with_time()
