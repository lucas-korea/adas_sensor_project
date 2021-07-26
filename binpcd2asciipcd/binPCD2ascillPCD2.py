import sys
import numpy as np
import os
import struct

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
DATA ascii
'''

def parsing_header_data(header):
    Line_num = 0
    print(header)
    txt_decode = header.decode().split("\n")
    while (txt_decode[Line_num].split(" ")[0] != "DATA"):
        if txt_decode[Line_num].split(" ")[0] == "SIZE":
            SIZE_list = txt_decode[Line_num].split(" ")[1:]
        elif txt_decode[Line_num].split(" ")[0] == "TYPE":
            TYPE_list = txt_decode[Line_num].split(" ")[1:]
        elif txt_decode[Line_num].split(" ")[0] == "POINTS":
            POINTS = txt_decode[Line_num].split(" ")[1]
        Line_num = Line_num + 1
    return SIZE_list, TYPE_list, POINTS

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

def parsing_bin_PCD(directory_path = os.getcwd()): # args가 없으면 코드가 위치한 디렉토리에서 검색,변환
    file_list = os.listdir(directory_path)
    file_list = [file for file in file_list if file.startswith("2_")] ## 지정된 디렉토리 내 pcd 파일만 검색
    file_list = [file for file in file_list if file.endswith("bin.pcd")]
    for i in file_list: #디렉토리 내 pcd 확장자 파일 대상으로 변환 시작 (ascii binary 구분없이 다 처리함)(근데 ascii 타입 pcd는 에러가 난다)
        print("now converting file name :" , i)
        file_name = i.split(".pcd")
        Origin_pcd_f = open(directory_path + "/" + i, 'rb')
        txt = Origin_pcd_f.read(0xc1) # 헤더까지 하드코딩으로 짜르기. 샘플로 제공된 pcd 파일은 전부 0x135위치까지 header가 차지하고 있기 때문에.
        SIZE_list, TYPE_list, POINTS = parsing_header_data(txt)
        PCD_data_part = Origin_pcd_f.read() # 헤더까지 다 읽은 기록이 있기 때문에, 나머지를 다 읽으면 PCD 데이터 부분이다.
        lines = parsing_PCD_data(PCD_data_part)
        POINTS = POINTS.replace("\n", "")
        with open (file_name[0] + "_ascii.pcd", 'w+') as f:
            f.write(HEADER.format(int(POINTS), int(POINTS))+'\n'.join(lines))
    # exit(1)

if __name__ == "__main__":
    try:
        parsing_bin_PCD(sys.argv[1])
    except:
        parsing_bin_PCD()
