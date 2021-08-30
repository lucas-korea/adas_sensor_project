import os
import numpy as np
from tkinter import filedialog
from tkinter import messagebox
import shutil

# path_dir = "E:\\20210826_005023\\20210826_005023\\PCDPNGfiles_matched"
# move_dir = "E:\\20210826_005023\\20210826_005023\\PCDPNGfiles"
# file_list = [file for file in os.listdir(path_dir) if file.endswith(".png")]
# print(len(file_list))
# png_i = 0
# for file_name in file_list:
#     if png_i % 10 == 5 or png_i % 10 == 0 or 1:
#         print(png_i)
#         shutil.move(path_dir + '\\' + file_name, move_dir + '\\' + file_name)
#     png_i = png_i + 1


def select_folder(str_):
    folder = filedialog.askdirectory(initialdir=os.getcwd(),
                                        title=str_)
    if folder == '':
        print("폴더을 추가 하세요")
        messagebox.showwarning("경고", "폴더을 추가 하세요")  # 파일 선택 안했을 때 메세지 출력
        exit(1)
    return "\\".join(folder.split("/"))



file_path_list = []
file_list = []
dirname = select_folder("Frame_TimesStamp(이미지 관련)를 다 찾고자 하는 상위 폴더를 선택하세요")
for (path, dir, files) in os.walk(dirname):
    file_list.append([file for file in files if file.startswith("Frame_TimeStamp_")])
    file_path_list.append([path + '\\' + file for file in files if file.startswith("Frame_TimeStamp_")])
file_list = [v for v in file_list if v]
file_path_list = [v for v in file_path_list if v]
move_dirname = select_folder("Frame_TimesStamp를 복사할 곳을 선택하세요")
file_new_list = [0 for i in range(len(file_list[0]))]
for i in range(len(file_path_list)):
    shutil.copy2(file_path_list[i][0], move_dirname + '\\' + file_list[i][0])