def get_area(filename):
    area = []
    with open(filename,'r',encoding = 'utf-8') as f:
        for line in f.readlines():
            if line != '\n':
                x,y = line.split(',')
                area.append([float(x),float(y)])
    return area

def get_shields(filename):
    shields = []
    with open(filename,'r',encoding = 'utf-8') as f:
        sh = []
        for line in f.readlines():
            if line == 'next':
                shields.append(sh)
                sh.clear()
            elif line != '\n':
                x,y = line.split(',')
                sh.append([float(x),float(y)])
    return shields
