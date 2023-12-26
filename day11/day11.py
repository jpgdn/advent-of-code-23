from collections import defaultdict
def part12(fn,expansion=2):
    with open(fn, 'r') as file:
        grid = [s.strip() for s in file.readlines()]

    # Compute col and row sizes (either "expansion" or 1)
    i_size = defaultdict(lambda:expansion)
    j_size = defaultdict(lambda:expansion)
    for j, line in enumerate(grid):
        for i, c in enumerate(line):
            if c == '#': 
                i_size[i] = 1
                j_size[j] = 1

    # Compute expanded galaxy coordinates
    galaxies = []
    j_exp = 0
    for j, line in enumerate(grid):
        i_exp = 0
        for i, c in enumerate(line):
            if c == '#': 
                galaxies.append((i_exp,j_exp))
            i_exp += i_size[i]
        j_exp += j_size[j]

    # Sum up the distances
    res = 0
    for k, (i1,j1) in enumerate(galaxies):
        for (i2,j2) in galaxies[k+1:]:
            res += abs(i2-i1) + abs(j2-j1)
    return res