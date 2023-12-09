import math
import re

def _race_dist(charge_time,race_time):
    return (charge_time*(race_time-charge_time))

def _proc_races(races):
    prod = 1
    for tmax, dbest in races:
        # Compute minimum charge time
        tc1 = math.ceil(tmax/2 - math.sqrt(tmax*tmax/4 - dbest))
        if (_race_dist(tc1,tmax)==dbest): tc1 += 1
        # Compute maximum charge time
        tc2 = math.floor(tmax/2 + math.sqrt(tmax*tmax/4 - dbest))
        if (_race_dist(tc2,tmax)==dbest): tc2 -= 1

        # Number of winning charge times
        count = int(tc2-tc1)+1
        prod *= count
    return prod

def part1(fn):
    with open(fn, 'r') as file:
        lines = file.readlines()
    times = re.findall(r'(\d+)',lines[0])
    times = [int(x) for x in times]
    distances = re.findall(r'(\d+)',lines[1])
    distances = [int(x) for x in distances]
    races = list(zip(times,distances))
    return _proc_races(races)

def part2(fn):
    with open(fn, 'r') as file:
        lines = file.readlines()
    times = re.findall(r'(\d+)',lines[0])
    t = ''.join(times)
    distances = re.findall(r'(\d+)',lines[1])
    d = ''.join(distances)
    races = [(int(t),int(d))]
    return _proc_races(races)