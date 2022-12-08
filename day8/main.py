import sys
import re
import ranges

def read_tree_grid(filename):
    grid = []
    with open(filename, 'r') as fp:
        for line in fp:
            new_row = [int(i) for i in line.strip()]
            if len(grid) and len(grid[-1]) != len(new_row):
                raise Exception('inconsistent size of row')
            grid.append(new_row)
    return grid

def is_outside_tree(grid, r, c):
    return r == 0 or c == 0\
        or r == len(grid) - 1 or c == len(grid[r]) - 1

def get_left(grid, r, c):
    return grid[r][:c]

def get_right(grid, r, c):
    return grid[r][c+1:]

def get_up(grid, r, c):
    out = []
    for i in range(0, r):
        out.append(grid[i][c])
    return out 

def get_down(grid, r, c):
    out = []
    for i in range(r + 1, len(grid)):
        out.append(grid[i][c])
    return out 

def count_visible_trees(grid):
    num_rows = len(grid)
    if len(grid) == 0:
        return
    num_cols = len(grid[0])
    
    total = 0
    for r in range(0, num_rows):
        for c in range(0, num_cols):
            # handle trees on the perimeter
            if is_outside_tree(grid, r, c)\
               or max(get_up(grid, r, c)) < grid[r][c]\
               or max(get_down(grid, r, c)) < grid[r][c]\
               or max(get_left(grid, r, c)) < grid[r][c]\
               or max(get_right(grid, r, c)) < grid[r][c]:
                total += 1
                 
    return total

if __name__=='__main__':
    if len(sys.argv) != 2:
        print('usage: python main.py INPUT')
    grid = read_tree_grid(sys.argv[1])
    print('total visible: %d' % count_visible_trees(grid))
