
def proc_line(seq,pattern):
    result_cache = dict()

    def _find_pos(n,pat_pos):
        """Compute a list of compatible positions for a sequence of length n starting at pat_pos in pattern"""
        pos = []
        if pat_pos+n > len(pattern):
            return pos
        for i in range(pat_pos,len(pattern)-n+1):
            sub = pattern[i:i+n]
            if i+n==len(pattern):
                cnext = '.'
            else:
                cnext = pattern[i+n]
            if all(c != '.' for c in sub) and cnext in ('?','.'):
                pos += [i]
            if pattern[i] == '#':   # Cannot leave unused # chars behind
                break
        return pos
    
    def _count_compat(seq_pos,pat_pos):
        """Count the number of compatible postions for the remaining sequences"""
        if (seq_pos,pat_pos) in result_cache:
            return result_cache[(seq_pos,pat_pos)]
        res = 0

        n = seq[seq_pos]
        pos = _find_pos(n,pat_pos)
        if seq_pos == len(seq)-1:   # We have processed all sequences
            for p in pos:
                if '#' not in pattern[p+n:]:
                    res += 1    # OK, we have used up all the # characters
        else:
            for p in pos:
                res += _count_compat(seq_pos+1,p+n+1)
        result_cache[(seq_pos,pat_pos)] = res
        return res

    return _count_compat(0,0)

def p12(fn,part=1):
    res = 0
    with open(fn, 'r') as file:
        for line in file:
            line = line.strip()
            pattern, s_seq = line.split(' ')
            seq = tuple(map(int,s_seq.split(',')))
            if part==2:
                pattern = '?'.join(5*[pattern])
                seq = 5 * seq
            res += proc_line(seq,pattern)
    return res

if __name__ == "__main__":
    fn = 'aoc23-12-input.txt'
    for part in (1,2):
        print(f'Part {part}: {p12(fn,part)}')
    # print(f'Part 2: {p12(fn,True)}')