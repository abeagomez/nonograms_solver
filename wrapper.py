#!/usr/bin/ech python
import sys
import json
from dfs import dfs
from cdfs_rows import cdfs as rcdfs
from cdfs_box import cdfs as bcdfs
from fixer import fdfs
from pdfs import pdfs
from ls import ls, lsmr
from sa import sa

methods = {
    # 'dfs': (dfs, 'Simple dfs', 30),
    'rcdfs': (rcdfs, 'Dfs con restricciones fijando filas completas.', 120),
    'bcdfs': (bcdfs, 'Dfs con restricciones fijando casilla por casilla', 120),
    'pdfs': (pdfs, 'Dfs con restricciones + invariantes fijando por casillas', 120),
    'fdfs': (fdfs, 'Dfs con restricciones + invariantes fijando por filas', 120),
    # 'ls': (ls, 'Local search', 5),
    # 'mrls': (lsmr, 'Local search with multiple restarts', 5),
    # 'sa': (sa, 'Recocido simulado', 5)
}

if __name__ == '__main__':
    if len(sys.argv) > 2:
        method = methods[sys.argv[1]][0]
        game_file = sys.argv[2]
        with open(game_file) as f:
            game = json.load(f)
        result = method(len(game[0]), game[0], game[1])
        print(result is not None)
        if result is not None:
            exit(0)
        exit(-1)
