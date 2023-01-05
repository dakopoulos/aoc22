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
    def __init__(self, filename, unbound=False):
        self.spring = '+'
        self.rock = '#'
        self.sand = 'o'
        self.empty = '.'
        self.startr = 0 
        self.startc = 500
        self.unbound = unbound
        bounds = self._read_bounds(filename)
        self._read_scan(filename, bounds)


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
            if self.unbound == True:
                bounds.maxr += 2

        return bounds


    def _read_scan(self, filename, bounds):
        # normalize
        normr, normc = bounds.normalize()
        self.startr += normr
        self.startc += normc
 
        # scan
        rows = bounds.maxr - bounds.minr + 1
        cols = bounds.maxc - bounds.minc + 1
        self.scan = [[self.empty for c in range(0, cols)] for r in range(0, rows)]
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
            if self.unbound:
                self.scan[-1] = [self.rock for c in range(0, len(self.scan[0]))]

    def drop_sand_unit(self):
        #print('New drop!')
        return self._drop_sand_unit_unbound(self.startr, self.startc) if self.unbound == True\
            else self._drop_sand_unit(self.startr, self.startc)
                
    
    def _drop_sand_unit(self, r, c):
        #print('starting at (%d, %d) = %s' % (r, c, self.scan[r][c]))
        # abyss reached
        if r + 2 > len(self.scan) or c < 0 or c > len(self.scan[r]) - 1:
            return False

        # keep going down
        if self.scan[r + 1][c] == self.empty:
            #print('go down')
            return self._drop_sand_unit(r + 1, c)
        # path is blocked
        else:
            # go left
            if r + 2 > len(self.scan) or self.scan[r + 1][c - 1] == self.empty:
                #print('go left')
                return self._drop_sand_unit(r + 1, c - 1)
            # go right
            elif r + 2 > len(self.scan) or c + 1 < len(self.scan[0])\
                and self.scan[r + 1][c + 1] == self.empty:
                #print('go right')
                return self._drop_sand_unit(r + 1, c + 1)
            # deposit
            else:
                #print('deposit')
                self.scan[r][c] = self.sand
                return True

    
    def _increase_columns(self, offset):
        #print('\t\tincrease cols: %d' % offset)
        for r in range(0, len(self.scan)):
            deposit = self.empty if r < len(self.scan) - 1 else self.rock
            if offset > 0:
                self.scan[r] = self.scan[r] + [deposit for i in range(abs(offset))]
            elif offset < 0:
                self.scan[r] = [deposit for i in range(abs(offset))] + self.scan[r]
        if offset < 0:
            self.startc += abs(offset)
        #self.print()


    def _drop_sand_unit_unbound(self, r, c):
        #print('\tstarting at (%d, %d)' % (r, c))
        # increase scan area
        if c < 0:
            #print('\treach left boundary...')
            self._increase_columns(c)
            c += abs(c) 
            #print('\t\tupdated starting at (%d, %d)' % (r, c))
        elif c >= len(self.scan[0]) - 1:
            #print('\t\treach right boundary...')
            self._increase_columns(c - len(self.scan[0]) + 2)
            #print('\t\tupdated starting at (%d, %d)' % (r, c))

        # keep going down
        if self.scan[r + 1][c] == self.empty:
            #print('\t\tgo down')
            return self._drop_sand_unit_unbound(r + 1, c)
        # path is blocked
        else:
            # deposit and stop if spring is reached
            # if last floor is reached
            # OR next row left and right is blocked with sand/rock.
            if r + 2 >= len(self.scan)\
                or ((self.scan[r + 1][c - 1] == self.rock
                     or self.scan[r + 1][c - 1] == self.sand)\
                    and (self.scan[r + 1][c + 1] == self.rock
                         or self.scan[r + 1][c + 1] == self.sand)):
                #print('\t\tdeposit')
                self.scan[r][c] = self.sand
                #self.print()
                return False if r == self.startr and c == self.startc else True
            # go left
            if self.scan[r + 1][c - 1] == self.empty:
                #print('\t\tgo left')
                return self._drop_sand_unit_unbound(r + 1, c - 1)
            # go right
            if c + 1 == len(self.scan[0]) or self.scan[r + 1][c + 1] == self.empty:
                #print('\t\tgo right')
                return self._drop_sand_unit_unbound(r + 1, c + 1)
            #print('r + 2 = %d; len(scan): %d' % (r + 2, len(self.scan)))
            raise Exception('shouldn\'t be here') 
if __name__=='__main__':
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print('usage: python main.py INPUT [UNBOUND]')
  
    unbound = False if len(sys.argv) == 2 else True if sys.argv[2] == '1' else False
    print('unbound: %s' % unbound)
    scan = Scan(sys.argv[1], unbound)
    scan.print()
    total = 0
    while True:
        if scan.drop_sand_unit() == False:
            if unbound == True:
                total += 1
            break
        total += 1
    
    scan.print()
    print('total sand units: %d' % total)
