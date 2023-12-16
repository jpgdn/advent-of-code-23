from pprint import pprint

def _neighbor_map(lines,c_start,s_node):
    """Create a dictionarity of allowed neighbors for each symbol"""
    # Neighbors for each pipe symbol
    nb = { '-': [(-1,0),(1,0)],
           '|': [(0,-1),(0,1)],
           '7': [(-1,0),(0,1)],
           'J': [(0,-1),(-1,0)],
           'L': [(0,-1),(1,0)],
           'F': [(0,1),(1,0)] }

    # Add S's neighbors by checking for neighbors that point back to S
    max_i, max_j = len(lines[0]), len(lines)
    s_nb = []
    for d in [(1,0),(0,1),(-1,0),(0,-1)]:
        i = s_node[0]+d[0]
        j = s_node[1]+d[1]
        if i in range(max_i) and j in range(max_j):
            c = lines[j][i]
            if c in nb:
                for nd in nb[c]:
                    if nd[0] == -d[0] and nd[1]== -d[1]:   # OK, points back to me
                        s_nb += [d]
    nb[c_start] = s_nb
    return nb

def _make_graph(lines,c_start,verbose=False):
    """Create a list of nodes starting with c_start and ending one step before returning to c_start"""
    # Find starting node
    for j, line in enumerate(lines):
        if c_start in line:
            s_node = (line.index(c_start),j)
            break

    nb = _neighbor_map(lines,c_start,s_node)

    graph = [{'pos': s_node, 'c': c_start}]
    prev_node = None
    cur_node = s_node
    c = c_start
    found_s = False
    while not found_s:
        # Find a neighbor
        for d in nb[c]:
            i = cur_node[0]+d[0]
            j = cur_node[1]+d[1]
            if (i,j) != prev_node:
                # Assuming each node has exactly two neighbors, this is the one that doesn't go back to where we came from
                c = lines[j][i]
                if c==c_start:
                    found_s = True
                else:
                    graph.append({'pos': (i,j), 'c': c})
                break   # Stop checking my neighbors
        prev_node = cur_node
        cur_node = (i,j)

    return graph

def part1(fn,verbose=False):
    """Solve part 1"""
    with open(fn, 'r') as file:
        lines = [s.strip() for s in file.readlines()]
    graph = _make_graph(lines,'S',verbose)
    return len(graph) // 2

def part2(fn,verbose=False):
    """Solve part 2"""
    with open(fn, 'r') as file:
        lines = [s.strip() for s in file.readlines()]
    graph = _make_graph(lines,'S',verbose)

    # Create a picture with the graph characters and '.' as background
    pic = [['.' for _ in range(len(lines[0]))] for _ in range(len(lines))]
    for node in graph:
        i, j = node['pos']
        pic[j][i] = node['c']

    # Define the (up,down) vertical crossings for each symbol
    # It would probably work just to count the 'up' crossings
    vcross = {'-': (0,0), '|': (1,1), '7': (1,0), 'J': (0,1), 'L': (0,1), 'F': (1,0)}
    # For S we need check its neighbors
    s_up, s_down = 0, 0
    s_j = graph[0]['pos'][1]
    for n_j in [graph[1]['pos'][1],graph[-1]['pos']][1]:
        if n_j > s_j:
            s_up += 1
        elif n_j < s_j:
            s_down += 1
    vcross['S'] = (s_up, s_down)

    # Traverse the picture line by line and count vertical crossings
    res = 0
    for j, line in enumerate(pic):
        inside = False
        up, down = 0, 0
        for i, c in enumerate(line):
            if c in vcross:
                up += vcross[c][0]
                down += vcross[c][1]
            else:
                if up % 2 == 1 and down % 2 == 1:
                    inside = not inside # We passed a border
                if inside:
                    pic[j][i] = '*'
                    res += 1
                up, down = 0, 0

    if verbose:
        for line in pic:
            s = ''.join(line)
            print(s)
    return res