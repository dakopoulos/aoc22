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
    rng = grid[r][:c]
    rng.reverse()
    return rng

def get_right(grid, r, c):
    return grid[r][c+1:]

def get_up(grid, r, c):
    out = []
    for i in reversed(range(0, r)):
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
            if is_outside_tree(grid, r, c)\
               or max(get_up(grid, r, c)) < grid[r][c]\
               or max(get_down(grid, r, c)) < grid[r][c]\
               or max(get_left(grid, r, c)) < grid[r][c]\
               or max(get_right(grid, r, c)) < grid[r][c]:
                total += 1
                 
    return total

def calc_viewing_distance(tree, neighbors):
    dist = 0
    if neighbors is not None:
        for i in neighbors:
            if i < tree:
                dist += 1
            else:
                dist += 1
                break
    return dist

def add_dist(dist, total):
    if dist > 0:
        if total == 0:
            total = dist
        else:
            total *= dist
    return total
    

def calc_scenic_score(grid, r, c):
    score = 0 
    tree = grid[r][c]
    
    score = add_dist(calc_viewing_distance(tree, get_up(grid, r, c)), score)
    score = add_dist(calc_viewing_distance(tree, get_down(grid, r, c)), score)
    score = add_dist(calc_viewing_distance(tree, get_left(grid, r, c)), score)
    score = add_dist(calc_viewing_distance(tree, get_right(grid, r, c)), score)
    
    return score;

def find_best_scenic_score(grid):
    num_rows = len(grid)
    if len(grid) == 0:
        return
    num_cols = len(grid[0])
    
    best = 0
    for r in range(0, num_rows):
        for c in range(0, num_cols):
            best = max(best, calc_scenic_score(grid, r, c))
    return best


if __name__=='__main__':
    if len(sys.argv) != 2:
        print('usage: python main.py INPUT')
    grid = read_tree_grid(sys.argv[1])
    print('total visible: %d' % count_visible_trees(grid))
    print('best scenic score: %d' % find_best_scenic_score(grid))
