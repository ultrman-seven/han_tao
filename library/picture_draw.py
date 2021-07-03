from matplotlib import pyplot as plt
import numpy as np

def pic_start():
    plt.ion()

def draw_points(points, color = 'b'):
    x,y =[], []
    for p in points:
        x.append(p.x)
        y.append(p.y)
    plt.scatter(np.array(x),np.array(y), c = color)

def pic_show():
    plt.show()
    plt.pause(0.02)
    plt.clf()

def draw_boundray(x, y, color = 'k'):
    plt.scatter(np.array(x),np.array(y), c=color)

def draw_area(points, color = 'r'):
    x,y =[], []
    for p in points:
        x.append(p.x)
        y.append(p.y)
    plt.plot(np.array(x),np.array(y),color)
