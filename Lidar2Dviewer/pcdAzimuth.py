import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
import cv2
import pickle
import struct

def TruncDecimal(x, digitNum):
    # print(x)
    x = x * pow(10, digitNum)
    x = math.trunc(x)
    x = x / pow(10, digitNum)
    # print(x)
    return x

def binPCD2asciiPCD(file_name): # args가 없으면 코드가 위치한 디렉토리에서 검색,변환
    Origin_pcd_f = open(file_name, 'rb')
    header = []
    field_list = []
    size_list = []
    type_list = []
    count_list = []
    breaker = False

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
                breaker = True
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
    return lines

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
            else:
                lines[line_i] = lines[line_i][1:]
            start = start + byte_len
            line_i = line_i + 1
        except Exception as e:
            break
    return lines

data  = binPCD2asciiPCD("H:\\cam-lidar_calibration\\lidar-camera\\2_20210713_113013_000060_0.pcd")
# print(data)
VerticalAngle = []
for i in range(len(data)):
    if i % 5000 == 0:
        print(i / len(data))
    try:
        VerticalAngle.append(math.atan(TruncDecimal(float(data[i].split(' ')[3]), 4) / (
            math.sqrt(pow(TruncDecimal(float(data[i].split(' ')[1]), 4), 2) + pow(TruncDecimal(float(data[i].split(' ')[2]), 4), 2))) - 0.0013762) * 180 / math.pi)
    except:
        pass
        # print(float(data[i].split(' ')[3]), float(data[i].split(' ')[1]), float(data[i].split(' ')[2]))

VerticalAngle = [x for x in VerticalAngle if math.isnan(x) == False]
for i in range(len(VerticalAngle)):
    VerticalAngle[i] = round(VerticalAngle[i], 3)
VerticalAngle = list(set(VerticalAngle))
# print(len(VerticalAngle))
VerticalAngle.sort()
print(VerticalAngle)