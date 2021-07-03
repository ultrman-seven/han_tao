import socket
from math import sin, cos, pi

IP = '192.168.1.125'
PORT = 2368
SCAN_TIMES = 120

server_cocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
address = (IP, PORT)
server_cocket.bind(address)
server_cocket.settimeout(10)

#接收原始数据
def __get_lidar_data():
    try:
        receive_data, client = server_cocket.recvfrom(1200)      
        return receive_data.hex()
    except socket.timeout:  #如果10秒钟没有接收数据进行提示（打印 "time out"）
        print("tme out")

#直接返回点云
def get_points():
    x=[]
    y=[]
    ls_data = []
    for i in range(SCAN_TIMES):
        ls_data.append(__get_lidar_data().split('ffee')[1:])
    last_dis = None
    last_ang = None
    for data in ls_data:        
        for dat in data:
            #4+ 4+4+2+90+4+2+90
            angle1 = int(dat[2:4]+dat[0:2],16) / 100
            distance1 = int(dat[6:8]+dat[4:6],16) / 500
            last_dis = int(dat[102:104]+dat[100:102],16) / 500
            if last_ang != None:
                angle2 = (angle1+last_ang)/2
                x.append(last_dis * cos(angle2 * pi / 180))
                y.append(last_dis * sin(angle2 * pi / 180))
            x.append(distance1 * cos(angle1 * pi / 180))
            y.append(distance1 * sin(angle1 * pi / 180))
            last_ang = angle1
    return [x, y]

def __get_sorted_data():
    ls_data = []
    for i in range(SCAN_TIMES):
        ls_data.append(__get_lidar_data().split('ffee')[1:])
    point_data = {}
    last_dis = None
    last_ang = None
    for data in ls_data:        
        for dat in data:
            #4+ 4+4+2+90+4+2+90
            angle1 = int(dat[2:4]+dat[0:2],16) / 100
            distance1 = int(dat[6:8]+dat[4:6],16) / 500
            last_dis = int(dat[102:104]+dat[100:102],16) / 500
            if last_ang != None:
                angle2 = (angle1+last_ang)/2
                point_data[angle2] = last_dis
            point_data[angle1] = distance1
            last_ang = angle1
    point_data = list(point_data.items())
    point_data = sorted(point_data,key=lambda x:x[0])
    return point_data

#返回排序后的点云
def get_sort_points():
    ls_data = []
    for i in range(SCAN_TIMES):
        ls_data.append(__get_lidar_data().split('ffee')[1:])
    point_data = {}
    last_dis = None
    last_ang = None
    for data in ls_data:        
        for dat in data:
            #4+ 4+4+2+90+4+2+90
            angle1 = int(dat[2:4]+dat[0:2],16) / 100
            distance1 = int(dat[6:8]+dat[4:6],16) / 500
            last_dis = int(dat[102:104]+dat[100:102],16) / 500
            if last_ang != None:
                angle2 = (angle1+last_ang)/2
                point_data[angle2] = last_dis
            point_data[angle1] = distance1
            last_ang = angle1
    point_data = list(point_data.items())
    x, y = [],[]
    for angle, distance in sorted(point_data,key=lambda x:x[0]):
        x.append(distance * cos(angle * pi / 180))
        y.append(distance * sin(angle * pi / 180))
    return [x,y]

#一阶低通滤波
def get_firstOrder_lowPass_filter_points(a_th=0.4,a_rh=0.4):
    point_data = __get_sorted_data()
    x, y = [],[]
    for i in len(point_data):
        theta, rh = point_data[i]
        theta_last, rh_last = point_data[i-1]
        theta = a_th*theta + (1-a_th)*theta_last
        rh = a_rh*rh + (1-a_rh)*rh_last
        x.append(rh * cos(theta * pi / 180))
        y.append(rh * sin(theta * pi / 180))
    return [x,y]


#半径滤波
def get_radius_filter_points():
    pass

#统计滤波
def statistical_filter_points(lenth = 0.05,total = 10 ,effective = 5):
    point_data = __get_sorted_data()
    for i in range(point_data):
        pass


    

#体素滤波
def voxel_filtering_point(polar = False):
    voxel = [[0,0] for _ in range(1440)]
    ls_data = []
    for i in range(SCAN_TIMES):
        ls_data.append(__get_lidar_data().split('ffee')[1:])
    last_dis = None
    last_ang = None
    for data in ls_data:        
        for dat in data:
            #4+ 4+4+2+90+4+2+90
            angle1 = int(dat[2:4]+dat[0:2],16) / 100
            distance1 = int(dat[6:8]+dat[4:6],16) / 500
            last_dis = int(dat[102:104]+dat[100:102],16) / 500
            if last_ang != None:
                angle2 = (angle1+last_ang)/2
                voxel[int(4*angle2)][0] += last_dis
                voxel[int(4*angle2)][1] += 1

            voxel[int(4*angle1)][0] += distance1
            voxel[int(4*angle1)][1] += 1
            last_ang = angle1

    if polar:
        if voxel[0][1] == 0:
            voxel[0][1] +=1
        points=[]
        for sum, n in voxel:
            if n != 0:
                points.append(sum/n)
            else:
                points.append(points[-1])
        return points
    else:
        x,y = [],[]
        for i in len(voxel):
            sum,n = voxel[i]
            ang = i/4
            if n != 0:
                dis = sum/n
                x.append(dis * cos(ang * pi / 180))
                y.append(dis * sin(ang * pi / 180))
        return [x,y]
