import os
import numpy as np
from tkinter import filedialog
from tkinter import messagebox
import shutil

def findNearNum(exList, values):
    answer = [0 for _ in range(2)]  # answer 리스트 0으로 초기화
    minValue = min(exList, key=lambda x: abs(x - values))
    exList = exList.tolist()
    minIndex = exList.index(minValue)
    answer[0] = minIndex
    answer[1] = minValue
    return answer

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory. ' + directory)
        exit(1)


def make_pcd_ts_listtxt(pcd_file_list):
    pcd_ts_list = [0 for i in range(len(pcd_file_list))]
    for i in range(len(pcd_file_list)):
        pcd_ts_list[i] = int(pcd_file_list[i].split('_')[-1][:-4])  # pcd file 끝에 있는 tickcount 추출
    pcd_ts_list.sort()
    for i in range(len(pcd_file_list)):
        pcd_ts_list[i] = str(pcd_ts_list[i]) + '\n'
    return pcd_ts_list


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


def select_lidar_data_list_txtfile_and_make_lidarTimeStamp_txtfile():
    # lidar_data_list_txtfile, lidar_data_list_txtfile_path = select_onefile(
    #     "라이다 데이터 리스트가 적힌 txt파일을 선택 해 주세요")  # gui로 선택하게 하기
    lidar_data_list_txtfile = 'E:\\20230824_lidar_camera_calibration\\H_L202308241634_lidar_list.txt'
    lidar_data_list_txtfile_path = 'E:\\20230824_lidar_camera_calibration'
    lidar_data_list_txtfile = str(lidar_data_list_txtfile)
    lidar_data_list_txtfile_path = str(lidar_data_list_txtfile_path)
    if (lidar_data_list_txtfile[-15:] != '_lidar_list.txt'):
        print('error : you choose wrong file!!!!')
        exit(1)
    with open(lidar_data_list_txtfile, 'r') as f:
        lidar_date_list = f.readlines()
    for i in range(len(lidar_date_list)):
        lidar_date_list[i] = '_'.join(lidar_date_list[i].split('\\')[-1].split('_')[1:3])[:-5]
    for date_i in range(len(lidar_date_list)):
        pcd_file_list = [file for file in os.listdir(lidar_data_list_txtfile_path) if
                         (file.startswith(lidar_date_list[date_i]) and file.endswith('.pcd'))]
        pcd_ts_list = make_pcd_ts_listtxt(pcd_file_list)
        with open(lidar_data_list_txtfile_path + "\\" + lidar_date_list[date_i] + "_lidar_TimeStamp.txt", 'w') as f:
            f.writelines(pcd_ts_list)
            print(lidar_data_list_txtfile_path + "\\" + lidar_date_list[
                date_i] + "_lidar_TimeStamp.txt" + "  {}th pcd ts list txt file maded!".format(date_i + 1))
        lidar_date_list[date_i] = lidar_date_list[date_i] + "_lidar_TimeStamp.txt"
    return lidar_date_list, lidar_data_list_txtfile_path


def search_all_Frame_TimeStamp_and_move2folder():
    file_path_list = []
    file_list = []
    # dirname = select_folder("Frame_TimesStamp(이미지 관련)가 모여있는 폴더를 선택하세요")
    dirname = 'E:\\20230824_lidar_camera_calibration\\frametimestamp'
    for (path, dir, files) in os.walk(dirname):
        file_list.append([file for file in files if file.startswith("Frame_TimeStamp_")])
        file_path_list.append([path + '\\' + file for file in files if file.startswith("Frame_TimeStamp_")])
    file_list = [v for v in file_list if v]
    file_path_list = [v for v in file_path_list if v]
    # move_dirname = select_folder("이미지(PNG) 파일이 있는 곳을 선택하세요")
    move_dirname = 'E:\\20230824_lidar_camera_calibration\\PNG'
    file_new_list = [0 for i in range(len(file_list[0]))]
    for i in range(len(file_path_list[0])):
        with open(file_path_list[0][i], 'r') as f:
            lines = f.readlines()
            for line_i in range(len(lines)):
                lines[line_i] = lines[line_i].split("\t")[1].replace(' ', '').replace('\n', '') + '_' + str(
                    line_i) + '\n'
        with open(move_dirname + '\\new_' + file_list[0][i], 'w') as f:
            f.writelines(lines)
        print("open {}  $$and make$$ {} !! \t {}th file".format(file_path_list[0][i], move_dirname + '\\new_' + file_list[0][i], i+1))
        file_new_list[i] = file_list[0][i]
    return file_list, move_dirname


