import os
import pandas as pd
import shutil

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
    dst_folder = ""
    KATECH_path = "G:\\2021.11.17 천안 한자연 Lidar 테스트\\한자연로깅\\검정색옷 보행자 테스트\\2"
    print(os.listdir(KATECH_path))
    CANEVI_path = "G:\\2021.11.17 천안 한자연 Lidar 테스트\\카네비로깅\\보행자\\검정색옷 보행자 테스트\\20m"
    print(os.listdir(CANEVI_path))
    dst_path = "G:\\2021.11.17 천안 한자연 Lidar 테스트\\통합\\" + dst_folder

def extract_folder_name_list():
    with open("list2.txt", 'w', encoding="UTF-8") as f:
        print(os.listdir("G:\\2021.11.17 천안 한자연 Lidar 테스트\\통합"))
        for i in range(len(os.listdir("G:\\2021.11.17 천안 한자연 Lidar 테스트\\통합"))):
            f.write(os.listdir("G:\\2021.11.17 천안 한자연 Lidar 테스트\\통합")[i] + '\n')
if __name__== "__main__":
    main()