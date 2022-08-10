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
        pcd_ts_list[i] = int(pcd_file_list[i].split('_')[3])  # pcd file 끝에 있는 tickcount 추출
    pcd_ts_list.sort()
    for i in range(len(pcd_file_list)):
        pcd_ts_list[i] = str(pcd_ts_list[i]) + '\n'
    return pcd_ts_list


def select_file(str_):
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
    lidar_data_list_txtfile, lidar_data_list_txtfile_path = select_file(
        "라이다 데이터 리스트가 적힌 txt파일을 선택 해 주세요")  # gui로 선택하게 하기
    lidar_data_list_txtfile = str(lidar_data_list_txtfile)
    lidar_data_list_txtfile_path = str(lidar_data_list_txtfile_path)
    if (lidar_data_list_txtfile[-15:] != '_lidar_list.txt'):
        print('error : you choose wrong file!!!!')
        exit(1)
    with open(lidar_data_list_txtfile, 'r') as f:
        lidar_date_list = f.readlines()
    print(lidar_date_list)
    for i in range(len(lidar_date_list)):
        lidar_date_list[i] = '_'.join(lidar_date_list[i].split('\\')[-1].split('_')[2:])[:-5]

    print(lidar_date_list) # yyyymmdd_hhmmss
    for date_i in range(len(lidar_date_list)):
        pcd_file_list = [file for file in os.listdir(lidar_data_list_txtfile_path) if
                         (file.startswith(lidar_date_list[date_i]) and file.endswith('H_upper.pcd'))]
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
    dirname = select_folder("Frame_TimesStamp(이미지 관련)가 모여있는 폴더를 선택하세요")
    for (path, dir, files) in os.walk(dirname):
        file_list.append([file for file in files if file.startswith("Frame_TimeStamp_")])
        file_path_list.append([path + '\\' + file for file in files if file.startswith("Frame_TimeStamp_")])
    file_list = [v for v in file_list if v]
    file_path_list = [v for v in file_path_list if v]
    move_dirname = select_folder("이미지(PNG) 파일이 있는 곳을 선택하세요")
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
            camera_ts_file = [file for file in os.listdir(camera_ts_path) if (file.endswith('_'.join(lidar_ts_filelist[file_i].split('_')[0:2]) + ".bin") and
                                                                              file.startswith('new_'))]
            print('camera_ts_file : ', camera_ts_file)
        with open(camera_ts_path + '\\' + camera_ts_file[0], 'r') as f:
            camera_ts_frame_list = f.readlines()
            camera_ts_list = [0 for i in range(len(camera_ts_frame_list))]
            camera_fr_list = [0 for i in range(len(camera_ts_frame_list))]
            for k in range(len(camera_ts_frame_list)):
                camera_ts_list[k] = camera_ts_frame_list[k].split('_')[0]
                camera_fr_list[k] = camera_ts_frame_list[k].split('_')[1]
            camera_ts_list = np.asarray(camera_ts_list, dtype=np.uint32)
            camera_fr_list = np.asarray(camera_fr_list, dtype=np.uint32)
        range_ = 40
        lidar_matched_list = []
        camera_matched_tick_list = []
        camera_matched_fr_list = []
        for i in range(len(lidar_ts_list)):
            mask_arr1 = camera_ts_list[:] > lidar_ts_list[i] - range_
            mask_arr2 = camera_ts_list[:] < lidar_ts_list[i] + range_
            mask_all = np.logical_and(mask_arr1, mask_arr2)
            tick = camera_ts_list[mask_all]
            frame = camera_fr_list[mask_all]
            tick = np.int64(tick)
            if len(tick) == 0:
                pass
            elif len(tick) == 1:
                lidar_matched_list.append(lidar_ts_list[i])
                camera_matched_tick_list.append(tick[findNearNum(tick, lidar_ts_list[i])[0]])
                camera_matched_fr_list.append(frame[findNearNum(tick, lidar_ts_list[i])[0]])
            elif len(tick) == 2:
                lidar_matched_list.append(lidar_ts_list[i])
                camera_matched_tick_list.append(tick[findNearNum(tick, lidar_ts_list[i])[0]])
                camera_matched_fr_list.append(frame[findNearNum(tick, lidar_ts_list[i])[0]])
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
    print(match_list_path_list,'\n', camera_ts_path,'\n', camera_ts_filelist,'\n', png_move_dir,'\n', pcd_move_dir)
    match_list_i = 0
    for match_list in match_list_path_list:
        camera_match_frame = []
        lidar_match_stamp = []
        with open(match_list, 'r') as f:
            lines = f.readlines()
        for i in range(len(lines)):
            camera_match_frame.append(lines[i].split('\t')[1])
            lidar_match_stamp.append(lines[i].split('\t')[2].replace('\n', ''))

        lidar_file_list = [file for file in os.listdir(camera_ts_path) if file.startswith('_'.join(match_list.split('\\')[-1].split('_')[0:2])) and file.endswith("H_upper.pcd")]
        camera_file_list = [file for file in os.listdir(camera_ts_filelist)
                            if file.startswith('1_' + '_'.join(match_list.split('\\')[-1].split('_')[0:2]))
                            or file.startswith('2_' + '_'.join(match_list.split('\\')[-1].split('_')[0:2]))
                            or file.startswith('3_' + '_'.join(match_list.split('\\')[-1].split('_')[0:2]))
                            or file.startswith('4_' + '_'.join(match_list.split('\\')[-1].split('_')[0:2]))
                            and file.endswith(".jpg")]
        print("camera_ts_path : ", camera_ts_path)
        print("camera_ts_filelist : ", camera_ts_filelist)
        # print("lidar_file_list : ", lidar_file_list)
        print("camera_file_list len : ", len(camera_file_list))
        lidar_match_file_list = []
        camera_match_file_list = []
        for i in range(len(camera_match_frame)):
            lidar_match_file_list.append([file for file in lidar_file_list if file.split('_')[3]==str(lidar_match_stamp[i])][-1])
            # camera_match_file_list.append([file for file in camera_file_list if file.endswith('0' + str(camera_match_frame[i]) + ".png")][-1])
            camera_match_file_list.append([file for file in camera_file_list if (int(file.split('_')[-1].split('.')[0]) == int(camera_match_frame[i])) and file.startswith('1_')][-1])
            # camera_match_file_list.append([file for file in camera_file_list if (int(file.split('_')[-1].split('.')[0]) == int(camera_match_frame[i])) and file.startswith('2_')][-1])
            # camera_match_file_list.append([file for file in camera_file_list if (int(file.split('_')[-1].split('.')[0]) == int(camera_match_frame[i])) and file.startswith('3_')][-1])
            # camera_match_file_list.append([file for file in camera_file_list if (int(file.split('_')[-1].split('.')[0]) == int(camera_match_frame[i])) and file.startswith('4_')][-1])

            # camera_match_file_list.append([file for file in camera_file_list if (int(file.split('_')[-1].split('.')[0]) == int(camera_match_frame[i]))][-1])
            # print(int(file.split('_')[-1].split('.')[0]))
        print("camera_match_file_list", camera_match_file_list)
        for i in range(len(camera_match_file_list)):
            print("coping {} / {} folder \t {} / {} files...".format(match_list_i+1, len(match_list_path_list), i+1, len(camera_match_file_list)))
            shutil.copy2(camera_ts_path + '\\' + lidar_match_file_list[i], pcd_move_dir + '\\' + '_'.join(lidar_match_file_list[i].replace('.pcd', '').split('_')[0:2])[2:]
                         + '_' + '{0:04d}'.format(i) + '_H'+ '.pcd')
            shutil.copy2(camera_ts_filelist + '\\' + camera_match_file_list[i], png_move_dir + '\\' + '_'.join(camera_match_file_list[i].replace('.png', '').split('_')[1:3])[2:]
                        + '_' + '{0:04d}'.format(i) + '_F' + '.png')
            shutil.copy2(camera_ts_filelist + '\\' + '2' + camera_match_file_list[i][1:], png_move_dir + '\\' + '_'.join(camera_match_file_list[i].replace('.png', '').split('_')[1:3])[2:]
                        + '_' + '{0:04d}'.format(i) + '_R' + '.png')
            shutil.copy2(camera_ts_filelist + '\\' + '3' + camera_match_file_list[i][1:], png_move_dir + '\\' + '_'.join(camera_match_file_list[i].replace('.png', '').split('_')[1:3])[2:]
                        + '_' + '{0:04d}'.format(i) + '_B' + '.png')
            shutil.copy2(camera_ts_filelist + '\\' + '4' + camera_match_file_list[i][1:], png_move_dir + '\\' + '_'.join(camera_match_file_list[i].replace('.png', '').split('_')[1:3])[2:]
                        + '_' + '{0:04d}'.format(i) + '_L' + '.png')
        match_list_i = match_list_i + 1

