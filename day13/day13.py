def part12(file_path,smudges):
    res = 0
    with open(file_path, 'r') as file:
        sections = file.read().split("\n\n")
        for s in sections:
            pattern = [line.strip() for line in s.splitlines()]
            res += 100*process_pattern(pattern,smudges) # Horizontal reflections
            pattern = list(map(''.join,zip(*pattern)))  # Transpose
            res += process_pattern(pattern,smudges)     # Vertical reflections
    return res

def process_pattern(p,smudges):
    rows = len(p)
    cols = len(p[0])
    res = 0
    for i in range(1,rows):
        diffsum = 0
        for j in range(0,min(i,rows-i)):
            diffsum += sum(1 for k in range(cols) if p[i-j-1][k] != p[i+j][k])  # Count non-matching characters
            if diffsum > smudges:
                break
        if diffsum==smudges:
            res = i
            break
    return res

if __name__ == "__main__":
    fn = 'aoc23-13-input.txt'
    print(f'Part 1: {part12(fn,0)}')
    print(f'Part 2: {part12(fn,1)}')