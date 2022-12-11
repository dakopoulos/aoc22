import sys


class Processor:
    def __init__(self, crt, critical_ticks=set()):
        self.crt = crt
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
        self.crt.draw(self.clock, self.register)
        self.clock += 1
        if self.clock in self.critical_ticks:
            self.sum_of_critical_signals += self.signal()

    def run_program(self, filename):
        with open(filename, 'r') as fp:
            for line in fp:
                line = line.strip()
                toks = line.split()
                cmd = toks[0]
                val = ' '.join(toks[1:])
                self.run(cmd, val)

class CRT:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.data = []
        for i in range(0, rows):
            self.data.append(['.']*self.cols)

    def render(self):
        print('----- CRT ------------------------------')
        for i in self.data:
            print(''.join(i))
        print('------CRT ------------------------------')

    def draw(self, pixel, sprite):
        r = int(pixel / self.cols) % self.rows
        c = int(pixel % self.cols)
        #print('pixel: %d, sprite: %d, (r=%d, c=%d)' % (pixel, sprite, r, c))
        if c in range(sprite - 1, sprite + 2):
            self.data[r][c] = '#'


if __name__=='__main__':
    if len(sys.argv) != 2:
        print('usage: python main.py INPUT')

    crt = CRT(6, 40)
    critical_ticks = set((20, 60, 100, 140, 180, 220))
    processor = Processor(crt, critical_ticks)
    processor.run_program(sys.argv[1])
    crt.render()
