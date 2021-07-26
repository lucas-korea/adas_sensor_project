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

def parse_pos(array, count):
    global append_data, append_azimuth
    add = 0
    for block in range(0, 24, 2):
        Azimuth[block] = (array[3 + add] * 256 + array[2 + add]) * 0.01

        if (Azimuth[block + 1] < 360): # 360 or bigger Azimuth is error.
            Azimuth[block + 1] = Azimuth[block] + 0.1
        else:
            Azimuth[block + 1] = Azimuth[block] - 359.9
        for channel in range(16):
            for Double in range(2):
                distance[channel][block + Double] = (array[5 + add] * 256 + array[4 + add]) * 0.002
                intensity[channel][block + Double] = array[6 + add]
                add += 3
        add += 4
    append_data = np.append(append_data, cal_lidar_pos(), axis=0)
    if count > COUNT_THRESH:
        append_data = np.delete(append_data, 0, axis=0)
        return (1, append_data)
    return (0, 0)

## lagacy function

# def draw_PCL(ax, point_cloud):
#     # global point_cloud
#     # while True:
#     plt.cla()
#     # 느리지만 옵션을 다양하게 줄 수 있는 함수
#     # ax.scatter(point_cloud[:, 0], point_cloud[:, 1], point_cloud[:, 2], c=color_arr.colors, s=point_cloud[:, 3]/255)
#     # 빠르지만 시각화 옵션이 별로 없는 함수
#     ax.plot(point_cloud[:, 0], point_cloud[:, 1], point_cloud[:, 2], 'r.')
#
#     ax.set_xlim(-5, 5)
#     ax.set_ylim(-5, 5)
#     ax.set_zlim(-5, 5)
#     plt.pause(0.001)  # 이게 자꾸 각도 중간이 skip되는 원인(이지 않을까?)
#     parse.clear_append_data()