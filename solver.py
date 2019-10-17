import argparse
from State import State
from PriorityQueue import PriorityQueue

def line_to_tokens(line):
    tokens = []
    for t in line.split(" "):
        if not t:
            continue
        if t.startswith("#"):
            break
        if '#' in t:
            tokens.append(t[:t.index("#")])
            break
        elif t == '\n':
            continue
        tokens.append(t)
    return tokens

def parse(f):
    puzzle_size = None
    puzzle = []
    puzzle_nmbrs = set()
    for line in f:
        tokens = line_to_tokens(line)
        if len(tokens) == 0:
            continue
        if puzzle_size is None:
            if len(tokens) != 1:
                raise ValueError(f"Bad size tokens: {tokens}")
                exit(1)
            try:
                puzzle_size = int(tokens[0])
            except ValueError:
                raise ValueError(f"Bad token: {tokens[0]}")
                exit(1)
        else:
            if len(tokens) != puzzle_size:
                raise ValueError(f"Bad tokens len: {tokens}")
                exit(1)
            try:
                puzzle_line = [int(tk) for tk in tokens]
                puzzle_nmbrs.update(puzzle_line)
                if len(puzzle_line) != puzzle_size:
                    raise ValueError("Bad puzzle formatting")
                puzzle.append(puzzle_line)
            except ValueError:
                raise ValueError(f"Bad tokens: {tokens}")
                exit(1)
    if len(puzzle) != puzzle_size:
        raise ValueError("Puzzle is too short")
    if len(puzzle_nmbrs) != puzzle_size ** 2:
        raise ValueError("Not all numbers are unique")
    # Handle case when numbers are not from 0 to N - 1
    if sorted(list(puzzle_nmbrs)) != list(range(puzzle_size ** 2)):  
        raise ValueError(f"Numbers should go from 0 to {puzzle_size ** 2}")
    return puzzle_size, State(puzzle)

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

def h_djkstra(node, solution=None):
    """ Djkstra algorithm is a special-case of A* when h(n) = 0 """
    return 0

def h_misplaced(node, sol):
    res = [sum([c1 != c2 for c1, c2 in zip(r1, r2)]) for r1, r2 in zip(node.values, sol.values)]
    return sum(res)

def h_euclidean(node, sol):
    """ RMSE between numbers """
    h, w = node.shape
    heur = 0
    for i in range(h):
        for j in range(w):
            c1 = node[i, j]
            c2 = sol[i, j]
            if c1 != c2:
                found = False
                for k in range(h):
                    for m in range(w):
                        c = sol[k, m]
                        if c1 == c:
                            heur += (k - i) ** 2 + (m - j) ** 2
                            found = True
                        if found:
                            break
                    if found:
                        break
                assert found
    return heur

def h_manhattan(node, sol):
    h, w = node.shape
    heur = 0
    for i in range(h):
        for j in range(w):
            c1 = node[i, j]
            c2 = sol[i, j]
            if c1 != c2:
                found = False
                for k in range(h):
                    for m in range(w):
                        c = sol[k, m]
                        if c1 == c:
                            heur += abs(k - i) + abs(m - j)
                            found = True
                        if found:
                            break
                    if found:
                        break
                assert found
    return heur



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('puzzle', help='path to puzzle file')
    parser.add_argument('--heuristic', default='misplaced', help="Heuristic to use [misplaced|euclidean|manhattan|djkstra]")
    parser.add_argument('--verbose', '-v', default=False, action='store_true', help='Verbose mode')

    args = parser.parse_args()
    try:
        f = open(args.puzzle)
    except FileNotFoundError:
        print("No such file. Nice try, though.")
        exit(1)
    
    try:
        puzzle_size, puzzle = parse(f)
    except ValueError as e:
        print(e)
        exit(1)
    

    if args.verbose:
        print("PUZZLE PARSED:", puzzle, sep='\n')

    solution = generate_solution(puzzle_size)
    if args.verbose:
        print("Solution:", solution, sep='\n')

    if args.heuristic == 'misplaced':
        h = h_misplaced
    elif args.heuristic == 'manhattan':
        h = h_manhattan
    elif args.heuristic == 'euclidean':
        h = h_euclidean
    elif args.heuristic == 'djkstra':
        h = h_djkstra
    else:
        print("Heuristic is not recognized")
        exit(1)

    # g = some_g
    opened = PriorityQueue()

    puzzle.heur = h(puzzle, solution)
    opened.add(puzzle.heur, puzzle)
    closed = set()
    search_path = []
    success = False
    max_iter = 100000
    verbose_step = int(max_iter // 20)
    iter = 0
    while True:
        if len(opened) == 0 or success or iter >= max_iter:
            print("BREAK", len(opened))
            break
        e = opened.pop()
        # print("went to\n", e.dir_from, '\n')
        # search_path.append(e)
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
                else:
                    if r.g * .5 + r.heur > (e.g + 1) * .7 + r.heur:
                        if r in closed:
                            print("HERE")
                            closed.remove(r)
                            opened.add(r.heur, r)
        # print("Opened:")
        # print("\n========\n".join(('|'.join((str(_), str(_.dir_from), str(h))) for _, h in zip(opened.v, opened.k))))
        iter += 1
        if args.verbose and iter % verbose_step == 0:
            print(f"[{iter}]: n_opened = {len(opened)} | n_closed = {len(closed)} | cur_depth: {e.g} | top-10 heur: {opened.k[:10]}")
    print("Success:", success, "n_iter:", iter, 'opened size:', len(opened))
    if success:
        state_path = []
        while e.came_from is not None:
            state_path.append(e)
            e = e.came_from
        state_path.append(puzzle)
        state_path = list(reversed(state_path))
        print("path length:", len(state_path))
        # if
        # print("\n========\n".join(('|'.join((str(_), str(_.dir_from), str(_.heur))) for _ in state_path)))
    # print("Opened")
    # print('\n-----\n'.join((str(_) for _ in opened)))
    # print("Closed:", closed)
    # print("Search path:\n", *(str(_) for _ in search_path), sep='\n========\n')