import sys
import re
import numpy

def line_has_only_numbers(line):
    toks = line.strip().split()
    for i in toks:
        if not i.isnumeric():
            return False
    return True


def read_total_stacks(filename):
    with open(filename, 'r') as fp:
        for line in fp:
            if line_has_only_numbers(line):
                return int(line.strip().split()[-1])
    raise Exception('cannot find total stacks')


def init_stacks(filename):
    # read total stacks
    stacks = [[] for _ in range(read_total_stacks(filename))]
    
    # initialize 
    with open(filename, 'r') as fp:
        for line in fp:
            line = line[0:-1] # remove newline
            if line_has_only_numbers(line):
                break
            toks = [line[i:i+4] for i in range(0, len(line), 4)]
            for i in range(0, len(toks)):
                tok = toks[i].strip()
                if tok != '':
                    crate = list(filter(None, re.split('\[|\]', tok)))[0]
                    stacks[i].insert(0, crate)
    
    return stacks

def rearrange(filename, stacks):
    read_moves = False
    with open(filename, 'r') as fp:
        for line in fp:
            line = line.strip()
            # found empty line --> move lines start
            if not line:
                read_moves = True
                continue
            if read_moves == True:
                # read move line and rearrange
                moves = list(filter(None, re.split(' |move|from|to', line)))
                if len(moves) != 3:
                    raise Exception('invalid line: %s' % line)
                total = int(moves[0])
                src = int(moves[1]) - 1
                trg = int(moves[2]) - 1
                for i in range(0, total):
                    if len(stacks[src]) > 0:
                        crate = stacks[src].pop()
                        stacks[trg].append(crate)


def get_top_crates(stacks):
    out = ''
    for i in stacks:
        if len(i) > 0:
            out += i[-1]
    return out


def read_rearrangement_file(filename):
    # init stacks
    stacks = init_stacks(filename)

    # rearrange
    rearrange(filename, stacks)

    top_crates = get_top_crates(stacks)
    print('top crates: %s' % top_crates)
    

if __name__=='__main__':
    if len(sys.argv) != 2:
        print('usage: python main.py INPUT')
    read_rearrangement_file(sys.argv[1]) 
