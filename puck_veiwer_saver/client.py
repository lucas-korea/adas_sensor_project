import socket
from matplotlib import pyplot as plt
import numpy as np
import color_arr
import time
import gc

DATA_RECV_BYTES = 1855488
LIDAR_DATA_SHAPE = (57984, 4)

def rm_zero_point(point_cloud): ## xyz가 전부 0이거나 Intensity = 0인 경우를 삭제
    mask_array1 = point_cloud[:, 0] == 0
    mask_array2 = point_cloud[:, 1] == 0
    mask_array3 = point_cloud[:, 2] == 0
    mask_array4 = point_cloud[:, 3] == 0
    mask_all = np.logical_and(mask_array1, mask_array2)
    mask_all = np.logical_and(mask_all, mask_array3)
    mask_all = np.logical_or(mask_all, mask_array4)
    point_cloud = point_cloud[~mask_all]
    return point_cloud

def rm_minus_data_and_3dto2d(point_cloud, axis=1): ## y < 0인 데이터를 없애고, y축 값을 없애 정면 시점을 구현 (but 부자연스럽)
    return np.delete(point_cloud[point_cloud[:, 1] > 0], axis, axis=1)

def rm_minus_data(point_cloud, axis=1):
    return np.delete(point_cloud, axis, axis=1)

def put_roi(point_cloud):
    xlim = (-2, 2)
    ylim = (-4, 4)
    mask_arr1 = point_cloud[:, 0] > xlim[0]
    mask_arr2 = point_cloud[:, 0] < xlim[1]
    mask_arr3 = point_cloud[:, 1] > ylim[0]
    mask_arr4 = point_cloud[:, 1] < ylim[1]
    mask_x = np.logical_and(mask_arr1, mask_arr2)
    mask_y = np.logical_and(mask_arr3, mask_arr4)
    mask_all = np.logical_and(mask_x, mask_y)
    point_cloud = point_cloud[mask_all]
    return point_cloud, xlim, ylim

def trim_60degree(point_cloud):
    mask_positive_x = point_cloud[:, 0] >= 0
    mask_negative_x = point_cloud[:, 0] < 0
    mask_right_y = (point_cloud[:, 1] > point_cloud[:, 0] * 1.732)
    mask_left_y = point_cloud[:, 1] > point_cloud[:, 0] * -1.732
    mask_right = np.logical_and(mask_positive_x, mask_right_y)
    mask_left = np.logical_and(mask_negative_x, mask_left_y)
    mask_all = np.logical_or(mask_left, mask_right)
    return point_cloud[mask_all]

# np.set_printoptions(threshold=np.nan)
def pcl_spherical_cord(point_cloud):
    ptsnew = np.hstack((point_cloud, np.zeros(point_cloud.shape)))
    xy = point_cloud[:,0]**2 + point_cloud[:,1]**2
    ptsnew[:, 4] = np.sqrt(xy + point_cloud[:, 2] ** 2) # radious
    ptsnew[:, 5] = np.arctan2(point_cloud[:, 2], np.sqrt(xy))  # for elevation angle defined from Z-axis down
    ptsnew[:, 6] = np.arctan2(point_cloud[:, 0], point_cloud[:, 1]) #xy plane theta
    ptsnew[:, 0] = np.tan(ptsnew[:, 6])
    ptsnew[:, 1] = np.tan(ptsnew[:, 5])
    return ptsnew

def pcl_cylinder_cord(point_cloud):
    ptsnew = np.zeros(point_cloud.shape)
    xy = point_cloud[:,0]**2 + point_cloud[:,1]**2
    ptsnew[:, 6] = np.arctan2(point_cloud[:, 0], point_cloud[:, 1]) #xy plane theta
    ptsnew[:, 0] = np.tan(ptsnew[:, 6])
    ptsnew[:, 1] = point_cloud[:, 2]
    return ptsnew

xyz_lim = 10
def view_pcl(client, time1):
    fig = plt.figure()
    plt.style.use(['dark_background'])
    ax = fig.add_subplot(111, projection='3d')
    while True:
    # for i in range(2):
        plt.cla()
        point_cloud = rm_zero_point(np.reshape(np.frombuffer(client.recv(DATA_RECV_BYTES), dtype=np.float64), LIDAR_DATA_SHAPE))
        # 느리지만 옵션을 다양하게 줄 수 있는 함수
        # ax.scatter(point_cloud[:, 0], point_cloud[:, 1], point_cloud[:, 2], s=0.2, c=color_arr.intensity_color(point_cloud))
        # 빠르지만 시각화 옵션이 별로 없는 함수
        ax.plot(point_cloud[:, 0], point_cloud[:, 1], point_cloud[:, 2], 'b.')
        ax.set_xlim(-xyz_lim, xyz_lim)
        ax.set_ylim(-xyz_lim, xyz_lim)
        ax.set_zlim(-xyz_lim, xyz_lim)
        # ax.set_xlabel('$X$', fontsize=20, rotation=150)
        # ax.set_ylabel('$Y$')
        # ax.set_zlabel(r'$\gamma$', fontsize=30, rotation=60)
        time2 = time.time()
        ax.text(-10, 0, 7, 'FPS:' + str(round(1 / (time2 - time1), 2)))
        time1 = time.time()
        plt.axis('off')
        plt.pause(0.001)
        gc.collect()
    plt.show()

def view_image(client, time1):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    while True:
        plt.cla()
        point_cloud = rm_zero_point(np.reshape(np.frombuffer(client.recv(DATA_RECV_BYTES), dtype=np.float64), LIDAR_DATA_SHAPE))

        # point_cloud = rm_minus_data_and_3dto2d(point_cloud, axis=1)

        # 2d front view =========================================================
        point_cloud = trim_60degree(point_cloud)
        point_cloud = pcl_spherical_cord(point_cloud)
        ax.scatter(point_cloud[:, 0], point_cloud[:, 1], s=0.2, c=color_arr.distance_color(point_cloud[:, 4], max_dist=10))
        # =========================================================================

        # 느리지만 옵션을 다양하게 줄 수 있는 함수
        # ax.scatter(point_cloud[:, 0], point_cloud[:, 1], s=0.2)
        # 빠르지만 시각화 옵션이 별로 없는 함수
        # ax.plot(point_cloud[:, 0], point_cloud[:, 1], 'r.')
        ax.set_xlim(-1, 1)
        ax.set_ylim(-.4, .4)
        # ax.set_xlim(-.6, .6)
        # ax.set_ylim(-.6, .6)
        time2 = time.time()
        ax.text(1, 3, 'FPS:' + str(round(1 / (time2 - time1), 2)))
        time1 = time.time()
        plt.pause(0.001)

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    LOCALHOST = "127.0.0.1"
    PORT_NO = 999
    client.connect((LOCALHOST, PORT_NO))
    print("conecte success\n")

    time1 = time.time()
    # view_pcl(client, time1)
    view_image(client, time1)
if __name__ == "__main__":
    main()