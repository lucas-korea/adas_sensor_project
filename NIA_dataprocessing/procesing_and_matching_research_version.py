import os
import numpy as np
from tkinter import filedialog
from tkinter import messagebox
import shutil

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory. ' + directory)
        exit(1)

def select_onefile(str_):
    files = filedialog.askopenfilenames(initialdir=os.getcwd(),
                                        title=str_,
                                        filetypes=(("*.txt", "*txt"), ("*.xls", "*xls"), ("*.csv", "*csv")))
    if files == '':
        print("파일을 추가 하세요")
        messagebox.showwarning("경고", "파일을 추가 하세요")  # 파일 선택 안했을 때 메세지 출력
        exit(1)
    dir_path = ("\\".join(list(files)[0].split("/")[: -1]))  # path 추출
    files = ("\\".join(list(files)[0].split("/"))) #path\\파일명 추출
    return files, dir_path

def select_folder(str_):
    folder = filedialog.askdirectory(initialdir=os.getcwd(),
                                        title=str_)
    if folder == '':
        print("폴더을 추가 하세요")
        messagebox.showwarning("경고", "폴더을 추가 하세요")  # 파일 선택 안했을 때 메세지 출력
        exit(1)
    return "\\".join(folder.split("/"))


def select_lidar_data_list():
    lidar_data_list_txtfile, lidar_data_list_txtfile_path = select_onefile(
        "라이다 데이터 리스트가 적힌 txt파일을 선택 해 주세요")  # gui로 선택하게 하기
    lidar_path = str(lidar_data_list_txtfile_path)
    if not lidar_data_list_txtfile.endswith("_list.txt"):
        print('error : you choose wrong file!!!!')
        exit(1)
    with open(lidar_data_list_txtfile, 'r') as f:
        lidar_date_list = f.readlines()
    for i in range(len(lidar_date_list)):
        lidar_date_list[i] = '_'.join(lidar_date_list[i].split('\\')[-1].split('_')[2:])[:-4]
    return lidar_date_list, lidar_path


def extract_PCDPNGpair_by_matchlist(match_list_path_list, lidar_path, pcd_move_dir):
    match_list_i = 0
    for match_list in match_list_path_list:
        lidar_match_stamp = []
        with open(match_list, 'r') as f:
            lines = f.readlines()
        for i in range(len(lines)):
            lidar_match_stamp.append(lines[i].split('\t')[2].replace('\n', ''))

        lidar_file_list = [file for file in os.listdir(lidar_path) if file.startswith('_'.join(match_list.split('\\')[-1].split('_')[0:2])) and file.endswith(".npy")]
        lidar_match_file_list = []
        for i in range(len(lidar_match_stamp)):
            print([file for file in lidar_file_list if file.endswith(str(lidar_match_stamp[i]) + ".npy")])
            lidar_match_file_list.append([file for file in lidar_file_list if file.endswith(str(lidar_match_stamp[i]) + ".npy")][0])

        for i in range(len(camera_match_file_list)):
            print("coping {} / {} folder \t {} / {} files...".format(match_list_i+1, len(match_list_path_list), i+1, len(camera_match_file_list)))
            shutil.copy2(lidar_path + '\\' + lidar_match_file_list[i], pcd_move_dir + '\\' + '_'.join(lidar_match_file_list[i].replace('.npy', '').split('_')[0:2])
                         + '_' + '{0:06d}'.format(i) + '.npy')
        match_list_i = match_list_i + 1

def find_match_list(lidar_path_):
    list = [file for file in os.listdir(lidar_path_) if file.endswith('match_list.txt')]
    for i in range(len(list)):
        list[i] = lidar_path_ + '\\' + list[i]
    return list

def main():
    print("select_lidar_data_list_txtfile_and_make_lidarTimeStamp_txtfile.......")
    lidar_file_path, lidar_path = select_lidar_data_list()
    print("select match_list_txtfile.......")
    match_list_path_list = find_match_list(lidar_path)
    pcd_move_dir = select_folder("매칭한 PCD 파일을 저장할 폴더를 선택하시오")
    print("extract_PCDPNGpair_by_matchlist.......")
    extract_PCDPNGpair_by_matchlist(match_list_path_list,lidar_path, pcd_move_dir)

if __name__ == "__main__":
    main()