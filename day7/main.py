import sys
import igraph

def goto_root(fs):
    return 0

def is_cmd(line):
    if len(line) > 0:
        return line.startswith('$ ')
    return False

def add_dir(fs, pwd, dirname):
    for i in pwd.successors():
        if i['name'] == dirname and i['type'] == 'dir':
            return
    fs.add_vertex(1)
    new_id = fs.vcount() - 1
    fs.add_edges([(pwd, new_id)])
    newdir = fs.vs[new_id]
    newdir['name'] = dirname
    newdir['type'] = 'dir'
    newdir['size'] = 0

def add_file(fs, pwd, filename, filesize):
    for i in pwd.successors():
        if i['name'] == filename and i['type'] == 'file':
            return
    fs.add_vertex(1)
    new_id = fs.vcount() - 1
    fs.add_edges([(pwd, new_id)])
    newfile = fs.vs[new_id]
    newfile['name'] = filename
    newfile['type'] = 'file'
    newfile['size'] = filesize
    

def read_fs(filename):
    fs = igraph.Graph(1, directed=True)
    fs.vs[0]['name'] = '/'
    fs.vs[0]['type'] = 'dir'
    fs.vs[0]['size'] = 0

    pwd = fs.vs[0]
    with open(filename, 'r') as fp:
        read_files = False
        for line in fp:
            line = line.strip()
            
            if is_cmd(line):
                read_files = False
                if line == '$ cd /':
                    pwd = fs.vs[0]
                elif line == '$ cd ..':
                    if pwd != fs.vs[0]:
                        pwd = pwd.predecessors()[0]
                elif line.startswith('$ cd '):
                    dirname = line.split()[2]
                    for i in pwd.successors():
                        if i['name'] == dirname and i['type'] == 'dir':
                            pwd = i
            else:
                if line.startswith('dir '):
                    add_dir(fs, pwd, line[4:])
                else:
                    toks = line.split()
                    add_file(fs, pwd, toks[1], int(toks[0]))
    
    return fs

def calc_dir_sizes(d, threshold):
    total = 0
    total_below_threshold = 0
    for f in d.successors():
        total += f['size']
        if f['type'] == 'dir':
            newtotals = calc_dir_sizes(f, threshold)
            total += newtotals[0]
            total_below_threshold += newtotals[1]
    if total <= threshold:
        total_below_threshold += total
    return (total, total_below_threshold)

if __name__=='__main__':
    if len(sys.argv) != 2:
        print('usage: python main.py INPUT')
    fs = read_fs(sys.argv[1])
    print(calc_dir_sizes(fs.vs[0], 100000))
