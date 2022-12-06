import sys

def to_priorities(items):
    priorities = []
    for i in items:
        order = ord(i)
        if order >= 97:
            priorities.append(order - 96)
        else:
            priorities.append(order - 38)
    return priorities
        

def read_rucksacks_file(filename):
    with open(filename, 'r') as fp:
        sum = 0
        for line in fp:
            line = line.strip()
            if len(line) % 2 != 0:
                raise Exception('number of items in both compartments must be equal')
            med = int(len(line) / 2)
            items1 = to_priorities(line[:med])
            items2 = to_priorities(line[med:])
            intersection = list(set(items1).intersection(items2))
            print('common item: %s' % intersection)
            if len(intersection) != 1:
                raise Exception('no common item is found')
            sum += intersection[0]

        print('sum of priorities: %d' % sum)

if __name__=='__main__':
    if len(sys.argv) != 2:
        print('usage: python main.py INPUT')
    read_rucksacks_file(sys.argv[1])
