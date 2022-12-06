import sys
import re
import ranges

def read_cleanup_file(filename, full_overlaps_only):
    sum = 0
    with open(filename, 'r') as fp:
        for line in fp:
            toks = re.split(',|-', line.strip())
            if len(toks) != 4:
                raise Exception('wrong line format. tokens: %s' % toks)
            r1 = ranges.Range(int(toks[0]), int(toks[1]), include_end=True)
            r2 = ranges.Range(int(toks[2]), int(toks[3]), include_end=True)
            r12 = r1.union(r2)
            if (full_overlaps_only == True and (r12 == r1 or r12 == r2))\
                or (full_overlaps_only == False and r12 != None):
                sum += 1
    return sum

if __name__=='__main__':
    if len(sys.argv) != 2:
        print('usage: python main.py INPUT')
    full_overlaps = read_cleanup_file(sys.argv[1], True)
    print('total full overlaps: %d' % full_overlaps)
    partial_overlaps = read_cleanup_file(sys.argv[1], False)
    print('total partial overlaps: %d' % partial_overlaps)
