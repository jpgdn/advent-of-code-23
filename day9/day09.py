def part12(fn,reverse=False):
    """
    Part 1: reverse=False
    Part 2: reverse=True
    """
    histories = []
    with open(fn, 'r') as file:
        for line in file:
            histories.append([int(i) for i in line.split()])
    sum = 0
    for h in histories:
        if reverse: h = h[::-1]
        # Compute the difference seuqences into an array (list of lists)
        arr = []
        while not all(x==0 for x in h):
            arr.append(h)
            h_next = []
            for i in range(0,len(h)-1):
                h_next.append(h[i+1]-h[i])
            h = h_next

        # Starting from the bottom, extrapolate the last value of each row
        for level in range(len(arr)-2,-1,-1):
            arr[level].append(arr[level][-1] + arr[level+1][-1])

        sum += arr[0][-1]
    return sum