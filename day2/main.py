import sys

def convert(shape):
    if shape == 'a' or shape == 'x':
        return 1
    if shape == 'b' or shape == 'y':
        return 2
    if shape == 'c' or shape == 'z':
        return 3
    raise Exception('invalid shape: %s' % shape)

def calc_round_points(theirs, mine):
    # points for shape
    pnts = mine

    # draw
    if theirs == mine:
        pnts += 3
    else:
        # win?
        if (theirs == 1 and mine == 2)\
            or (theirs == 2 and mine == 3)\
            or (theirs == 3 and mine == 1):
            pnts += 6
    return pnts

def read_strategy_file(filename):
    pnts = 0
    with open(filename, 'r') as fp:
        for line in fp:
            line = line.strip().lower()
            toks = line.split()
            if len(toks) == 2:
                pnts += calc_round_points(convert(toks[0]), convert(toks[1]))
            else:
                raise Exception('invalid strategy line: \'%s\'' % line)
    return pnts

def calc_round_points_v2(theirs, outcome):
    mine = theirs # init
    if outcome == 1: # loose
        if theirs == 1:
            mine = 3
        elif theirs == 2:
            mine = 1
        elif theirs == 3:
            mine = 2
    elif outcome == 2: # draw
        mine = theirs
    elif outcome == 3: # win
        if theirs == 1:
            mine = 2
        elif theirs == 2:
            mine = 3
        elif theirs == 3:
            mine = 1

    return calc_round_points(theirs, mine)

def read_strategy_file_v2(filename):
    pnts = 0
    with open(filename, 'r') as fp:
        for line in fp:
            line = line.strip().lower()
            toks = line.split()
            if len(toks) == 2:
                pnts += calc_round_points_v2(convert(toks[0]), convert(toks[1]))
            else:
                raise Exception('invalid strategy line: \'%s\'' % line)
    return pnts

if __name__=='__main__':
    if len(sys.argv) != 2:
        print('usage: python main.py INPUT')
    pnts = read_strategy_file_v2(sys.argv[1])
    print('total points: %d' % pnts)
