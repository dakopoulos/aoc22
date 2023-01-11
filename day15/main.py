import sys
import re
import multirange
import copy

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def print(self):
        print('pnt(%d, %d)' % (self.x, self.y))

    def manhattan(self, p):
        return abs(self.x - p.x) + abs(self.y - p.y) 

class Sensor:
    def __init__(self, loc, beacon):
        self.loc = loc
        self.beacon = beacon

    def print(self):
        print('Sensor: (%d, %d); Beacon: (%d, %d)'
            % (self.loc.x, self.loc.y, self.beacon.x, self.beacon.y))

    def calc_locations_without_beacon(self):
        locs = {}
        dist = self.loc.manhattan(self.beacon)
        for dy in range(-dist, dist + 1):
            xdiff = abs(dist - abs(dy))
            rang = range(self.loc.x - xdiff, self.loc.x + xdiff + 1)
            locs[self.loc.y + dy] = rang
        return locs

class Bounds:
    def __init__(self, minx, miny, maxx, maxy):
        self.min = Point(minx, miny)
        self.max = Point(maxx, maxy)

    def update(self, x, y):
        self.min.x = min(x, self.min.x)
        self.min.y = min(y, self.min.y)
        self.max.x = max(x, self.max.x)
        self.max.y = max(y, self.max.y)

    def print(self):
        print('bounds: min(%d, %d); max(%d, %d)'
            % (self.min.x, self.min.y, self.max.x, self.max.y))


def read_data(filename):
    sensors = []
    bounds = Bounds(sys.maxsize, sys.maxsize, -sys.maxsize, -sys.maxsize)
    with open(filename, 'r') as fp:
        for line in fp:
            coords = [int(i) for i in re.findall('[+|-]*[0-9]+', line)]

            for i in range(0, len(coords), 2):
                bounds.update(coords[i], coords[i+1])

            if len(coords) != 4:
                raise Exception('invalid line: %s' % line)
            sensors.append(
                Sensor(Point(coords[0], coords[1]),
                Point(coords[2], coords[3])))
    return sensors, bounds


def multirange_to_set(mr):
    out = set()
    for r in mr:
        out = out.union(set(r))
    return out


if __name__=='__main__':
    if len(sys.argv) < 2 or len(sys.argv) > 4:
        print('usage: python main.py INPUT [Y | MIND MAXD]')

    # inputs
    filename = sys.argv[1]
    trg_y = None
    min_dim = None
    max_dim = None
    if len(sys.argv) == 3:
        trg_y = int(sys.argv[2])
    elif len(sys.argv) == 4:
        min_dim = int(sys.argv[2])
        max_dim = int(sys.argv[3])
    print('settings: filename(%s); y(%s); min,max=(%s, %s)' % (filename, trg_y, min_dim, max_dim))

    # read data
    print('reading data...')
    sensors, bounds = read_data(sys.argv[1])

    # calculate empty locations
    print('calculating possible locations...')
    empty_locs = {}
    for s in sensors:
        locs = s.calc_locations_without_beacon()
        for y, rang in locs.items():
            if y not in empty_locs:
                empty_locs[y] = [rang]
            else:
                tmp = copy.deepcopy(empty_locs[y])
                empty_locs[y] = []
                for r in multirange.normalize_multi(tmp + [rang]):
                    empty_locs[y].append(r)

    # part 2
    if min_dim is not None and max_dim is not None:
        print('calculating tuning frequency...')
        all_positions = range(min_dim, max_dim + 1)
        for y, rang in empty_locs.items():
            if y >= min_dim and y <= max_dim:
                possible_positions = list(multirange.difference_one_multi(all_positions, empty_locs[y]))
                if len(possible_positions) == 1 and len(list(possible_positions[0])) == 1:
                    x = list(possible_positions[0])[0]
                    freq = x * 4000000 + y
                    print('tuning frequency: %d' % freq)
                    break

    # part1: find total positions on target-y than cannot contain a beacon
    # (remove locations of sensors and beacons)
    if trg_y != None:
        print('removing locations of sensors and beacons...')
        if trg_y in empty_locs:
            trg_y_locs = multirange_to_set(empty_locs[trg_y])
            for s in sensors:
                if s.loc.y == trg_y:
                    trg_y_locs -= {s.loc.x}
                if s.beacon.y == trg_y:
                    trg_y_locs -= {s.beacon.x}
            print('Positions that cannot contain beacon (y=%d): %d' % (trg_y, len(trg_y_locs)))
        
