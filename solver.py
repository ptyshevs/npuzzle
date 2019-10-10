import argparse

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

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('puzzle', help='path to puzzle file')

    args = parser.parse_args()
    try:
        f = open(args.puzzle)
    except FileNotFoundError:
        print("No such file. Nice try, though.")
        exit(1)
    
    puzzle_size = None
    puzzle = []
    for line in f:
        tokens = line_to_tokens(line)
        if len(tokens) == 0:
            continue
        if puzzle_size is None:
            if len(tokens) != 1:
                print(f"Bad size tokens: {tokens}")
                exit(1)
            try:
                puzzle_size = int(tokens[0])
            except ValueError:
                print(f"Bad token: {tokens[0]}")
                exit(1)
        else:
            if len(tokens) != puzzle_size:
                print(f"Bad tokens len: {tokens}")
                exit(1)
            try:
                puzzle_line = [int(tk) for tk in tokens]
                puzzle.append(puzzle_line)
            except ValueError:
                print(f"Bad tokens: {tokens}")
                exit(1)
    if len(puzzle) != puzzle_size:
        print("Puzzle is too short")
        exit(1)
    print("PUZZLE PARSED:", puzzle)