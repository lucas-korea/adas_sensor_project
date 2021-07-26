#!/usr/bin/env python
import socket
import parse
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pyplot as plt
import color_arr ## 시각화를 위한 색깔 arr
import time

def main():
    ## UDP setting
    IP_ADDRESS = "192.168.1.77"
    PORT_NO = 2368
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serverSocket.bind((IP_ADDRESS, PORT_NO))
    count = 0

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    print("start")
    time_1 = time.time()
    # while True: ## 실시간 관찰
    for i in range(20): ## 짧은 시간만 관찰하거나 딱 한번만 찍고 정지시키고 싶을 때
    # ==============================================================
        while True:
            ## 라이다 데이터 패킷을 메뉴얼에 따라 파싱하여 리턴하는 함수
            count += 1
            get_data, point_cloud = parse.parse_pos(serverSocket.recv(1206), count)
            if (get_data):
                count = 0
                break
        plt.cla()
        # 느리지만 옵션을 다양하게 줄 수 있는 함수
        # ax.scatter(point_cloud[:, 0], point_cloud[:, 1], point_cloud[:, 2], c=color_arr.colors, s=point_cloud[:, 3]/255)
        # 빠르지만 시각화 옵션이 별로 없는 함수
        ax.plot(point_cloud[:, 0], point_cloud[:, 1], point_cloud[:, 2], 'r.')
        ax.set_xlim(-5, 5)
        ax.set_ylim(-5, 5)
        ax.set_zlim(-5, 5)
        time_2 = time.time()
        ax.text(-15, 0, 7, 'FPS:'+str(round(1/(time_2-time_1), 2)))
        time_1 = time.time()
        plt.pause(0.001)
        parse.clear_append_data()
    plt.show() ## 실시간에서는 없어도 됨
if __name__ == "__main__":
    main()