def make_match_list_txtfile(lidar_ts_filelist, lidar_ts_path, camera_ts_path):
    match_list_path_list = []
    for file_i in range(len(lidar_ts_filelist)):
        with open(lidar_ts_path + '\\' + lidar_ts_filelist[file_i], 'r') as f:
            lidar_ts_list = f.readlines()
            lidar_ts_list = np.asarray(lidar_ts_list, dtype=np.uint32)
            print(lidar_ts_filelist)
            print('_'.join(lidar_ts_filelist[file_i].split('_')[0:2]) + ".bin")
            camera_ts_file = [file for file in os.listdir(camera_ts_path) if (file.endswith('_'.join(lidar_ts_filelist[file_i].split('_')[0:2]) + ".bin"))]
        with open(camera_ts_path + '\\' + camera_ts_file[0], 'r') as f:
            camera_ts_frame_list = f.readlines()
            camera_ts_list = [0 for i in range(len(camera_ts_frame_list))]
            camera_fr_list = [0 for i in range(len(camera_ts_frame_list))]
            for k in range(len(camera_ts_frame_list)):
                camera_ts_list[k] = camera_ts_frame_list[k].split('_')[0]
                camera_fr_list[k] = camera_ts_frame_list[k].split('_')[1]
            camera_ts_list = np.asarray(camera_ts_list, dtype=np.uint32)
            camera_fr_list = np.asarray(camera_fr_list, dtype=np.uint32)
        range_ = 34
        lidar_matched_list = []
        camera_matched_tick_list = []
        camera_matched_fr_list = []
        for i in range(len(lidar_ts_list)):
            mask_arr1 = camera_ts_list[:] > lidar_ts_list[i] - range_
            mask_arr2 = camera_ts_list[:] < lidar_ts_list[i] + range_
            mask_all = np.logical_and(mask_arr1, mask_arr2)
            tick = camera_ts_list[mask_all]
            frame = camera_fr_list[mask_all]
            if len(tick) == 0 :
                print("skip PCD file matching!! no matched RGB and thermal!")
                pass
            else:
                lidar_matched_list.append(lidar_ts_list[i])
                camera_matched_tick_list.append(tick[findNearNum(tick, lidar_ts_list[i])[0]])
                camera_matched_fr_list.append(frame[findNearNum(tick, lidar_ts_list[i])[0]])
        with open(lidar_ts_path + '\\' + '_'.join(lidar_ts_filelist[file_i].split('_')[0:2]) + "_match_list.txt", 'w') as f:
            print(lidar_ts_path + '\\' + '_'.join(lidar_ts_filelist[file_i].split('_')[0:2]) + "_match_list.txt\t{}th file maded!!".format(file_i+1))
            for i in range(len(lidar_matched_list)):
                f.write(str(camera_matched_tick_list[i]) + '\t' + str(camera_matched_fr_list[i]) + '\t' +
                        str(lidar_matched_list[i]) + '\n')
        match_list_path_list.append(lidar_ts_path + '\\' + '_'.join(lidar_ts_filelist[file_i].split('_')[0:2]) + "_match_list.txt")
    return match_list_path_list


def extract_PCDPNGpair_by_matchlist(match_list_path_list, camera_ts_path, camera_ts_filelist, png_move_dir, pcd_move_dir):
    match_list_i = 0
    for match_list in match_list_path_list:
        camera_match_frame = []
        lidar_match_stamp = []
        with open(match_list, 'r') as f:
            lines = f.readlines()
        for i in range(len(lines)):
            camera_match_frame.append(lines[i].split('\t')[1])
            lidar_match_stamp.append(lines[i].split('\t')[2].replace('\n', ''))

        lidar_file_list = [file for file in os.listdir(camera_ts_path) if file.startswith('_'.join(match_list.split('\\')[-1].split('_')[0:2])) and file.endswith(".pcd")]
        camera_file_list = [file for file in os.listdir(camera_ts_filelist) if file.startswith('2_' + '_'.join(match_list.split('\\')[-1].split('_')[0:2])) and file.endswith(".png")]
        lidar_match_file_list = []
        camera_match_file_list = []
        for i in range(len(camera_match_frame)):
            lidar_match_file_list.append([file for file in lidar_file_list if file.endswith(str(lidar_match_stamp[i]) + ".pcd")][0])
            camera_match_file_list.append([file for file in camera_file_list if file.endswith(str(camera_match_frame[i]) + ".png")][0])

        for i in range(len(camera_match_file_list)):
            print("coping {} / {} folder \t {} / {} files...".format(match_list_i+1, len(match_list_path_list), i+1, len(camera_match_file_list)))
            shutil.copy2(camera_ts_path + '\\' + lidar_match_file_list[i], pcd_move_dir + '\\' + '_'.join(lidar_match_file_list[i].replace('.pcd', '').split('_')[0:2])
                         + '_' + '{0:06d}'.format(i) + '.pcd')
            shutil.copy2(camera_ts_filelist + '\\' + camera_match_file_list[i], png_move_dir + '\\' + '1_' + '_'.join(camera_match_file_list[i].replace('.png', '').split('_')[1:3])
                         + '_' + '{0:06d}'.format(i) + '.png')
        match_list_i = match_list_i + 1


def main():
    print("select_lidar_data_list_txtfile_and_make_lidarTimeStamp_txtfile.......")
    lidar_ts_filelist, lidar_ts_path = select_lidar_data_list_txtfile_and_make_lidarTimeStamp_txtfile()

    print("search_all_Frame_TimeStamp_and_move2folder.......")
    camera_ts_filelist, camera_ts_path = search_all_Frame_TimeStamp_and_move2folder()
    print("make_match_list_txtfile.......")
    # png_move_dir = select_folder("매칭한 PNG 파일을 저장할 폴더를 선택하시오")
    # pcd_move_dir = select_folder("매칭한 PCD 파일을 저장할 폴더를 선택하시오")
    png_move_dir='E:\\20230824_lidar_camera_calibration\\PNG_matched'
    pcd_move_dir='E:\\20230824_lidar_camera_calibration\\PCD_matched'
    print(lidar_ts_filelist, '\n', lidar_ts_path,'\n',  camera_ts_path)
    match_list_path_list = make_match_list_txtfile(lidar_ts_filelist, lidar_ts_path, camera_ts_path)
    print("extract_PCDPNGpair_by_matchlist.......")
    extract_PCDPNGpair_by_matchlist(match_list_path_list, lidar_ts_path, camera_ts_path, png_move_dir, pcd_move_dir)

if __name__ == "__main__":
    main()