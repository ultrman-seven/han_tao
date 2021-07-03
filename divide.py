from library.lslidar import get_points
import numpy as np
from matplotlib import pyplot as plt

xd, yd = [], []
view = True

name = input('区域:\n"b":边界,"s":学生区,"t":老师区,"sh":屏蔽区')
areas = {'b':'area/boundary.txt','s':'area/student.txt','t':'area/teacher.txt','sh':'area/shield.txt'}
if name in areas:
    name = areas[name]
with open(name,'w',encoding = 'utf-8') as f:
    pass

def perssed(event):
    global name
    if event.button == 1:
        with open(name,'a',encoding = 'utf-8') as f:
            f.write(str(event.xdata))
            f.write(',')
            f.write(str(event.ydata))
            f.write('\n')
            xd.append(event.xdata)
            yd.append(event.ydata)
    if event.button == 3:
        with open('area/student.txt','w',encoding = 'utf-8') as f:
            xd.clear()
            yd.clear()
    if event.button == 2:
        if name != areas['sh']:
            global view
            view = not view
        else:
            with open(name,'a',encoding = 'utf-8') as f:
                f.write('next\n')
                xd.clear()
                yd.clear()

plt.ion()
fig = plt.figure()
while True:
    x, y = get_points()  
    plt.scatter(np.array(x),np.array(y))
    #plt.plot(np.array(x),np.array(y))
    plt.scatter(0,0, c = 'r',marker='x')
    if view and len(xd)!=0:
        plt.plot(np.array(xd),np.array(yd),'r')
        plt.scatter(xd[-1],yd[-1])
    else:
        plt.scatter(np.array(xd),np.array(yd), c = 'r')
    fig.canvas.mpl_connect('button_press_event',perssed)
    plt.show()
    plt.pause(0.02)
    plt.clf()