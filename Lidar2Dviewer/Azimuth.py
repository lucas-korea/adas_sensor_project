import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
import cv2
import pickle

# list = {"beam_altitude_angles": [10.16, 10.01, 9.82, 9.68, 9.51, 9.32, 9.17, 9.01, 8.84, 8.66, 8.5, 8.33, 8.15, 7.98, 7.81, 7.66, 7.47, 7.32, 7.14, 6.96, 6.8, 6.63, 6.46, 6.29, 6.12, 5.94, 5.76, 5.61, 5.43, 5.26, 5.09, 4.91, 4.72, 4.58, 4.4, 4.23, 4.04, 3.87, 3.7, 3.53, 3.36, 3.19, 3.02, 2.83, 2.66, 2.49, 2.32, 2.15, 1.97, 1.8, 1.65, 1.46, 1.3, 1.12, 0.95, 0.78, 0.6, 0.41, 0.26, 0.08, -0.08, -0.26, -0.44, -0.61, -0.79, -0.95, -1.13, -1.32, -1.47, -1.66, -1.83, -2, -2.17, -2.34, -2.51, -2.7, -2.87, -3.03, -3.2, -3.38, -3.55, -3.72, -3.89, -4.07, -4.23, -4.41, -4.58, -4.76, -4.93, -5.1, -5.25, -5.44, -5.61, -5.8, -5.96, -6.14, -6.3, -6.47, -6.64, -6.82, -6.98, -7.16, -7.32, -7.5, -7.66, -7.84, -8.01, -8.17, -8.34, -8.49, -8.66, -8.85, -9.02, -9.18, -9.359999999999999, -9.539999999999999, -9.69, -9.84, -10.02, -10.2, -10.36, -10.52, -10.68, -10.85, -11.01, -11.19, -11.34, -11.51],
#         "beam_azimuth_angles": [2.05, 0.6899999999999999, -0.6899999999999999, -2.04, 2.06, 0.68, -0.68, -2.04, 2.05, 0.67, -0.68, -2.06, 2.04, 0.68, -0.6899999999999999, -2.04, 2.04, 0.7, -0.68, -2.05, 2.05, 0.68, -0.6899999999999999, -2.05, 2.05, 0.68, -0.6899999999999999, -2.05, 2.05, 0.6899999999999999, -0.68, -2.03, 2.04, 0.6899999999999999, -0.6899999999999999, -2.04, 2.05, 0.68, -0.6899999999999999, -2.05, 2.05, 0.6899999999999999, -0.68, -2.05, 2.05, 0.68, -0.68, -2.04, 2.04, 0.68, -0.67, -2.05, 2.03, 0.68, -0.68, -2.04, 2.05, 0.68, -0.67, -2.05, 2.06, 0.68, -0.67, -2.04, 2.04, 0.6899999999999999, -0.67, -2.05, 2.06, 0.68, -0.6899999999999999, -2.05, 2.05, 0.6899999999999999, -0.68, -2.05, 2.05, 0.6899999999999999, -0.67, -2.05, 2.05, 0.6899999999999999, -0.68, -2.04, 2.05, 0.68, -0.6899999999999999, -2.04, 2.05, 0.68, -0.67, -2.05, 2.06, 0.67, -0.68, -2.05, 2.04, 0.68, -0.68, -2.05, 2.06, 0.68, -0.67, -2.05, 2.04, 0.6899999999999999, -0.6899999999999999, -2.05, 2.05, 0.7, -0.68, -2.05, 2.05, 0.67, -0.68, -2.06, 2.05, 0.6899999999999999, -0.67, -2.05, 2.05, 0.6899999999999999, -0.68, -2.03, 2.05, 0.68, -0.68, -2.04],
#         "lidar_origin_to_beam_origin_mm": 13.762}
#
# print(list["beam_azimuth_angles"])
# print(len(list["beam_azimuth_angles"]))
# for i in range(len(list["beam_azimuth_angles"])):
#     if i % 4 == 0:
#         print();
#     print(list["beam_azimuth_angles"][i], end='')

if __name__ == '__main__':
    data = pd.read_csv("H:\\라이다 지그 장착 시 데이터 양상\\기둥 뗀거.csv")
    VerticalAngle = []
    for i in range(len(data)):
        if i % 5000 == 0:
            print(i / len(data))
        try:
            VerticalAngle.append(math.atan(data.iloc[i]['Point:2'] /(math.sqrt(pow(data.iloc[i]["Point:0"], 2) + pow(data.iloc[i]["Point:1"], 2)))) * 180 / math.pi)
        except:
            pass

    VerticalAngle = [x for x in VerticalAngle if math.isnan(x) == False]
    for i in range(len(VerticalAngle)):
        VerticalAngle[i] = round(VerticalAngle[i], 3)
    VerticalAngle = list(set(VerticalAngle))
    print(len(VerticalAngle))
    VerticalAngle.sort()
    print(VerticalAngle)
# if __name__ == '__main__':
#     # exit(1)
#     with open("azimuthlist.pickle", "rb") as fw:
#         azimuthlist = pickle.load(fw)
#
#
#     azimuthlist = [x for x in azimuthlist if math.isnan(x) == False]
#     for i in range(len(azimuthlist)):
#         azimuthlist[i] = round(azimuthlist[i], 2)
#     azimuthlist = list(set(azimuthlist))
#     print(len(azimuthlist))
#     azimuthlist.sort()
#     print(azimuthlist)
