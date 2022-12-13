import sys
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import dijkstra

def to_height(s):
    if s == 'E': # best signal
        return -2
    elif s == 'S': # start position
        return -1
    return ord(s) - 97

def to_letter(i):
    if i == -2: # best signal
        return 'E'
    elif i == -1: # start position
        return 'S'
    return chr(i + 97)

def read_map(filename):
    out = []
    with open(filename, 'r') as fp:
        for line in fp:
            line = line.strip()
            out.append([i for i in line])
    return out

def find_startend(data):
    start_i = None
    end_i = None

    rows = len(data)
    cols = len(data[0])
    for r in range(0, rows):
        for c in range(0, cols):
            if data[r][c] == 'S':
                start_i = to_index(r, c, cols)
            elif data[r][c] == 'E':
                end_i = to_index(r, c, cols)
    return (start_i, end_i)

def to_index(r, c, total_c):
    return r * total_c + c

def get_neighbors(r, c, total_r, total_c):
    neighbors = [(r+1, c), (r, c+1), (r, c-1), (r-1, c)]
    return [i for i in neighbors\
        if i[0] >= 0 and i[1] >= 0 and i[0] < total_r and i[1] < total_c]

def to_graph(data):
    rows = len(data)
    cols = len(data[0])
    total = rows * cols

    graph = [[0 for r in range(total)] for c in range(total)]

    for src_r in range(0, rows):
        for src_c in range(0, cols):
            # curr index
            src = data[src_r][src_c]
            src_height = to_height(src)
            src_index = to_index(src_r, src_c, cols)

            # find neighbors
            for n in get_neighbors(src_r, src_c, rows, cols):
                trg_r = n[0]
                trg_c = n[1]
                trg = data[trg_r][trg_c]
                trg_height = to_height(trg)
                trg_index = to_index(trg_r, trg_c, cols)
                
                # z-distance 
                dist = trg_height - src_height
                
                if trg == 'E':
                    if src == 'z':
                        graph[src_index][trg_index] = 1
                else:  
                    # all paths can leave S
                    if src == 'S':
                        graph[src_index][trg_index] = 1
                    # same height or change by +/- 1
                    elif abs(dist) == 1 or dist == 0:
                        graph[src_index][trg_index] = 1
                        graph[trg_index][src_index] = 1
                    # decreasing height more than one
                    elif dist < -1:
                        graph[src_index][trg_index] = 1

    return graph    
                     
if __name__=='__main__':
    if len(sys.argv) != 2:
        print('usage: python main.py INPUT')

    # read map
    raw_data = read_map(sys.argv[1])
    start_i, end_i = find_startend(raw_data)

    # convert to graph
    graph = csr_matrix(to_graph(raw_data))

    dist_matrix = dijkstra(
        csgraph=graph, unweighted=True, directed=True,
        indices=start_i)

    print('dist: %s' % dist_matrix[end_i])
