import socket
from matplotlib import pyplot as plt
import numpy as np
import color_arr
import time

DATA_RECV_BYTES = 1855488
LIDAR_DATA_SHAPE = (57984, 4)

xyz_lim = 15
def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    LOCALHOST = "127.0.0.1"
    PORT_NO = 999
    client.connect((LOCALHOST, PORT_NO))
    print("conecte success\n")

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    time1 = time.time()
    while True:
        # buffer =
        point_cloud = np.frombuffer(client.recv(DATA_RECV_BYTES), dtype=np.float64)
        point_cloud = np.reshape(point_cloud, LIDAR_DATA_SHAPE)
        plt.cla()
        # 느리지만 옵션을 다양하게 줄 수 있는 함수
        ax.scatter(point_cloud[:, 0], point_cloud[:, 1], point_cloud[:, 2], s=point_cloud[:, 3]/255, c=color_arr.colors)
        # 빠르지만 시각화 옵션이 별로 없는 함수
        # ax.plot(point_cloud[:, 0], point_cloud[:, 1], point_cloud[:, 2], 'r.')
        ax.set_xlim(-xyz_lim, xyz_lim)
        ax.set_ylim(-xyz_lim, xyz_lim)
        ax.set_zlim(-xyz_lim, xyz_lim)
        time2 = time.time()
        ax.text(-10, 0, 7, 'FPS:' + str(round(1 / (time2 - time1), 2)))
        time1 = time.time()
        plt.pause(0.001)
if __name__ == "__main__":
    main()