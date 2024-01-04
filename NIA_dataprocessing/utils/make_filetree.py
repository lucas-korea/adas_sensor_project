import os
import numpy as np
from tkinter import filedialog
from tkinter import messagebox
import shutil

def select_folder(str_):
    folder = filedialog.askdirectory(initialdir=os.getcwd(),
                                        title=str_)
    if folder == '':
        print("폴더을 추가 하세요")
        messagebox.showwarning("경고", "폴더을 추가 하세요")  # 파일 선택 안했을 때 메세지 출력
        exit(1)
    return folder

if __name__ == '__main__':
    folder = select_folder("고르세요 폴더를")
    os.mkdir(folder + '\\'+ 'gps')
    os.mkdir(folder + '\\' + 'image_B')
    os.mkdir(folder + '\\' + 'image_F')
    os.mkdir(folder + '\\' + 'image_L')
    os.mkdir(folder + '\\' + 'image_R')
    os.mkdir(folder + '\\' + 'lidar_H')
    os.mkdir(folder + '\\' + 'lidar_L')
    print(folder)