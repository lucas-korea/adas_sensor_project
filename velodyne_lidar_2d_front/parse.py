import math
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pyplot as plt

angle = np.array([-15, 1, -13, -3 ,-11, 5, -9, 7, -7, 9, -5, 11, -3, 13, -1, 15])
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
MIN_DEG = 150
MAX_DEG = 210

def cal_lidar_pos():
    Azimuth_radian = Azimuth * np.pi / 180
    dist_cos_angle_radian = distance * cos_angle_radian
    x_ = dist_cos_angle_radian * np.sin(Azimuth_radian)
    y_ = dist_cos_angle_radian * np.cos(Azimuth_radian)
    z_ = distance * sin_angle_radian
    return((np.swapaxes(np.stack([x_, y_, z_, intensity], axis=-1), 0, 1)).reshape(-1, 4))

def clear_append_data():
    global append_data
    append_data = np.empty((1, 4), dtype=float)

def parse_330to30(Azi_arr):
    start = 0
    end_trigger = 0
    result = np.zeros(384, dtype=int)
    Azi_MIN = np.min(Azi_arr)
    if Azi_MIN > MIN_DEG and Azi_MIN < MAX_DEG:
        start = 1
    elif Azi_MIN >= MAX_DEG-1.20 and Azi_MIN < MAX_DEG+1.20:
        end_trigger = 1

    if start:
        for k in range(24):
            for q in range(16):
                result[k*16 + q] = 1
    return result, end_trigger

global append_azimuth
append_azimuth = np.empty((1,1), dtype=float)
def parse_pos(array, count):
    global append_data, append_azimuth

    add = 0
    for block in range(0, 24, 2):
        Azimuth[block] = (array[3 + add] * 256 + array[2 + add]) * 0.01
        Azimuth[block + 1] = Azimuth[block] + 0.1
        for channel in range(16):
            for Double in range(2):
                distance[channel][block + Double] = (array[5 + add] * 256 + array[4 + add]) * 0.002
                intensity[channel][block + Double] = array[6 + add]
                add += 3
        add += 4

    degree_flag, end_flag = parse_330to30(Azimuth)
    # print(Azimuth)
    # print(degree_flag)
    # print(cal_lidar_pos())
    # print(cal_lidar_pos()[degree_flag, :])
    append_data = np.append(append_data, cal_lidar_pos(), axis=0)
    append_azimuth = np.append(append_azimuth, Azimuth)
    # print("degree_flag")
    # print(degree_flag)
    # print("cal_lidar_pos[degree_flag]")
    # print(cal_lidar_pos()[degree_flag, :])
    # print("raw cal_lidar_pos")
    # print(cal_lidar_pos())
    # print(degree_flag.shape, cal_lidar_pos().shape, cal_lidar_pos()[degree_flag, :].shape)
    # print("\n\n")

    # if end_flag:
    if count > COUNT_THRESH:
        # print("here")
        np.savetxt("append_azimuth.txt", append_azimuth, fmt="%1.2f")
        append_data = np.delete(append_data, 0, axis=0)

        return (1, append_data)
    return (0, 0)