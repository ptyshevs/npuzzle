import argparse
from State import State
from PriorityQueue import PriorityQueue
from parser import parse
from heuristics import *
import sys

def generate_solution(side):
    sol = State([[0 for _ in range(side)] for _ in range(side)])
    step = side - 1
    dir = 'r'
    c = 1
    cp = [0, 0]
    cnt = 0
    first_time = True
    while step != 0:
        for i in range(step):
            sol[cp[0], cp[1]] = c
            c += 1

            if dir == 'r':
                cp[1] += 1
            elif dir == 'd':
                cp[0] += 1
            elif dir == 'l':
                cp[1] -= 1
            elif dir == 'u':
                cp[0] -= 1


        if (first_time and cnt == 3):
            first_time = False
            step -= 1
            cnt = 0
        elif cnt == 2:
            step -= 1
            cnt = 0

        cnt += 1

        if dir == 'r':
            dir = 'd'
        elif dir == 'd':
            dir = 'l'
        elif dir == 'l':
            dir = 'u'
        else:
            dir = 'r'
    sol._find_empty()
    return sol

def cnt_inversions(puzzle):
    n_inv = 0
    flat = []
    for r in puzzle.values:
        for c in r:
            flat.append(c)
    n = len(flat)
    for i in range(n):
        is_inv = False
        if flat[i] == 0:
            continue
        for j in range(i):
            if flat[j] == 0:
                continue
            if flat[j] > flat[i]:
                # print(f"inverse: {flat[j]} > {flat[i]}")
                n_inv += 1
    return n_inv

def is_solvable(puzzle, solution):
    n_inv = cnt_inversions(puzzle)
    sol_inv = cnt_inversions(solution)
    print("n_inversions:", n_inv, 'sol_inversions:', sol_inv)
    n_inv = n_inv % 2
    sol_inv = sol_inv % 2

    n = puzzle.w
    
    if n % 2 == 1:
        return n_inv == sol_inv
    else:
        y, x = puzzle.empty_loc
        if (puzzle.h - y - 1) % 2 == 0:
            return n_inv != sol_inv
        else:
            return n_inv == sol_inv

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', '-f', help='path to puzzle file', default=None, required=False)
    parser.add_argument('--heuristic', default='misplaced', help="Heuristic to use [misplaced|euclidean|manhattan|djkstra]")
    parser.add_argument('--verbose', '-v', default=False, action='store_true', help='Verbose mode')
    parser.add_argument('--iter', '-i', default='heuristic', help="Number of iterations [heuristic|inf|int]")

    args = parser.parse_args()
    try:
        if args.file is None:
            f = sys.stdin
        else:
            f = open(args.file)
    except FileNotFoundError:
        print("No such file. Nice try, though.")
        exit(1)
    
    try:
        puzzle_size, puzzle = parse(f)
        puzzle = State(puzzle)
        solution = generate_solution(puzzle_size)
    except ValueError as e:
        print(e)
        exit(1)

    solvable = is_solvable(puzzle, solution)    

    if args.verbose:
        print("PUZZLE PARSED:", puzzle, sep='\n')
        print("Solution:", solution, sep='\n')
        print("Solvable:", solvable)

    if not solvable:
        exit(0)
    heur_map = {'misplaced': h_misplaced, 'manhattan': h_manhattan,
                'euclidean': h_euclidean, 'djkstra': h_djkstra}
    
    h = heur_map.get(args.heuristic, None)
    if h is None:
        print("Heuristic is not recognized")
        exit(1)

    opened = PriorityQueue()
    puzzle.heur = h(puzzle, solution)
    opened.add(puzzle.heur, puzzle)
    closed = set()
    search_path = []
    success = False

    if args.iter == 'heuristic':
        max_iter = puzzle_size * 10000
        verbose_step = int(max_iter // 20)

    elif args.iter == 'inf':
        max_iter = float('inf')
        verbose_step = 1000
    else:
        try:
            max_iter = int(args.iter)
            verbose_step = int(max_iter // 20)

        except ValueError:
            print("Bad value of iter argument (must be convertable to integer)")
            exit(1)
    iter = 0
    while True:
        if len(opened) == 0 or success or iter >= max_iter:
            print("BREAK", len(opened))
            break
        e = opened.pop()
        closed.add(e)
        if e == solution:
            print("SOLVED")
            success = True
        else:
            for dir in ['u', 'r', 'd', 'l']:
                if e.dir_from == 'u' and dir == 'd':
                    continue
                elif e.dir_from == 'r' and dir == 'l':
                    continue
                elif e.dir_from == 'd' and dir == 'u':
                    continue
                elif e.dir_from == 'l' and dir == 'r':
                    continue
                try:
                    r = e.swap(dir)
                    r.heur = h(r, solution)
                    r.came_from = e
                    r.dir_from = dir
                    r.g = e.g + 1 # + Cost
                except ValueError:
                    continue
                
                if r not in opened and r not in closed:
                    opened.add(r.g * .4 + r.heur, r)
                # else:
                #     if r.g * .4 + r.heur > (e.g + 1) * .4 + r.heur:
                #         if r in closed:
                #             print("HERE")
                #             closed.remove(r)
                #             opened.add(r.heur, r)
        iter += 1
        if args.verbose and iter % verbose_step == 0:
            print(f"[{iter}]: n_opened = {len(opened)} | n_closed = {len(closed)} | cur_depth: {e.g} | top-5 heur: {', '.join(str(round(_, 1)) for _ in opened.k[:5])}")

    state_path = []
    if success:
        while e.came_from is not None:
            state_path.append(e)
            e = e.came_from
        state_path.append(puzzle)
        state_path = list(reversed(state_path))
    print(f"Success: {success} | n_iter: {iter} | n_opened: {len(opened)} | n_closed: {len(closed)} | path length: {len(state_path)}")
    if success:
        print('->'.join((c.dir_from for c in state_path[1:])))
        print("Final state:\n===========\n", state_path[-1], sep='')
        # for s in state_path:
        #     print(s, sep='')
        #     print("===============")
