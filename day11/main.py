import sys
import re
import copy

class Operation:
    def __init__(self, op1, op, op2):
        if op1 != 'old':
            raise Exception('unknown operand: %s' % op1)
        if op != '+' and op != '-' and op != '*':
            raise Exception('unknown operand: %s' % op)
        self.op1 = op1
        self.op = op
        self.op2 = op2


class Item:
    def __init__(self, worry_level):
        self.worry_level = worry_level

    def apply(self, op):
        op1 = self.worry_level
        op2 = self.worry_level if op.op2 == 'old' else int(op.op2)
        if op.op == '+':
            self.worry_level = op1 + op2
        elif op.op == '*':
            self.worry_level = op1 * op2
        elif op.op == '-':
            self.worry_level = op1 - op2
            


class Monkey:
    def __init__(self, mod, op, trg1, trg2, items=[]):
        self.items = items
        self.mod = mod
        self.op = op
        self.trg1 = trg1
        self.trg2 = trg2
        self.total_inspections = 0

    def print(self):
        print('Monkey:'\
            '\n\tmod  : %d'\
            '\n\top   : %s %s %s'\
            '\n\titems: %s'\
            % (self.mod, self.op.op1, self.op.op, self.op.op2, self.items))

    def inspect_item(self, i):
        if i >= 0 and i < len(self.items):
            self.total_inspections += 1
            item = self.items[i]
            item.apply(self.op)
            item.worry_level = int(item.worry_level / 3)
            if item.worry_level % self.mod == 0:
                return self.trg1
            else:
                return self.trg2


def read_monkey(fp):
    line = fp.readline().strip()
    line = line[len('Starting items: '):]
    toks = re.split(',', line)
    items = [Item(int(i)) for i in toks]
    
    line = fp.readline().strip()
    line = line[len('Operation: new = '):]
    toks = re.split(' ', line)
    op1 = toks[0].strip()
    op = toks[1].strip()
    op2 = toks[2].strip()

    line = fp.readline().strip()
    line = line[len('Test: divisible by '):]
    mod = int(line)

    line = fp.readline().strip()
    line = line[len('If true: throw to monkey '):]
    trg1 = int(line)

    line = fp.readline().strip()
    line = line[len('If false: throw to monkey '):]
    trg2 = int(line)

    return Monkey(mod, Operation(op1, op, op2), trg1, trg2, items)
    

def read_monkeys(filename):
    monkeys = []
    with open(filename, 'r') as fp:
        for line in fp:
            if line.startswith('Monkey'):
                monkeys.append(read_monkey(fp))

    return monkeys

if __name__=='__main__':
    if len(sys.argv) != 2:
        print('usage: python main.py INPUT')

    monkeys = read_monkeys(sys.argv[1])
    # round
    for round in range(0, 20):
        # monkey
        for i in range(0, len(monkeys)):
            monkey = monkeys[i]
            print('Monkey %d' % i)
            # inspect all items
            for j in range(0, len(monkey.items)):
                print('\tInspect item with worry level %d' % monkey.items[j].worry_level)
                trg = monkey.inspect_item(j)
                print('\tItem with worry level %d is thrown to monkey %d'\
                    % (monkey.items[j].worry_level, trg))
                # throw
                monkeys[trg].items.append(monkey.items[j])
            # clear this monkey's items
            monkey.items = []

    for i in range(0, len(monkeys)):
        print('Monkey %d: %s' % (i, [i.worry_level for i in monkeys[i].items]))

    for i in range(0, len(monkeys)):
        print('Monkey insepected items: %d' % monkeys[i].total_inspections)
    
    inspections = [i.total_inspections for i in monkeys]
    inspections.sort()
    monkey_business = inspections[-1] * inspections[-2]
    print('Monkey business: %d' % monkey_business)
