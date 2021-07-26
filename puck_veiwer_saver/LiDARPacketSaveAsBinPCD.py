import sys
import numpy as np
import os
import struct
import parse

HEADER = '''# .PCD v0.7 - Point Cloud Data file format
VERSION 0.7
FIELDS x y z intensity
SIZE 4 4 4 4
TYPE F F F F
COUNT 1 1 1 1
WIDTH {}
HEIGHT 1
VIEWPOINT 0 0 0 1 0 0 0
POINTS {}
DATA binary
'''

def parsing_PCD_data(PCD):
    start = 0
    lines = []
    while (1):
        try:
            byte_len = 4 * 4
            x, y, z, intensity = struct.unpack("ffff", PCD[start: start + byte_len])  # B:부호없는 정수, c:문자
            lines.append('{:.6f} {:.6f} {:.6f} {:.6f}'.format(x, y, z, intensity))
            start = start + byte_len
        except:
            print("end of pcd file")
            break
    return lines

def save_bin_PCD_from_packet(directory_path = os.getcwd()): # args가 없으면 코드가 위치한 디렉토리에서 검색,변환
    file_list = os.listdir(directory_path)
    file_list = [file for file in file_list if file.endswith(".bin")] ## 지정된 디렉토리 내 bin 파일만 검색
    for i in file_list:
        print("now converting file name :" , i)
        file_name = i.split(".bin")
        Origin_pcd_f = open(directory_path + "\\" + i, 'rb')
        PCD_packet = Origin_pcd_f.read()
        ###
        #paket data 2 point cloud data function
        get_data, point_cloud = parse.parse_pos(PCD_packet)
        ## 미완성
        ###
        lines = parsing_PCD_data(point_cloud)
        with open(file_name[0] + ".pcd", 'w') as f:
            f.write(HEADER.format(len(lines)))
        for j in range(len(lines)):
            with open(file_name[0] + ".pcd", 'ab') as f:
                f.write(struct.pack("ffff", lines[j][:]))

if __name__ == "__main__":
    save_bin_PCD_from_packet()
