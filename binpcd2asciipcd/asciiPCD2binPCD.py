import sys
import numpy as np
import os
import struct

file_list = os.listdir(os.getcwd())
file_list = [file for file in file_list if file.startswith("2_")]  ## 지정된 디렉토리 내 pcd 파일만 검색
file_list = [file for file in file_list if not file.endswith("bin.pcd")]
for file_name in file_list:
    f = open(file_name, 'r')
    header = []
    list_pcd = []
    for i in range(10):
        header.append(f.readline())
    f.readline() # DATA ascii 부분 날리기
    header.append("DATA binary\n")
    read_suc = f.readline()
    while read_suc:
        x, y, z, intensity = read_suc.split(' ')
        list_pcd.append([float(x), float(y), float(z), float(intensity.replace('\n', ""))])
        read_suc = f.readline()
    f.close()

    with open(file_name + "_bin.pcd", 'w') as f:
        f.write(''.join(header))
    with open(file_name + "_bin.pcd", 'ab') as f:
        for j in range(len(list_pcd)):
            f.write(struct.pack("ffff", list_pcd[j][0], list_pcd[j][1], list_pcd[j][2], list_pcd[j][3]))
