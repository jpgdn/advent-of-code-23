def _hand_type(hand):
    """Calculate the hand type value"""
    # Create histogram of values
    hist = [0] * 13
    for n in hand:
        hist[n] += 1
    hist.sort(reverse=True)
    highest_multiple = hist[0]
    hand_type = highest_multiple * 2
    # Check for full house or two pairs: Is there a second pair?
    if highest_multiple in [2,3] and hist[1]==2:
        hand_type += 1
    return hand_type

def _hand_type_jokers(hand):
    """Recursively substitute the jokers with every other card and find the highest hand type value"""
    if hand.count(0):
        # We have at least one joker
        test_hand = hand[:]
        ix = test_hand.index(0)
        hand_type = 0
        for i in range(1,13):
            test_hand[ix] = i
            hand_type = max(hand_type,_hand_type_jokers(test_hand))
    else:
        # No jokers - calculate and return the hand type
        hand_type = _hand_type(hand)
    return hand_type

def _aoc23_7_proc(fn,joker=False):
    """Process the input lines and calculate the total win"""
    with open(fn, 'r') as file:
        lines = [s.strip() for s in file.readlines()]
    if joker:   # J = Joker, value 0
        d = {'A':12, 'K':11, 'Q':10, 'J':0, 'T':9, '9':8, '8':7, '7':6, '6':5, '5':4, '4':3, '3':2, '2':1}
    else:
        d = {'A':12, 'K':11, 'Q':10, 'J':9, 'T':8, '9':7, '8':6, '7':5, '6':4, '5':3, '4':2, '3':1, '2':0}
    hands = []
    for line in lines:
        hand, bid = line.split()
        hand = [int(d[c]) for c in hand]
        bid = int(bid)
        if joker:
            hand_type = _hand_type_jokers(hand)
        else:
            hand_type = _hand_type(hand)
        hands.append((hand_type, hand, bid))
    hands = sorted(hands)

    return sum((rnk+1)*hand[2] for rnk, hand in enumerate(hands))


def part1(fn):
    return _aoc23_7_proc(fn,False)

def part2(fn):
    return _aoc23_7_proc(fn,True)