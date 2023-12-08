def _proc_input(fn):
    """Process the input file and return the seed numbers and a range map (a list of lists of ranges)"""
    maps = []
    seeds = []
    with open(fn, 'r') as file:
        for line in file:
            line = line.strip()
            if not seeds:
                _, s = line.split(': ')
                seeds = [int(num) for num in s.split()]
                # print(f'Seeds: {seeds}')
            elif ':' in line:
                # print(f'New map: ', line)
                maps.append([])
            elif line:
                row = [int(num) for num in line.split()]
                ranges = [range(row[0], row[0] + row[2]), range(row[1], row[1] + row[2])]
                maps[-1].append(ranges)
    
    # Maybe it is a good idea to sort the ranges by the start position of the "from" range
    for i, m in enumerate(maps):
        maps[i] = sorted(maps[i], key=lambda f: f[1][0])

    return seeds, maps

def part1(fn,verbose=False):
    seeds, maps = _proc_input(fn)
    
    for ranges in maps:
        next_seeds = []
        for seed in seeds:
            for tr, fr in ranges:
                if seed in fr:
                    # Found in "from" range: Map to "to" range
                    offset = tr.start - fr.start
                    next_seeds.append(seed + offset)
                    break
            else:
                # Checked all ranges - no overlap found (we did not hit "break")
                next_seeds.append(seed)
        # The output from this map will be the input to the next map
        seeds = next_seeds
    
    if verbose: print(seeds)
    return min(seeds)


def part2(fn,verbose=False):
    s, maps = _proc_input(fn)
    src = []
    # Convert seed numbers to a list of seed ranges
    for i, s in enumerate(s):
        if i % 2 == 0:
            start = s
        else:
            src.append(range(start,start+s))
    
    for i, ranges in enumerate(maps):
        dst = []
        for r in src:
            if verbose: print(f'Level {i}, checking seeds: {r}')
            # Check each source range for overlap with the "from" ranges in the map
            for tr, fr in ranges:
                if r.stop <= fr.start or fr.stop <= r.start:
                    # No overlap - skip to next range
                    continue
                # Internal range: Overlap between seed and source
                ir = range(max(r.start, fr.start), min(r.stop, fr.stop))
                # Left range: From seed start to ir start (False if seed start >= ir start)
                lr = range(r.start, ir.start)
                # Right range: From ir stop to seed stop (False if seed start >= ir start)
                rr = range(ir.stop, r.stop)
                # Add lr and/or rr to the current list of seed ranges to be checked
                if lr:  # If lr is a valid range
                    src.append(lr)
                if rr:  # If rr is a valid range
                    src.append(rr)
                # Map the internal range (which we know is valid) to the next layer
                offset = tr.start - fr.start
                dst.append(range(ir.start + offset, ir.stop + offset))
                break
            else:
                # Checked all ranges - no overlap found (we did not hit "break")
                if verbose: print('Nothing found')
                dst.append(r)

            if verbose: print(f'Updated source: {src}')
        src = dst

    return min(x.start for x in src)