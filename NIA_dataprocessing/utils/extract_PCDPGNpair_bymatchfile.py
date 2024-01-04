import shutil
import os
from tkinter import filedialog
from tkinter import messagebox



def select_folder(str_):
    folder = filedialog.askdirectory(initialdir=os.getcwd(),
                                        title=str_)
    if folder == '':
        print("폴더을 추가 하세요")
        messagebox.showwarning("경고", "폴더을 추가 하세요")  # 파일 선택 안했을 때 메세지 출력
        exit(1)
    return "\\".join(folder.split("/"))


def extract_PCDPNGpair_by_matchlist(match_list_path_list, camera_ts_path, camera_ts_filelist):
    png_move_dir = select_folder("매칭한 PNG 파일을 저장할 폴더를 선택하시오")
    pcd_move_dir = select_folder("매칭한 PCD 파일을 저장할 폴더를 선택하시오")

    for match_list in match_list_path_list:
        print(match_list)
        camera_match_frame = []
        lidar_match_stamp = []
        with open(match_list, 'r') as f:
            lines = f.readlines()
        for i in range(len(lines)):
            camera_match_frame.append(lines[i].split('\t')[1])
            lidar_match_stamp.append(lines[i].split('\t')[2].replace('\n', ''))

        '_'.join(match_list.split('\\')[-1].split('_')[0:2])
        lidar_file_list = [file for file in os.listdir(camera_ts_path) if file.startswith('_'.join(match_list.split('\\')[-1].split('_')[0:2])) and file.endswith(".pcd")]
        camera_file_list = [file for file in os.listdir(camera_ts_filelist) if file.startswith('2_' + '_'.join(match_list.split('\\')[-1].split('_')[0:2])) and file.endswith(".png")]
        lidar_match_file_list = []
        camera_match_file_list = []
        for i in range(len(camera_match_frame)):
            lidar_match_file_list.append([file for file in lidar_file_list if file.endswith(str(lidar_match_stamp[i]) + ".pcd")][0])
            camera_match_file_list.append([file for file in camera_file_list if file.endswith(str(camera_match_frame[i]) + ".png")][0])

        for i in range(len(camera_match_file_list)):
            shutil.copy2(camera_ts_path + '\\' + lidar_match_file_list[i], pcd_move_dir + '\\' + '_'.join(lidar_match_file_list[i].replace('.pcd', '').split('_')[0:2])
                         + '_' + '{0:06d}'.format(i) + '.pcd')
            shutil.copy2(camera_ts_filelist + '\\' + camera_match_file_list[i], png_move_dir + '\\' + '1_' + '_'.join(camera_match_file_list[i].replace('.png', '').split('_')[1:3])
                         + '_' + '{0:06d}'.format(i) + '.png')
if __name__ == "__main__":
    extract_PCDPNGpair_by_matchlist()