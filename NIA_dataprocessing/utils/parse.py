import math
import numpy as np
import gc

angle_radian = angle / 180 * math.pi
angle_radian = np.transpose(np.array([angle_radian]))
cos_angle_radian = np.cos(angle_radian)
sin_angle_radian = np.sin(angle_radian)
Azimuth = np.zeros(24)
distance = np.zeros((16, 24))
intensity = np.zeros((16, 24))
pos_intens = np.zeros((16, 24, 4)) #distance에서 계산되어 return 될 값
append_data =np.empty((1, 4), dtype=float)
COUNT_THRESH = 150

def cal_lidar_pos():
    Azimuth_radian = Azimuth * np.pi / 180
    dist_cos_angle_radian = distance * cos_angle_radian
    x_ = dist_cos_angle_radian * np.sin(Azimuth_radian)
    y_ = dist_cos_angle_radian * np.cos(Azimuth_radian)
    z_ = distance * sin_angle_radian
    return(np.stack([x_, y_, z_, intensity], axis=-1).reshape(-1, 4))

def clear_append_data(): # point cloud를 한번 plot한 뒤에 전역변수를 한번 삭제해주기 위해
    global append_data
    append_data = np.empty((1, 4), dtype=float)
    gc.collect()

def parse_pos(array, count):
    global append_data, append_azimuth
    add = 0
    for block in range(0, 24, 2):
        Azimuth[block] = (array[3 + add] * 256 + array[2 + add]) * 0.01 # array[0] array[1]은 0xFFEE flag
        if (Azimuth[block + 1] < 359.9): # 360 or bigger Azimuth is error.
            Azimuth[block + 1] = Azimuth[block] + 0.1
        else:
            Azimuth[block + 1] = Azimuth[block] - 359.9
        for Double in range(2):
            for channel in range(16):
                if channel > -1:
                    distance[channel][block + Double] = (array[5 + add] * 256 + array[4 + add]) * 0.002
                    intensity[channel][block + Double] = array[6 + add]
                else:
                    distance[channel][block + Double] = 0
                    intensity[channel][block + Double] = 0
                add += 3
        add += 4
    append_data = np.append(append_data, cal_lidar_pos(), axis=0)
    if count > COUNT_THRESH:
        append_data = np.delete(append_data, 0, axis=0)
        return (1, append_data)
    return (0, 0)
