import enum
import library.picture_draw as pd
import library.camera_control as cc
from library.point_map import call_middle_point, comput_distance

class Identity(enum.Enum):
    student = 1
    teacher = 2

class Person():
    def __init__(self,identity, height=1.5):
        self.number = [0,0,0]
        self.cam = None
        self.id = identity
        self.height = height
        self.position = []
        self.past_position = []

    def camera_init(self, name, x,y,z, rotationAngle, camHorSpeed=10, camVerSpeed=10):
        self.cam = cc.Camera(name, x,y,z, rotationAngle, camHorSpeed=10, camVerSpeed=10)

    def camera_track_person(self, poe_index = -1):
        x,y = self.position[poe_index]
        self.cam.position_control(x, y, self.height)

    def camera_track_middle(self):
        p = call_middle_point(self.position[0],self.position[-1])
        self.cam.position_control(p.x, p.y, self.height)

    def is_slight_shaking(self, distance = 0.05):
        if len(self.position) == len(self.past_position):
            for now, past in zip(self.position,self.past_position):
                if comput_distance(now, past) < distance:
                    return True
        return False

    def add_number(self, add=1):
        self.number[0] = self.number[0] + add
    def reset_number(self):
        self.number[2] = self.number[1]
        self.number[1] = self.number[0]
        self.number[0] = 0
        self.position = []
        self.past_position = self.position[:]
    def add_position(self, point):
        self.number[0] = self.number[0] + 1
        self.position.append(point)
    def draw(self, color):
        pd.draw_points(self.position,color)
    def check_person(self):
        a,b,c = self.number
        if a == b and a == c:
            return True
        return False

def check_identity(point, classroom):
    if classroom.is_teacher(point):
        return Identity.teacher
    if classroom.is_student(point):
        return Identity.student
