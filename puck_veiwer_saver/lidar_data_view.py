#!/usr/bin/env python
import socket
import math
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pyplot as plt
import time
import csv

def cal_lidar_pos(Azimuth_, distance_, angle_):
    x_ = distance_ * math.sin(Azimuth_ / 360 * 2 * math.pi) * math.cos(angle_ / 360 * 2 * math.pi)
    y_ = distance_ * math.cos(Azimuth_ / 360 * 2 * math.pi) * math.cos(angle_ / 360 * 2 * math.pi)
    z_ = distance_ * math.sin(angle_ / 360 * 2 * math.pi)
    return(x_, y_, z_)

def main():
    IP_ADDRESS = "192.168.1.77"
    PORT_NO = 2368
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serverSocket.bind((IP_ADDRESS, PORT_NO))
    array = [None]*64;
    vertical_angle = [-15, 1, -13, -3 ,-11, 5, -9, 7, -7, 9, -5, 11, -3, 13, -1, 15]

    # # while True:
    # for i in range(10):
    #     array = serverSocket.recv(1206)
    #     add = 0
    #     for block in range(12):
    #         Azimuth = (array[3 + add] * 256 + array[2 + add]) * 0.01
    #         # print("data block :", block, "$$Azimuth :", Azimuth)
    #         for double_ in range(2):
    #             for channel in range (16):
    #                 angle = vertical_angle[channel]
    #                 distance = round((array[5 + add] * 256 + array[4 + add]) * 0.002, 3)
    #                 intensity = array[6 + add]
    #                 # print("$$channel {} angle{} $$distance : {} $$intensity : {}".format(channel, vertical_angle[channel], distance, intensity))
    #                 # x, y, z = cal_lidar_pos(Azimuth, distance, angle)
    #                 plt.pause(0.000001)
    #                 add += 3
    #         add += 4

    fig = plt.figure(1)
    ax = fig.add_subplot(111, projection='3d')
    data = []
    start_time = time.time()
    # while True:
    for i in range(600):
        array = serverSocket.recv(1206)
        add = 0
        for block in range(12):
            Azimuth = (array[3 + add] * 256 + array[2 + add]) * 0.01
            data.append(Azimuth)
            # print("data block :", block, "$$Azimuth :", Azimuth)
            for channel in range(16):
                for Double in range(2):
                    angle = vertical_angle[channel]
                    distance = round((array[5 + add] * 256 + array[4 + add]) * 0.002, 3)
                    intensity = array[6 + add]
                    # print("$$c?hannel {} angle{} $$distance : {} $$intensity : {}".format(channel, vertical_angle[channel], distance, intensity))
                    cal_lidar_pos(Azimuth, distance, angle)
                    add += 3
            add += 4
        # plt.pause(0.01)
    print(time.time() - start_time)
    plt.figure(2)
    plt.plot(np.transpose(data), range(len(data)))
    plt.show()
if __name__ == "__main__":
    main()