import sys

class Processor:
    def __init__(self, critical_ticks=set()):
        self.clock = 0
        self.register = 1
        self.critical_ticks = critical_ticks
        self.sum_of_critical_signals = 0
    
    def signal(self):
        return self.clock * self.register
    
    def run(self, cmd, val):
        # error handling
        if (cmd != 'noop' and cmd != 'addx')\
           or (cmd == 'noop' and len(val) != 0)\
           or (cmd == 'addx' and len(val) == 0):
            raise Exception('invalid command: %s' % line)

        # noop
        if cmd == 'noop':
            self._inc_clock()
        # add to register
        elif cmd == 'addx':
            self._inc_clock()
            self._inc_clock()
            add = int(val)
            self.register += add
        else:
            raise Exception('fail')

    def _inc_clock(self):
        self.clock += 1
        if self.clock in self.critical_ticks:
            print('clock[%d]; register[%d]; signal[%d]' % (self.clock, self.register, self.signal()))
            self.sum_of_critical_signals += self.signal()

    def run_program(self, filename):
        with open(filename, 'r') as fp:
            for line in fp:
                line = line.strip()
                toks = line.split()
                cmd = toks[0]
                val = ' '.join(toks[1:])
                self.run(cmd, val)

if __name__=='__main__':
    if len(sys.argv) != 2:
        print('usage: python main.py INPUT')

    critical_ticks = set((20, 60, 100, 140, 180, 220))
    processor = Processor(critical_ticks)
    processor.run_program(sys.argv[1])
    print('sum of critical signals: %d' % processor.sum_of_critical_signals)
