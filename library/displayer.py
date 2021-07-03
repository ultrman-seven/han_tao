import serial
from enum import Enum

class Scene(Enum):
    teacher_all = 1
    student_all = 2
    teacher_feature = 3
    student_feature = 4

class Displayer():
    def __init__(self, name):
        self.current_display = None
        try:
            portx = name
            bps = 9600
            timex = 5
            self.ser = serial.Serial(portx, bps, timeout=timex)
            return True
        except Exception as e:
            print("can't open port " + name,e)
            return False
        
    def write(self, data):
        return self.ser.write(bytearray(data))
