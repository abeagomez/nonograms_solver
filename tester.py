from case_generator import generate_boards
from cdfs_box import cdfs
from game import Game

boards = generate_boards(10, 10)

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
    print('\n---------------\n{}\n----------------\n'.format(sol))
