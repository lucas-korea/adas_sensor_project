import os
import pandas as pd
import shutil
import glob
path = "G:\\2021.11.17 천안 한자연 Lidar 테스트\\H2BUS_LiDAR_실험기록_211117.xlsx"
def main():
    data = pd.read_excel(path, sheet_name=1)
    for i in range(len(data.values)):
        STR = (str(data.values[i][0]).replace('\'', '') + '_' +
        str(data.values[i][1]).replace('\'', '') + '_' +
        str(data.values[i][3]).replace('\'', '') + '_' +
        str(data.values[i][4]).replace('\'', '') + '_' +
        str(data.values[i][6]).replace('\'', ''))
        os.mkdir("G:\\2021.11.17 천안 한자연 Lidar 테스트\\통합\\" + STR)

def main2():
    PATH_LIST = os.listdir("G:\\2021.11.17 천안 한자연 Lidar 테스트\\통합")
    for PATH in PATH_LIST:
        os.mkdir("G:\\2021.11.17 천안 한자연 Lidar 테스트\\통합\\" + PATH + '\\20˚' )
        os.mkdir("G:\\2021.11.17 천안 한자연 Lidar 테스트\\통합\\" + PATH + '\\9.6˚')
        os.mkdir("G:\\2021.11.17 천안 한자연 Lidar 테스트\\통합\\" + PATH + '\\webcam')
        os.mkdir("G:\\2021.11.17 천안 한자연 Lidar 테스트\\통합\\" + PATH + '\\velodyne puck')


 ## 카네비컴 pcd 파일 각도별로 하나씩만 복사, 복사하면서 이름도 변경 (예시: point.cloud.pcd -> 1_주간_보행자_흑색_10_20˚.pcd)
 ## 벨로다인 pcd 파일 이름 변경하면서 복사 (1_주간_보행자_흑색_10_puck.pcd)
 ## 웹캠 이미지,영상 복사 (1_주간_보행자_흑색_10.jpg or .avi)
def move_files():
    num1 = '7'
    num2 = '70m'
    dst_folder = '36_주간_이륜차_흑색_70'
    print(dst_folder)
    KATECH_path = "G:\\2021.11.17 천안 한자연 Lidar 테스트\\한자연로깅\\검은옷 이륜차테스트\\" + num1
    CANEVI_path = "G:\\2021.11.17 천안 한자연 Lidar 테스트\\카네비로깅\\이륜차\\검정색옷 이륜차 테스트\\" + num2
    dst_path = "G:\\2021.11.17 천안 한자연 Lidar 테스트\\통합"

    shutil.copy2(KATECH_path + '\\' + "PCDLOG_LiDAR(0).pcd" ,dst_path + '\\' + dst_folder)
    os.rename(dst_path + '\\' + dst_folder + '\\' + "PCDLOG_LiDAR(0).pcd" , dst_path + '\\' + dst_folder + '\\' + dst_folder +"_20˚_2.pcd")
    shutil.copy2(CANEVI_path + '\\' + "PCDLOG_LiDAR(0).pcd" ,dst_path + '\\' + dst_folder)
    os.rename(dst_path + '\\' + dst_folder + '\\' + "PCDLOG_LiDAR(0).pcd" , dst_path + '\\' + dst_folder + '\\' + dst_folder + "_9.6˚_2.pcd")
    shutil.copy2(glob.glob(KATECH_path + '\\2021*')[0], dst_path + '\\' + dst_folder)
    os.rename(glob.glob(dst_path + '\\' + dst_folder + '\\2021*')[0], dst_path + '\\' + dst_folder + '\\' + dst_folder + '_puck_2.pcd')
    shutil.copy2(glob.glob(KATECH_path + '\\TV*')[0], dst_path + '\\' + dst_folder)
    extension = os.path.splitext(glob.glob(dst_path + '\\' + dst_folder + '\\TV*')[0])[1]
    os.rename(glob.glob(dst_path + '\\' + dst_folder + '\\TV*')[0], dst_path + '\\' + dst_folder + '\\' + dst_folder + '_2' + extension)

def extract_folder_name_list():
    with open("list2.txt", 'w', encoding="UTF-8") as f:
        print(os.listdir("G:\\2021.11.17 천안 한자연 Lidar 테스트\\통합"))
        for i in range(len(os.listdir("G:\\2021.11.17 천안 한자연 Lidar 테스트\\통합"))):
            f.write(os.listdir("G:\\2021.11.17 천안 한자연 Lidar 테스트\\통합")[i] + '\n')
if __name__== "__main__":
    move_files()
    # for (path, dir, files) in os.walk("G:\\2021.11.17 천안 한자연 Lidar 테스트\\통합"):
    #     print(path)
    #     print(len(files),'개 : ', files)
