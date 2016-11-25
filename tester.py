from case_generator import generate_boards
from cdfs_box import cdfs as cdfs_box
from cdfs_rows import cdfs as cdfs_rows
from pdfs import pdfs
from game import Game
import subprocess
import numpy as np
import time
import json


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


def check_with_time(count=int(1e2)):
    idx = 0
    with open('test_cases/run', 'r') as f:
        run = int(f.read())
    with open('test_cases/run', 'w') as f:
        f.write(str(run + 1))
    for s in range(5, 21):
        for p in np.arange(0.1, 1., 0.1):
            boards = generate_boards(count, s, p)
            for size, l, b in boards:
                density = calc_density(l[0], size)
                print('Case {}:\nDensity {}'.format(idx, density))
                with open('test_cases/{}_{}_case'.format(run, idx), 'w') as f:
                    f.write('{}\n{}\n{}\n{}\n{}'.format(size, l[0], l[1], density, str(b)))
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
                t3 = time.time()
                sol3 = pdfs(size, l[0], l[1])
                tt3 = time.time() - t3

                with open('test_cases/{}_{}_result'.format(run, idx), 'w') as f:
                    f.write('{}\n{}\n{}'.format(str(tt), str(tt2), str(tt3)))

                if sol1 is None or sol2 is None or sol3 is None:
                    print('ERROR - solution not found')

                print('Fijando casillas {}\nFijando filas {}\nProbabilista {}\n'.format(tt, tt2, tt3))
                idx += 1


def calc_density(restrictions, width):
    return sum([sum(x) for x in restrictions]) / (width * width) * 100


def generate_cases(count=int(1e3)):
    idx = 0
    for s in range(5, 21):
        cases = []
        for p in np.arange(0.1, 1., 0.1):
            print(p)
            boards = generate_boards(count, s, p)
            for size, l, b in boards:
                density = calc_density(l[0], size)
                a = {'list': l, 'density': density}
                cases.append(a)
            print('generated all cases')
        with open('test_cases/cases_{}.json'.format(idx), 'w') as f:
            json.dump(cases, f)
        idx += 1


def check_with_timeout(method, timeout):
    res = subprocess.run(['time', 'gtimeout', str(timeout), 'python', 'wrapper.py', method, 'test_case'],
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    if res.returncode != 0:
        print(res.stderr)
        return timeout, False
    time = float(res.stderr.strip().split()[0])
    result = eval(res.stdout.strip()) if res.returncode == 0 else False
    return time, result


if __name__ == '__main__':
    from wrapper import methods

    for i in range(16):
        print(i)
        for key in methods.keys():
            print(key)
            timeout = methods[key][2]
            with open('test_cases/cases_{}.json'.format(i)) as f:
                test_cases = json.load(f)
            print(len(test_cases))
            all_fail = True
            times = []
            results = []
            for c, case in enumerate(test_cases):
                with open('test_case', 'w') as f:
                    json.dump(case['list'], f)
                t, result = check_with_timeout(key, timeout)
                print(c, t, result)
                times.append(t)
                results.append(result)
                all_fail &= not result
            with open('results/{}_{}'.format(key, i), 'w') as f:
                json.dump([x for x in zip(times, results)], f)
            if all_fail: break
