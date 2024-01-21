def print_grid(grid):
    for line in grid:
        print(''.join(line))

def score_grid(grid):
    score = 0
    size = len(grid)
    for i in range(size):
        row = grid[i]
        for cell in row:
            if cell == 'O':
                score += size - i
    return score

def tilt_grid(grid):
    pos = [0] * len(grid[0])    # First free position for each column
    for i, row in enumerate(grid):
        for j, c in enumerate(row):
            if c == 'O':
                # Move O to the first free position (could be its present position)
                grid[i][j] = '.'
                grid[pos[j]][j] = 'O'
                pos[j] += 1
            elif c == '#':
                pos[j] = i+1
    return grid

def part1(fn):
    with open(fn, 'r') as file:
        grid = [list(line.strip()) for line in file.readlines()]

    tilt_grid(grid)
    res = score_grid(grid)
    return res

def part2(fn,spins=20):
    with open(fn, 'r') as file:
        grid = [list(line.strip()) for line in file.readlines()]

    grid_cache = dict()
    res_list = []
    for i in range(spins):
        for d in range(4):
            grid = tilt_grid(grid)
            grid = [list(row)[::-1] for row in zip(*grid)]  # Rotate 90 degrees
        g = tuple(tuple(row) for row in grid)   # Hash key
        if g in grid_cache:
            # We found a cycle
            cycle = i - grid_cache[g]
            start = grid_cache[g]
            print(f'{start = }, {cycle = }')
            ix = start + (spins - start - 1) % cycle
            break
        grid_cache[g] = i
        res_list.append(score_grid(grid))
    else:   # We didn't find a cycle
        ix = spins-1
    
    print(f'{ix = }')
    return res_list[ix]

if __name__ == "__main__":
    fn = 'aoc23-14-input.txt'
    print(f'Part 1: {part1(fn)}')
    c = 1000000000
    print(f'Part 2: {part2(fn,c)}')