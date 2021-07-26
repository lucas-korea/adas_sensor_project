#!/usr/bin/env python
import socket
import parse
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pyplot as plt
import color_arr ## 시각화를 위한 색깔 arr
import time


def main():
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    print("start")
    time_1 = time.time()
    count = 0
    # while True: ## 실시간 관찰
    for i in range(1): ## 짧은 시간만 관찰하거나 딱 한번만 찍고 정지시키고 싶을 때

        point_cloud = np.loadtxt("test0.txt")
        print(point_cloud.shape)
        # 느리지만 옵션을 다양하게 줄 수 있는 함수
        # ax.scatter(point_cloud[:, 0], point_cloud[:, 1], point_cloud[:, 2], c=color_arr.colors, s=point_cloud[:, 3]/255)
        # 빠르지만 시각화 옵션이 별로 없는 함수
        ax.plot(point_cloud[:, 0], point_cloud[:, 1], point_cloud[:, 2], 'r.')

        ax.set_xlim(-5, 5)
        ax.set_ylim(-5, 5)
        ax.set_zlim(-5, 5)
        plt.show() ## 실시간에서는 없어도 됨
if __name__ == "__main__":
    main()