import os
import struct
from matplotlib import pyplot as plt
import gc
import numpy as np
import sys
import math

global ExtrinsicMat
ExtrinsicMat = np.array([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]], dtype=np.float64)
def parsing_binPCD2asciiPCD(PCD, type_list, count_list):
    start = 0
    lines = [[]]

    pack_str = ""
    format_str = ""
    byte_len = 0
    type_list[-1] = type_list[-1].replace('\n', '')
    type_list[-1] = type_list[-1].replace('\r', '')
    for i in range(len(type_list)):
        if (type_list[i] == "F"):
            for j in range(int(count_list[i])):
                pack_str = pack_str + "f"
                format_str = format_str + "{:.6f} "
                byte_len = byte_len + 4
        elif (type_list[i] == "U"):
            for j in range(int(count_list[i])):
                pack_str = pack_str + "B"
                format_str = format_str + "{} "
                byte_len = byte_len + 1
    line_i = 0
    format_str = format_str.split(" ")
    while (1):
        try:
            scalar_fileds = struct.unpack(pack_str, PCD[start: start + byte_len])  # B:부호없는 정수, c:문자
            for i in range(len(type_list)):
                lines[line_i] = str(lines[line_i]) + " " + format_str[i].format(scalar_fileds[i])
            lines.append("")
            if line_i == 0:
                lines[line_i] = lines[line_i][3:]
            else :
                lines[line_i] = lines[line_i][1:]
            start = start + byte_len
            line_i = line_i + 1
        except Exception as e:
            break
    return lines

def binPCD2asciiPCD(file_name): # args가 없으면 코드가 위치한 디렉토리에서 검색,변환
    Origin_pcd_f = open(file_name, 'rb')
    header = []
    field_list = []
    size_list = []
    type_list = []
    count_list = []

    line = Origin_pcd_f.readline().decode()
    line = line.replace("\r", "")
    line = line.replace("\n", "")
    header.append(line+'\n')
    while line:
        line = Origin_pcd_f.readline().decode()
        line = line.replace("\r", "")
        line = line.replace("\n", "")
        words = line.split(' ')
        if words[0] == "DATA":
            if words[1] != "binary":
                print("skip {} cause it is not bin type".format(file_name))
                break
            header.append("DATA ascii\n")
            break
        elif words[0] == "FIELDS":
            for j in range(len(words)-1):
                field_list.append(words[j+1])
        elif words[0] == "SIZE":
            for j in range(len(words)-1):
                size_list.append(words[j+1])
        elif words[0] == "TYPE":
            for j in range(len(words)-1):
                type_list.append(words[j+1])
        elif words[0] == "COUNT":
            for j in range(len(words)-1):
                count_list.append(words[j+1])
        header.append(line+'\n')

    PCD_data_part = Origin_pcd_f.read() # 헤더까지 다 읽은 기록이 있기 때문에, 나머지를 다 읽으면 PCD 데이터 부분이다.
    lines = parsing_binPCD2asciiPCD(PCD_data_part, type_list, count_list)
    Origin_pcd_f.close()
    return lines

xyz_lim = 10
fig = plt.figure()
plt.style.use(['dark_background'])
ax = fig.add_subplot(111, projection='3d')
plt.cla()

ax.plot([0],[0],[0], 'b.', alpha = 0.2)
ax.set_xlim(-xyz_lim, xyz_lim)
ax.set_ylim(-xyz_lim, xyz_lim)
ax.set_zlim(-xyz_lim, xyz_lim)

