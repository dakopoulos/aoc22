import sys
import ast
import functools

def compare_ints(l, r):
    #print('\tcomparing ints: %s vs %s' % (l, r)) 
    if l == r:
        return None
    return l < r


def compare_lists(l, r):
    #print('\tcomparing lists: %s vs %s' % (l, r))
    if len(l) == 0 and len(r) > 0:
        #print('left run out or items')
        return True
    elif len(r) == 0 and len(l) > 0:
        #print('right run out or items')
        return False

    for i in range(0, len(l)):
        # right run out of items
        if i == len(r):
            #print('right run out or items')
            return False

        # keep comparing
        #print('comparing: %s, %s' % (l[i], r[i]))
        status = compare(l[i], r[i])
        if status != None:
            return status
        
        # left run out of items
        if i + 1 == len(l) and i + 1 < len(r):
            #print('left run out or items')
            return True

def compare(l, r):
    #print('\tcomparing packets: %s vs %s' % (l, r)) 
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

def compare_for_sorting(l, r):
    status = compare(l, r)
    if status == True:
        return -1
    elif status == False:
        return 1
    return 0

    
def read_packets(filename):
    packets = []
    with open(filename, 'r') as fp:
        while True:
            packets.append(ast.literal_eval(fp.readline().strip()))
            packets.append(ast.literal_eval(fp.readline().strip()))
            if not fp.readline():
                break
    return packets


def find_sum_of_indices_in_right_order(packets):
    pair_id = 1
    total_right_order = 0
    for i in range(0, len(packets), 2):
        if compare(packets[i], packets[i+1]) == True:
            total_right_order += pair_id
        pair_id += 1
    return total_right_order 


def print_packets(packets):
    for i in packets:
        print('%s' % i)


def sort_packets(packets):
    return sorted(packets, key=functools.cmp_to_key(compare_for_sorting))


if __name__=='__main__':
    if len(sys.argv) < 2:
        print('usage: python main.py INPUT')
    print('reading packets...')
    packets = read_packets(sys.argv[1])
    print('finding sum of indices in right order...')
    total_right_order = find_sum_of_indices_in_right_order(packets)
    print('sum of indices in right order: %d' % total_right_order)
    
    print('inserting missing packets...')
    miss1 = [[2]]
    packets.append(miss1)
    miss2 = [[6]]
    packets.append(miss2)
    print('sorting...')
    sorted_packets = sort_packets(packets)
    print('finding indexes...')
    m1 = sorted_packets.index(miss1) + 1
    m2 = sorted_packets.index(miss2) + 1
    print('decoder key: %d = %d x %d' % (m1 * m2, m1, m2))
    
    #print_packets(sorted_packets)
