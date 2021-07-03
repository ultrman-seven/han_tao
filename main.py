import library.lslidar as ls
import library.person as ps
import library.point_map as ptmp
import library.displayer as ds
import library.picture_draw as pd
import library.readfile as rf

points_resolution = 0.01
person_width = 0.3
boundary = rf.get_area('area/boundary.txt')
tea_area = rf.get_area('area/teacher.txt')
stu_area = rf.get_area('area/student.txt')
shield = rf.get_shields('area/shield.txt')
classroom = ptmp.Map(boundary, student=stu_area, teacher=tea_area, shields=shield)

stu = ps.Person(ps.Identity.student,1.7)
tea = ps.Person(ps.Identity.teacher,1.5)

stu.camera_init('/dev/ttyUSB0')
tea.camera_init('/dev/ttyUSB1')
dis = ds.Displayer('/dev/ttyUSB2')
pd.pic_start()

while True:
    classroom.draw()
    x, y = ls.get_sort_points()
    #pd.draw_boundray(x,y)
    pd.draw_points([ptmp.Point()])

    points = []
    for x0, y0 in zip(x,y):
        points.append(ptmp.Point(x0, y0))

    people_position = []
    start = points[0]
    end = start

    for i in range(len(points)):
        if not classroom.is_in_map(points[i]):
            if not ptmp.is_equal(start,end):
                start = points.index(start)
                start = points[start+1]
                if ptmp.comput_distance(start,end) > person_width:
                    people_position.append(ptmp.call_middle_point(start,end))
        end = points[i]
        if not classroom.is_in_map(points[i]):
            start = end

    for person_p in people_position:#判断是学生还是老师
        id = ps.check_identity(person_p,classroom)
        if id == ps.Identity.student:
            stu.add_position(person_p)
        if id == ps.Identity.teacher:
            tea.add_position(person_p)

    if stu.check_person() and tea.check_person():#三次扫描人数相等
        stu.draw('r')
        tea.draw('b')
        print('stu=',stu.number[0])
        print('tea=',tea.number[0],'\n')
        if not stu.is_slight_shaking():
            stu.camera_track_person()
        if not tea.is_slight_shaking():
            tea.camera_track_person()

    stu.reset_number()
    tea.reset_number()

    pd.pic_show()