plt.axis('off')
plt.pause(0.001)
gc.collect()
global MicroMode
MicroMode = 0
def key_press(event):
    global PointCloud, PointCloudOrigin, ExtrinsicMat, MicroMode
    new_xyz_lim = [plt.xlim(), plt.ylim()]
    new_ExtrinsicMat = np.array([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]], dtype=np.float64)
    sys.stdout.flush()
    deg_del = 0.01
    pos_del = 0.1
    if MicroMode:
        deg_del *= 0.1
        pos_del *= 0.1
    if event.key == 'a':
        PointCloud[:, 0] = PointCloud[:, 0] - pos_del
        new_ExtrinsicMat[0][3] -= pos_del
    elif event.key == 'd':
        PointCloud[:, 0] = PointCloud[:, 0] + pos_del
        new_ExtrinsicMat[0][3] += pos_del
    elif event.key == 'w':
        PointCloud[:, 1] = PointCloud[:, 1] - pos_del
        new_ExtrinsicMat[1][3] -= pos_del
    elif event.key == 'x':
        PointCloud[:, 1] = PointCloud[:, 1] + pos_del
        new_ExtrinsicMat[1][3] += pos_del
    elif event.key == 'v':
        PointCloud[:, 2] = PointCloud[:, 2] - pos_del
        new_ExtrinsicMat[2][3] -= pos_del
    elif event.key == 'b':
        PointCloud[:, 2] = PointCloud[:, 2] + pos_del
        new_ExtrinsicMat[2][3] += pos_del


    ## z축 기준 변환
    elif event.key == 'y':
        PointCloud[:, 0] = PointCloud[:, 0] * math.cos(deg_del) - PointCloud[:, 1] * math.sin(deg_del)
        PointCloud[:, 1] = PointCloud[:, 0] * math.sin(deg_del) + PointCloud[:, 1] * math.cos(deg_del)
        new_ExtrinsicMat[0][0] = math.cos(deg_del)
        new_ExtrinsicMat[0][1] = -math.sin(deg_del)
        new_ExtrinsicMat[1][0] = math.sin(deg_del)
        new_ExtrinsicMat[1][1] = math.cos(deg_del)
    elif event.key == 'n':
        PointCloud[:, 0] = PointCloud[:, 0] * math.cos(deg_del) + PointCloud[:, 1] * math.sin(deg_del)
        PointCloud[:, 1] = -PointCloud[:, 0] * math.sin(deg_del) + PointCloud[:, 1] * math.cos(deg_del)
        new_ExtrinsicMat[0][0] = math.cos(deg_del)
        new_ExtrinsicMat[0][1] = math.sin(deg_del)
        new_ExtrinsicMat[1][0] = -math.sin(deg_del)
        new_ExtrinsicMat[1][1] = math.cos(deg_del)
    ## y축 기준 변환
    elif event.key == 'u':
        # for i in range(len(PointCloud)):
        PointCloud[:, 0] = PointCloud[:, 2] * math.sin(deg_del) + PointCloud[:, 0] * math.cos(deg_del)
        PointCloud[:, 2] = PointCloud[:, 2] * math.cos(deg_del) - PointCloud[:, 0] * math.sin(deg_del)
        new_ExtrinsicMat[0][0] = math.cos(deg_del)
        new_ExtrinsicMat[0][2] = math.sin(deg_del)
        new_ExtrinsicMat[2][0] = -math.sin(deg_del)
        new_ExtrinsicMat[2][2] = math.cos(deg_del)
    elif event.key == 'j':
        PointCloud[:, 0] = -PointCloud[:, 2] * math.sin(deg_del) + PointCloud[:, 0] * math.cos(deg_del)
        PointCloud[:, 2] = PointCloud[:, 2] * math.cos(deg_del) + PointCloud[:, 0] * math.sin(deg_del)
        new_ExtrinsicMat[0][0] = math.cos(deg_del)
        new_ExtrinsicMat[0][2] = -math.sin(deg_del)
        new_ExtrinsicMat[2][0] = math.sin(deg_del)
        new_ExtrinsicMat[2][2] = math.cos(deg_del)
    ## x축 기준 변환
    elif event.key == 'i':
        PointCloud[:, 1] = PointCloud[:, 1] * math.cos(deg_del) - PointCloud[:, 2] * math.sin(deg_del)
        PointCloud[:, 2] = PointCloud[:, 1] * math.sin(deg_del) + PointCloud[:, 2] * math.cos(deg_del)
        new_ExtrinsicMat[1][1] = math.cos(deg_del)
        new_ExtrinsicMat[1][2] = -math.sin(deg_del)
        new_ExtrinsicMat[2][1] = math.sin(deg_del)
        new_ExtrinsicMat[2][2] = math.cos(deg_del)
    elif event.key == 'k':
        PointCloud[:, 1] = PointCloud[:, 1] * math.cos(deg_del) + PointCloud[:, 2] * math.sin(deg_del)
        PointCloud[:, 2] = -PointCloud[:, 1] * math.sin(deg_del) + PointCloud[:, 2] * math.cos(deg_del)
        new_ExtrinsicMat[1][1] = math.cos(deg_del)
        new_ExtrinsicMat[1][2] = math.sin(deg_del)
        new_ExtrinsicMat[2][1] = -math.sin(deg_del)
        new_ExtrinsicMat[2][2] = math.cos(deg_del)
    elif event.key == 'z':
        if MicroMode: MicroMode = 0
        else : MicroMode = 1
    elif event.key == 'p': # check calibration using refresh
        print(PointCloud[0])
        print(PointCloudOrigin[0])
        print(ExtrinsicMat @ PointCloudOrigin[0])
        for q in range(len(PointCloud)):
            PointCloud[q] = ExtrinsicMat @ PointCloudOrigin[q]
    elif event.key == '[':
        plt.cla()
        ax.plot(RefPointCloud[:, 0], RefPointCloud[:, 1], RefPointCloud[:, 2], 'r.', alpha=0.4, markersize=1)
        plt.draw()
        plt.axis('off')
        ax.set_xlim(new_xyz_lim[0][0], new_xyz_lim[0][1])
        ax.set_ylim(new_xyz_lim[1][0], new_xyz_lim[1][1])
        ax.set_zlim((new_xyz_lim[0][0] - new_xyz_lim[0][1]) / 2, (-new_xyz_lim[0][0] + new_xyz_lim[0][1]) / 2)
        print("micromde", MicroMode)
        print("result\n", ExtrinsicMat)
        return
    plt.cla()
    ax.plot(PointCloud[:, 0], PointCloud[:, 1], PointCloud[:, 2], 'b.', alpha=0.4, markersize=1)
    ax.plot(RefPointCloud[:, 0], RefPointCloud[:, 1], RefPointCloud[:, 2], 'r.', alpha=0.4, markersize=1)
    plt.draw()
    plt.axis('off')
    ax.set_xlim(new_xyz_lim[0][0], new_xyz_lim[0][1])
    ax.set_ylim(new_xyz_lim[1][0], new_xyz_lim[1][1])
    ax.set_zlim((new_xyz_lim[0][0] - new_xyz_lim[0][1])/2 , (-new_xyz_lim[0][0] + new_xyz_lim[0][1])/2)
    ExtrinsicMat = ExtrinsicMat @ new_ExtrinsicMat
    print("micromde", MicroMode)
    print("result\n", ExtrinsicMat)
