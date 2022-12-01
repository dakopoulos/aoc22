import sys

def read_calories_file(filename):
    print('reading calories file: %s...' % filename)
    calories = []
    with open(filename, 'r') as fp:
        curr_calories = 0
        for line in fp:
            line = line.strip()
            if len(line) != 0:
                curr_calories += int(line)
            else:
                #print('elf #%d has total: %d calories' % (len(calories), curr_calories))
                calories.append(curr_calories)
                curr_calories = 0
    print('...done')
    return calories

if __name__=='__main__':
    if len(sys.argv) != 2:
        print('usage: python main.py INPUT')
    calories = read_calories_file(sys.argv[1])
    print('the elf with the most calories carries: %d' % max(calories))
