
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
