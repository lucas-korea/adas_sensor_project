import os
import struct
from tkinter import filedialog
from tkinter import messagebox
import numpy as np


# def main():
#     PATH = "D:\\NIA4차 대비 실도로 주행 sample PNGPCD 3case"
#     PCDlist = [file for file in os.listdir(PATH) if os.path.splitext(file)[1] == '.pcd']
#     print(PCDlist)
#
#     for j in range(len(PCDlist)):
#         print(j/len(PCDlist))
#         with open(PATH + '\\' + PCDlist[j], 'rb') as f:
#             header = b''
#             for i in range(11):
#                 header += f.readline()
#             point_cloud = f.read()
#
#         with open(PATH + '\\' + PCDlist[j].split('.')[0] + '_convert.pcd', 'ab') as f:
#             f.write(header)
#             for i in range(int(len(point_cloud)/16)):
#                 onepoint = struct.unpack('ffff', point_cloud[0 + i * 16:16 + i * 16])
#                 f.write(struct.pack('ffff', -onepoint[1], onepoint[0], onepoint[2], onepoint[3]))

def ChangeAxis(FilePath):
    with open(FilePath, 'rb') as f:
        header = b''
        for i in range(11):
            header += f.readline()
        point_cloud = f.read()

    with open(FilePath.split('.')[0] + '_convert2.pcd', 'ab') as f:
        f.write(header)
        for i in range(int(len(point_cloud)/16)):
            onepoint = struct.unpack('ffff', point_cloud[0 + i * 16:16 + i * 16])
            f.write(struct.pack('ffff', -onepoint[0], onepoint[1], onepoint[2], onepoint[3]))

def chaneg_angle(FilePath):
    with open(FilePath, 'rb') as f:
        header = b''
        for i in range(11):
            header += f.readline()
        point_cloud = f.read()

    with open(FilePath.split('.')[0] + '_convert2.pcd', 'ab') as f:
        f.write(header)
        for i in range(int(len(point_cloud)/16)):
            onepoint = struct.unpack('ffff', point_cloud[0 + i * 16:16 + i * 16])
            f.write(struct.pack('ffff',
                                np.cos(2 / 180 * np.pi) * onepoint[0] - np.sin(2 / 180 * np.pi) * onepoint[1],
                                np.sin(2 / 180 * np.pi) * onepoint[0] + np.cos(2 / 180 * np.pi) * onepoint[1]
                                , onepoint[2], onepoint[3]))

def select_files(str_):
    files = filedialog.askopenfilenames(initialdir=os.getcwd(),
                                        title=str_,
                                        filetypes=( ("*.pcd", "*pcd"), ("*.txt", "*txt")))
    if files == '':
        print("파일을 추가 하세요")
        messagebox.showwarning("경고", "파일을 추가 하세요")  # 파일 선택 안했을 때 메세지 출력
        exit(1)
    return files

if __name__ == "__main__":
    files = select_files("파일 선택하세요")
    print(files)
    # path = "I:\\20220727calibration\\cam-lidar mating\\lidar_h(좌표축 에러)"
    # files = os.listdir(path)
    cnt = 0
    for file in files:
        chaneg_angle(file)
        print(cnt, '/', len(files))
        cnt += 1