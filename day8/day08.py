import re
import math
from itertools import cycle

def _parse_input(fn):
    """Parse input file and return data structures"""
    with open(fn, 'r') as file:
        lines = [s.strip() for s in file.readlines()]
    directions = lines[0].replace('L','0').replace('R','1')
    labels = []
    next_labels = []
    for line in lines[2:]:
        m = re.findall(r'[A-Z]+',line)
        labels.append(m[0])
        next_labels.append((m[1],m[2]))
    return directions, labels, next_labels

def _count_steps(directions, labels, next_labels, start_node, end_node):
    """Compute the number of steps to get from start_node to end_node"""
    count = 0
    ix = labels.index(start_node)
    for c in cycle(directions):
        count += 1
        next_addr = next_labels[ix][int(c)]
        ix = labels.index(next_addr)
        if labels[ix].endswith(end_node):
            break
    return count

def part1(fn):
    """Part 1: Count the number of steps to get from AAA to ZZZ"""
    directions, labels, next_labels = _parse_input(fn)
    count = _count_steps(directions, labels, next_labels, 'AAA', 'ZZZ')
    return count

def part2(fn):
    """
    Part 2: Count the number of steps until all ghosts are at a node ending with Z
    Use the empirical observation that each ghost moves in cycles.
    Then the answer is the least common multiple of the steps for each ghost.
    """
    directions, labels, next_labels = _parse_input(fn)
    start_nodes = [s for s in labels if s[2]=='A']
    steps = []
    for start_node in start_nodes:
        steps.append(_count_steps(directions, labels, next_labels, start_node, 'Z'))
    return math.lcm(*steps)