global PointCloud
global PointCloudOrigin
global RefPointcloud

if __name__ == "__main__":
    RefPointCloud = binPCD2asciiPCD("C:\\Users\\정찬영\\PycharmProjects\\Radar_Lidar_calibration\\202254102723_bin.pcd")
    RefPointCloud.pop(-1)
    RefPointCloudNew = []
    PointCloud = binPCD2asciiPCD("C:\\Users\\정찬영\\PycharmProjects\\Radar_Lidar_calibration\\202254103025_bin.pcd")
    PointCloud.pop(-1)
    PointCloudNew = []
    for i in range(len(PointCloud)):
        Point = np.float_(PointCloud[i].split(" "))
        PointCloudNew.append([Point[0],Point[1], Point[2],1.0])
    for i in range(len(RefPointCloud)):
        Point = np.float_(RefPointCloud[i].split(" "))
        RefPointCloudNew.append([Point[0],Point[1], Point[2],1.0])

    PointCloud = np.reshape(PointCloudNew, (-1,4))
    PointCloudOrigin = PointCloud.copy()
    RefPointCloud = np.reshape(RefPointCloudNew, (-1, 4))
    ax.plot(PointCloud[:, 0], PointCloud[:, 1], PointCloud[:, 2], 'b.', alpha=0.4, markersize=1)
    ax.plot(RefPointCloud[:, 0], RefPointCloud[:, 1], RefPointCloud[:, 2], 'r.', alpha=0.4, markersize=1)
    cid2 = plt.connect('key_press_event', key_press)
    plt.show()
