import sys
import math
from enum import Enum

class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


def to_direction(s):
    str = s.lower()
    if str == 'u':
        return Direction.UP
    elif str == 'd':
        return Direction.DOWN
    elif str == 'l':
        return Direction.LEFT
    elif str == 'r':
        return Direction.RIGHT
    else:
        raise Exception('invalid direction: %s' % s)


class Position:
    def __init__(self, x_, y_):
      self.x = x_
      self.y = y_
    
    def move(self, direction, steps):
        if direction == Direction.UP:
            self.y += steps
        elif direction == Direction.DOWN:
            self.y -= steps
        elif direction == Direction.LEFT:
            self.x -= steps
        elif direction == Direction.RIGHT:
            self.x += steps


def move_knot(tail, head):
    dx = head.x - tail.x
    dy = head.y - tail.y
    if abs(dx) > 2 or abs(dy) > 2:
        raise Exception('head moved too far away')
    
    if abs(dx) < 2 and abs(dy) < 2:
        return False
    elif abs(dx) == 2:
        dx /= 2
        if abs(dy) > 0:
            dy = 1 if dy > 0 else -1
    elif abs(dy) == 2:
        dy /= 2
        if abs(dx) > 0:
            dx = 1 if dx > 0 else -1
        
    tail.x += dx
    tail.y += dy

    return True


def read_bridge_motions_file(filename, max_rope_size):
    with open(filename, 'r') as fp:
        # original positions for head and tail
        rope = [Position(0, 0)]

        # all positions that the tail visited
        visited = set()
        visited.add((rope[0].x, rope[0].y))

        for line in fp:
            toks = line.strip().split()
            if len(toks) != 2:
                raise Exception('invalid line: "%s"' % line)

            # movement of head
            direction = to_direction(toks[0])
            steps = int(toks[1])

            # step-by-step
            for step in range(0, steps):
                # move head
                rope[0].move(direction, 1)

                # move knots based on the previous knot
                last_knot_moved = False
                for knot in range(1, len(rope)):
                    last_knot_moved = move_knot(rope[knot], rope[knot - 1])
                if len(rope) == 10:
                    visited.add((rope[-1].x, rope[-1].y))

                # add knot
                if len(rope) == 1 or (last_knot_moved == True and len(rope) < max_rope_size):
                    rope.append(Position(0, 0))

    return visited


if __name__=='__main__':
    argc = len(sys.argv)
    if argc != 2 or argc != 3:
        print('usage: python main.py INPUT [ROPESIZE=2]')
    ropesize = int(sys.argv[2]) if argc == 3 else 2
    visited = read_bridge_motions_file(sys.argv[1], ropesize)
    print('total visited: %d' % len(visited))
