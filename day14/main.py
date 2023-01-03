import sys
import re


class Bounds:
    def __init__(self, minr, maxr, minc, maxc):
        self.minr = minr
        self.minc = minc
        self.maxr = maxr
        self.maxc = maxc

    def normalize(self):
        offr = -self.minr
        self.minr += offr
        self.maxr += offr
        
        offc = -self.minc
        self.minc += offc
        self.maxc += offc
        
        return offr, offc

    def print(self):
        print('boundaries: r->[%d, %d], c->[%d, %d]'
            % (self.minr, self.maxr, self.minc, self.maxc))


class Scan:
    def __init__(self, filename):
        self.spring = '+'
        self.rock = '#'
        self.sand = 'o'
        self.empty = '.'
        self.startr = 0 
        self.startc = 500        
        self.bounds = self._read_bounds(filename)
        self._read_scan(filename, self.bounds)


    def print(self):
        for i in self.scan:
            print('%s' % ''.join(i))
        

    def _read_bounds(self, filename):
        bounds = Bounds(0, -sys.maxsize, sys.maxsize, -sys.maxsize)
        with open(filename, 'r') as fp:
            for line in fp:
                pnts = list(filter(None, re.split('->|\W', line)))
                for i in range(0, len(pnts), 2):
                    c = int(pnts[i])
                    bounds.minc = min(c, bounds.minc)
                    bounds.maxc = max(c, bounds.maxc)
                    r = int(pnts[i + 1])
                    bounds.minr = min(r, bounds.minr)
                    bounds.maxr = max(r, bounds.maxr)
        return bounds


    def _read_scan(self, filename, bounds):
        # normalize
        normr, normc = bounds.normalize()
        self.startr += normr
        self.startc += normc
 
        # scan
        self.rows = bounds.maxr - bounds.minr + 1
        self.cols = bounds.maxc - bounds.minc + 1
        self.scan = [[self.empty for c in range(0, self.cols)] for r in range(0, self.rows)]
        self.scan[self.startr][self.startc] = self.spring

        #print_scan(scan)
        with open(filename, 'r') as fp:
            for line in fp:
                coords = [int(i) for i in list(filter(None, re.split('->|\W', line)))]
                prev_r = None
                prev_c = None
                for i in range(0, len(coords), 2):
                    c = coords[i] + normc
                    r = coords[i + 1] + normr

                    if prev_r is not None and prev_c is not None:
                        if prev_r == r:
                            for i in range(min(prev_c, c), max(prev_c, c) + 1):
                                self.scan[r][i] = self.rock
                        elif prev_c == c:
                            for i in range(min(prev_r, r), max(prev_r, r) + 1):
                                self.scan[i][c] = self.rock
                        else:
                            raise Exception('invalid line: %s' % line)
                    
                    prev_r = r
                    prev_c = c


    def drop_sand_unit(self):
        return self._drop_sand_unit(self.startr, self.startc)
                

    def _drop_sand_unit(self, r, c):
        #print('starting at (%d, %d) = %s' % (r, c, self.scan[r][c]))
        # abyss reached
        if r + 2 > self.rows or c < self.bounds.minc or c > self.bounds.maxc:
            return False

        # keep going down
        if self.scan[r + 1][c] == self.empty:
            #print('go down')
            return self._drop_sand_unit(r + 1, c)
        # path is blocked
        else:
            # go left
            if r + 2 > self.rows or self.scan[r + 1][c - 1] == self.empty:
                #print('go left')
                return self._drop_sand_unit(r + 1, c - 1)
            # go right
            elif r + 2 > self.rows or c + 1 < self.cols\
                and self.scan[r + 1][c + 1] == self.empty:
                #print('go right')
                return self._drop_sand_unit(r + 1, c + 1)
            # deposit
            else:
                #print('deposit')
                self.scan[r][c] = self.sand
                return True
                 
if __name__=='__main__':
    if len(sys.argv) < 2:
        print('usage: python main.py INPUT')
  
    scan = Scan(sys.argv[1])
    scan.print()
    total = 0
    while True:
        if scan.drop_sand_unit() == False:
            break
        total += 1
    
    scan.print()
    print('total sand units before abyss: %d' % total)
