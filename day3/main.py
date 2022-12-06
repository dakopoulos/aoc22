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


def common_items(items1, items2):
    return list(set(items1).intersection(items2))


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
            intersection = common_items(items1, items2)
            if len(intersection) != 1:
                raise Exception('no common item is found')
            sum += intersection[0]

        print('sum of priorities: %d' % sum)


def extract_group(rucksacks):
    print('proceessing %d rucksacks' % len(rucksacks))
    for i in range(0, len(rucksacks)):
        for j in range(i + 1, len(rucksacks)):
            common_ij = common_items(rucksacks[i], rucksacks[j])
            for k in range(j + 1, len(rucksacks)):
                common_ijk = common_items(common_ij, rucksacks[k])
                if len(common_ijk) == 1:
                    return [[i, j, k], common_ijk[0]]
    raise Exception('can\'t find group')

def read_rucksacks_file_v2(filename):
    # create list of all items
    rucksacks = []
    with open(filename, 'r') as fp:
        for line in fp:
            line = line.strip()
            if len(line) % 2 != 0:
                raise Exception('number of items in both compartments must be equal')
            rucksacks.append(to_priorities(line))

    # extract groups
    sum = 0
    while len(rucksacks) != 0: 
        group_info = extract_group(rucksacks)
        sum += group_info[1]
        for i in sorted(group_info[0], reverse=True):
            rucksacks.pop(i)
    return sum

if __name__=='__main__':
    if len(sys.argv) != 2:
        print('usage: python main.py INPUT')
    sum = read_rucksacks_file_v2(sys.argv[1])
    print('sum of priorities: %d' % sum)
