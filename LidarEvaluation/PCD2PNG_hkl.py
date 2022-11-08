import sys
import numpy as np
import pandas as pd
import math
import cv2
import struct
np.set_printoptions(threshold=sys.maxsize)


def parsing_binPCD2asciiPCD(PCD, size_list, type_list, count_list, colrow):
    print(colrow)
    start = 0
    pack_str = ""
    byte_len = 0
    type_list[-1] = type_list[-1].replace('\n', '')
    type_list[-1] = type_list[-1].replace('\r', '')
    for i in range(len(type_list)):
        if (type_list[i] == "F"):
            for j in range(int(count_list[i])):
                pack_str = pack_str + "f"
                byte_len = byte_len + 4
        elif (type_list[i] == "U"):
            for j in range(int(count_list[i])):
                if size_list[i] == "1":
                    pack_str = pack_str + "B"
                elif size_list[i] == "4":
                    pack_str = pack_str + 'BBBB'
                byte_len = byte_len + int(size_list[i])
    Depth_img = np.zeros((56, 384), dtype=np.uint8)
    intensity_img = np.zeros((56, 384), dtype=np.uint8)
    intensity_img_realLike = np.zeros((56, 384*2), dtype=np.uint8)
    HorizonResol = 360 / (384)
    for row in range(56):
        for col in range(384):
            #pixel에 1:1 매칭이 되는 이미지
            print(pack_str, byte_len, PCD[start: start + byte_len])
            scalar_fileds = struct.unpack(pack_str, PCD[start: start + byte_len])  # B:부호없는 정수, c:문자
            Depth_img[row, col] = 3*np.sqrt(scalar_fileds[0]*scalar_fileds[0] + scalar_fileds[1]*scalar_fileds[1] + scalar_fileds[2]*scalar_fileds[2])
            intensity_img[row, col] = (scalar_fileds[4] + scalar_fileds[5] + scalar_fileds[6])/3
            start = start + byte_len
            # print(scalar_fileds)
    return Depth_img, intensity_img, intensity_img_realLike

def MakePCDimg(file_name):
    Origin_pcd_f = open(file_name, 'rb')
    header = []
    field_list = []
    size_list = []
    type_list = []
    count_list = []
    width = 0
    height = 0
    breaker = False

    line = Origin_pcd_f.readline().decode()
    line = line.replace("\r", "")
    line = line.replace("\n", "")
    header.append(line + '\n')
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
            for j in range(len(words) - 1):
                field_list.append(words[j + 1])
        elif words[0] == "SIZE":
            for j in range(len(words) - 1):
                size_list.append(words[j + 1])
        elif words[0] == "TYPE":
            for j in range(len(words) - 1):
                type_list.append(words[j + 1])
        elif words[0] == "COUNT":
            for j in range(len(words) - 1):
                count_list.append(words[j + 1])
        elif words[0] == "WIDTH":
            width = int(words[1])
        elif words[0] == "HEIGHT":
            height = int(words[1])
        header.append(line + '\n')

    PCD_data_part = Origin_pcd_f.read()  # 헤더까지 다 읽은 기록이 있기 때문에, 나머지를 다 읽으면 PCD 데이터 부분이다.
    Depth_img, intensity_img, intensity_img_realLike = parsing_binPCD2asciiPCD(PCD_data_part, size_list, type_list, count_list, (width, height))
    return Depth_img, intensity_img, intensity_img_realLike