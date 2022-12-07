import sys
import re
import ranges

def read_signal(filename, marker_length=4):
    out = 0
    with open(filename, 'r') as fp:
        line = fp.readline().strip()
        buffer = []
        for i in range(0, len(line)):
            if len(buffer) == marker_length:
                buffer = buffer[1:]
            buffer.append(line[i])
            if len(buffer) == marker_length and len(set(buffer)) == len(buffer):
                return i + 1

if __name__=='__main__':
    if len(sys.argv) != 2:
        print('usage: python main.py INPUT')
    sop_marker = read_signal(sys.argv[1], 4) 
    print('start-of-packet marker: %d' % sop_marker)
    som_marker = read_signal(sys.argv[1], 14) 
    print('start-of-message marker: %d' % som_marker)
