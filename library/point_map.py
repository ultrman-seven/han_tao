import numpy as np
from numpy.linalg import solve
import math
import library.picture_draw as pd
class Point():
    def __init__(self, x=0, y=0, z = 0, rh = None, theta = None):
        self.z = z
        self.rh, self.theta = rh, theta
        if rh == None:
            self.x, self.y = x,y
        else:          
            self.x = rh * math.cos(theta)
            self.y = rh * math.sin(theta)

    def turn_to_polar(self):
        self.theta = math.atan2(self.y,self.x)
        self.rh = math.sqrt(self.x**2 + self.y**2)

    def comput_distance(self, point):
        return math.sqrt((self.x-point.x)**2 + (self.y-point.y)**2)

    def comput_middle_point(self,point):
        return Point((self.x+point.x)/2, (self.y+point.y)/2)

    def comput_turn_angle(self,from_,to):
        p1 = Point(from_.x-self.x, from_.y - self.y)
        p2 = Point(to.x-self.x, to.y - self.y)
        p1.turn_to_polar()
        p2.turn_to_polar()
        if p1.theta<0:
           p1.theta = p1.theta
        if p2.theta<0:
           p2.theta = p2.theta
        result = p2.theta - p1.theta
        while math.fabs(result) > math.pi:
            if result>0:
                result = result-2*math.pi
            else:
                result = result+2*math.pi
        return result

    def equal_to(self, point):
        if self.x == point.x and self.y == point.y:
            return True
        return False

class Line():
    def __init__(self, p1, p2):
        self.point1, self.point2 = p1, p2
        self.a, self.b = solve(np.array([[p1.x,1],[p2.x,1]]), np.array([p1.y,p2.y]))

    def comput_distance(self, point):
        dis = ((self.a * point.x - point.y + self.b)**2) / (self.a**2+1)
        return math.sqrt(dis)


class Area():
    def __init__(self, points):
        self.points = []
        for x, y in points:
            self.points.append(Point(x, y))

    def is_in_area(self, point):
        points = self.points[:]
        points.append(self.points[0])
        turn_angle = 0
        for i in range(len(self.points)):
            turn_angle = turn_angle + point.comput_turn_angle(points[i],points[i+1])
        if turn_angle > math.pi:
            return True
        return False

    def draw(self, color):
        points = self.points[:]
        points.append(self.points[0])
        pd.draw_area(points,color)


class Map():
    def __init__(self, boundary, student, teacher, shields=[]):
        self.boundary = Area(boundary)
        self.stu = Area(student)
        self.tea = Area(teacher)
        self.shields = []
        for shield in shields:
            self.shields.append(Area(shield))

    def is_in_map(self,point):
        if self.boundary.is_in_area(point):
            for shield in self.shields:
                if shield.is_in_area(point):
                    return False
            return True
        return False


    def is_teacher(self, point):
        if self.tea.is_in_area(point):
            return True
        return False

    def is_student(self, point):
        if self.stu.is_in_area(point):
            return True
        return False

    def draw(self):
        self.boundary.draw('r')
        self.stu.draw('y')
        self.tea.draw('k')
        for sh in self.shields:
            sh.draw('g')

def comput_distance(p1, p2):
    return math.sqrt((p1.x-p2.x)**2 + (p1.y-p2.y)**2)

def call_middle_point(p1, p2):
    return Point((p1.x+p2.x)/2, (p1.y+p2.y)/2)

def is_equal(p1, p2):
    if p1.x == p2.x and p1.y == p2.y:
        return True
    return False