def matching_HighLow(match_list_path_list, lidar_ts_path, pcd_move_dir):
    range_ = 50
    for match_list in match_list_path_list:
        camera_match_frame = []
        lidar_match_stamp = []
        with open(match_list, 'r') as f:
            lines = f.readlines()
        for i in range(len(lines)):
            lidar_match_stamp.append(lines[i].split('\t')[2].replace('\n', ''))
        LowLidarList = [file for file in os.listdir(lidar_ts_path)
                        if file.startswith('_'.join(match_list.split('\\')[-1].split('_')[0:2]))
                        and file.endswith("L_under.pcd")]
        lidar_match_stamp_list = np.asarray(lidar_match_stamp, dtype=np.uint32)
        lidar_match_stamp_list.sort()
        LowLidarList.sort()
        LowLidar_stamp_List = []
        for i in range(len(LowLidarList)):
            LowLidar_stamp_List.append(int(LowLidarList[i].split('_')[3]))
        print("LowLidar_stamp_List", LowLidar_stamp_List)
        cnt = 0
        for i in range(len(LowLidarList)):
            print(i, '/' , len(LowLidarList))
            mask_arr1 = lidar_match_stamp_list[:] > LowLidar_stamp_List[i] - range_
            mask_arr2 = lidar_match_stamp_list[:] <= LowLidar_stamp_List[i] + range_
            mask_all = np.logical_and(mask_arr1, mask_arr2)
            if len(lidar_match_stamp_list[mask_all]):
                shutil.copy2(lidar_ts_path + '\\' + LowLidarList[i],
                             pcd_move_dir + '\\' + '_'.join(LowLidarList[i].split('_')[:2])[2:]
                             + '_'  + '{0:04d}'.format(cnt) + '_L'+ '.pcd')
                # print('_'.join(LowLidarList[i].split('_')[:2])[2:])
                cnt += 1
            else:
                print("no matched!!")

def main():
    print("select_lidar_data_list_txtfile_and_make_lidarTimeStamp_txtfile.......")
    lidar_ts_filelist, lidar_ts_path = select_lidar_data_list_txtfile_and_make_lidarTimeStamp_txtfile()
    print("search_all_Frame_TimeStamp_and_move2folder.......")
    camera_ts_filelist, camera_ts_path = search_all_Frame_TimeStamp_and_move2folder()
    print("make_match_list_txtfile.......")
    png_move_dir = select_folder("매칭한 PNG 파일을 저장할 폴더를 선택하시오")
    pcd_move_dir = select_folder("매칭한 PCD 파일을 저장할 폴더를 선택하시오")
    match_list_path_list = make_match_list_txtfile(lidar_ts_filelist, lidar_ts_path, camera_ts_path)
    print("extract_PCDPNGpair_by_matchlist.......")
    extract_PCDPNGpair_by_matchlist(match_list_path_list, lidar_ts_path, camera_ts_path, png_move_dir, pcd_move_dir)
    matching_HighLow(match_list_path_list, lidar_ts_path, pcd_move_dir)
if __name__ == "__main__":
    main()