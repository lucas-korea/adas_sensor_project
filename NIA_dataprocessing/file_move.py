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


def copy_frametimestamp():
    file_path_list = []
    file_list = []
    dirname = select_folder("Frame_TimesStamp(이미지 관련)를 다 찾고자 하는 상위 폴더를 선택하세요")
    move_dirname = select_folder("Frame_TimesStamp를 복사할 곳을 선택하세요")
    for (path, dir, files) in os.walk(dirname):
        file_list.append([file for file in files if file.startswith("Frame_TimeStamp_")])
        file_path_list.append([path + '\\' + file for file in files if file.startswith("Frame_TimeStamp_")])
    file_list = [v for v in file_list if v]
    file_path_list = [v for v in file_path_list if v]

    file_new_list = [0 for i in range(len(file_list[0]))]
    for i in range(len(file_path_list)):
        shutil.copy2(file_path_list[i][0], move_dirname + '\\' + file_list[i][0])

def move_image_file():
    file_path_list = []
    file_list = []
    dirname = select_folder("image를 다 찾고자 하는 상위 폴더를 선택하세요")
    move_dirname = select_folder("image를 복사할 곳을 선택하세요")
    for (path, dir, files) in os.walk(dirname):
        print(path)
        for file in files:
            if file.endswith(".png"):
                file_list.append(file)
                file_path_list.append(path + '\\' + file)

    for i in range(len(file_path_list)):
        if i % 1000 == 0:
            print("{} / {} ".format(i, len(file_path_list)))
        shutil.move(file_path_list[i], move_dirname + '\\' + file_list[i])

def distribute_Kcity_data():
    PCDpath = "Y:\\PCDmatched"
    PNGpath = "Y:\\PNGmatched"
    for (path, dir, files) in os.walk("Y:"):
        for file in files:
            if file.endswith(".bin") and file.startswith("GPS"):
                print(path, dir, file)
                os.makedirs('\\'.join(path.split('\\')[:-1]) + "\\" + "image_F", exist_ok=True)
                os.makedirs('\\'.join(path.split('\\')[:-1]) + "\\" + "image_B", exist_ok=True)
                os.makedirs('\\'.join(path.split('\\')[:-1]) + "\\" + "image_L", exist_ok=True)
                os.makedirs('\\'.join(path.split('\\')[:-1]) + "\\" + "image_R", exist_ok=True)
                os.makedirs('\\'.join(path.split('\\')[:-1]) + "\\" + "Lidar_H", exist_ok=True)

                PCDlist = os.listdir(PCDpath)
                PCDlist = [f for f in PCDlist if f.startswith("_".join(file.split('_')[1:3])[2:-4]) and f.endswith('.pcd')]

                PNGlistF = os.listdir(PNGpath)
                PNGlistF = [f for f in PNGlistF if f.startswith("_".join(file.split('_')[1:3])[2:-4]) and f.endswith("F.png")]

                PNGlistB = os.listdir(PNGpath)
                PNGlistB = [f for f in PNGlistB if f.startswith("_".join(file.split('_')[1:3])[2:-4]) and f.endswith("B.png")]

                PNGlistL = os.listdir(PNGpath)
                PNGlistL = [f for f in PNGlistL if f.startswith("_".join(file.split('_')[1:3])[2:-4]) and f.endswith("L.png")]

                PNGlistR = os.listdir(PNGpath)
                PNGlistR = [f for f in PNGlistR if f.startswith("_".join(file.split('_')[1:3])[2:-4]) and f.endswith("R.png")]

                for PCDfile in PCDlist:
                    shutil.copy2(PCDpath + '\\' + PCDfile, '\\'.join(path.split('\\')[:-1]) + "\\" + "Lidar_H" + '\\' + PCDfile)
                for PNGfile in PNGlistF:
                    shutil.copy2(PNGpath + '\\' + PNGfile, '\\'.join(path.split('\\')[:-1]) + "\\" + "image_F" + '\\' + PNGfile)
                for PNGfile in PNGlistB:
                    shutil.copy2(PNGpath + '\\' + PNGfile, '\\'.join(path.split('\\')[:-1]) + "\\" + "image_B" + '\\' + PNGfile)
                for PNGfile in PNGlistL:
                    shutil.copy2(PNGpath + '\\' + PNGfile, '\\'.join(path.split('\\')[:-1]) + "\\" + "image_L" + '\\' + PNGfile)
                for PNGfile in PNGlistR:
                    shutil.copy2(PNGpath + '\\' + PNGfile, '\\'.join(path.split('\\')[:-1]) + "\\" + "image_R" + '\\' + PNGfile)



if __name__ == "__main__":
    distribute_Kcity_data()
