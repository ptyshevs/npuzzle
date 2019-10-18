
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
    return puzzle_size, puzzle
