import sys
import ast

def compare_ints(l, r):
    print('\tcomparing ints: %s vs %s' % (l, r)) 
    if l == r:
        return None
    return l < r


def compare_lists(l, r):
    print('\tcomparing lists: %s vs %s' % (l, r))
    if len(l) == 0 and len(r) > 0:
        print('left run out or items')
        return True
    elif len(r) == 0 and len(l) > 0:
        print('right run out or items')
        return False

    for i in range(0, len(l)):
        # right run out of items
        if i == len(r):
            print('right run out or items')
            return False

        # keep comparing
        print('comparing: %s, %s' % (l[i], r[i]))
        status = compare(l[i], r[i])
        if status != None:
            return status
        
        # left run out of items
        if i + 1 == len(l) and i + 1 < len(r):
            print('left run out or items')
            return True

def compare(l, r):
    print('\tcomparing packets: %s vs %s' % (l, r)) 
    # both ints
    if isinstance(l, int) and isinstance(r, int):
        return compare_ints(l, r)
    # both lists
    elif isinstance(l, list) and isinstance(r, list):
        return compare_lists(l, r)
    # one list, one int
    else:
        if isinstance(l, int):
            l_int = [l]
            return compare(l_int, r)
        else:
            r_int = [r]
            return compare(l, r_int)

    
def read_packets(filename):
    with open(filename, 'r') as fp:
        pair_id = 1
        total_right_order = 0
        while True:
            l = ast.literal_eval(fp.readline().strip())
            r = ast.literal_eval(fp.readline().strip())
            print('pair[%d]...' % pair_id)
            right_order = compare(l, r)
            print('...%s' % right_order)
            if right_order == True:
                total_right_order += pair_id
            pair_id += 1
            if not fp.readline():
                break

        print('sum of indices in right order: %d' % total_right_order)


if __name__=='__main__':
    if len(sys.argv) < 2:
        print('usage: python main.py INPUT')
    read_packets(sys.argv[1])

