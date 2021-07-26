import pickle
import sys
import numpy as np
import os
import struct
import binascii

HEADER = '''# .PCD v0.7 - Point Cloud Data file format
VERSION 0.7
FIELDS Scalar_field_#6 Scalar_field_#5 Scalar_field_#4 Scalar_field_#3 Scalar_field_#2 Scalar_field x y z _
SIZE 4 4 4 4 4 4 4 4 4 1
TYPE F F F F F F F F F U
COUNT 1 1 1 1 1 1 1 1 1 4
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
            byte_len = 4 * 9 + 1 * 4
            SF6, SF5, SF4, SF3, SF2, SF1, x, y, z, c1, c2, c3, c4 = struct.unpack("fff fff fff BBBB", PCD[start: start + byte_len])  # B:부호없는 정수, c:문자
            lines.append('{:.6f} {:.6f} {:.6f} {:.6f} {:.6f} {:.6f} {:.6f} {:.6f} {:.6f}  {} {} {} {}'.format(SF6, SF5, SF4, SF3,SF2, SF1, x, y, z,c1, c2, c3, c4))
            start = start + byte_len
        except:
            print("end of pcd file")
            break
    return lines

def parsing_bin_PCD(directory_path = os.getcwd()): # args가 없으면 코드가 위치한 디렉토리에서 검색,변환
    file_list = os.listdir(directory_path)
    file_list = [file for file in file_list if file.endswith(".pcd")] ## 지정된 디렉토리 내 pcd 파일만 검색
    for i in file_list: #디렉토리 내 pcd 확장자 파일 대상으로 변환 시작 (ascii binary 구분없이 다 처리함)(근데 ascii 타입 pcd는 에러가 난다)
        print("now converting file name :" , i)
        file_name = i.split(".pcd")
        Origin_pcd_f = open(directory_path + "\\" + i, 'rb')
        Origin_pcd_f.read(0x137) # 헤더까지 하드코딩으로 짜르기. 샘플로 제공된 pcd 파일은 전부 0x135위치까지 header가 차지하고 있기 때문에.
        PCD_data_part = Origin_pcd_f.read() # 헤더까지 다 읽은 기록이 있기 때문에, 나머지를 다 읽으면 PCD 데이터 부분이다.
        print(bytes(PCD_data_part[0:100]))
        print(file_name)
        try:
            with open (file_name[0] + ".bin", 'wb') as f:
                pickle.dump(PCD_data_part, f)
            with open(file_name[0] + ".bin2", 'w') as f:
                f.write(HEADER)
            with open(file_name[0] + ".bin2", 'ab') as f:
                f.write(PCD_data_part)
        except:
            with open(file_name[0] + ".bin2", 'wb') as f:
                f.write(PCD_data_part)
        exit(1)

def load_pickle():
    with open("2021-07-13-11-35-51_None-Data_15.bin", 'rb') as f:
        data = pickle.load(f)
        print(binascii.b2a_hex(data[0:100]))
        # print('\n'.join(parsing_PCD_data(data)))
        with open("bintest.txt", "w") as f:
            f.write('\n'.join(parsing_PCD_data(data)))

def main():
    # parsing_bin_PCD()
    load_pickle()

if __name__ == "__main__":
    main()
