# 본 코드는 gps binary 데이터를 이용해 좌표 list를 뽑아내고, 이를 google map api를 이용하여 실제로 그려본다

import csv
from tkinter import filedialog
from tkinter import messagebox
import os

def select_file(str_):
    files = filedialog.askopenfilenames(initialdir=os.getcwd(),
                                        title=str_,
                                        filetypes=( ("*.bin", "*bin"), ("*.txt", "*txt"),("*.csv", "*csv")))
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

def GPGGA_parser(line):
    line = line.replace('\n', '').split('\t')[2:5]

    return splited_GPGGA


def GPRMC_parser(line):
    line = line.replace('\n', '').split('\t')[2:5]

    return splited_GPRMC

def function():
    # gps_bin_path = select_file('select GPS bin file')[0]
    # match = open(select_file('select mathch file')[0])
    # gps_save_path = select_folder("select save folder")
    files = os.listdir('F:\\20230828_gps_test\\bin')
    for i in range(len(files)):
        gps_bin_path = 'F:\\20230828_gps_test\\bin\\' + files[i]
        with open(gps_bin_path) as f:
            print(gps_bin_path)
            cnt = 0
            CSV = open('F:\\20230828_gps_test\\csv\\' + files[i].split('.')[0] + '.csv',
                       'w', encoding='utf-8', newline='')
            wr = csv.writer(CSV)
            line_empty_flag = 0
            while(1):
                line = f.readline().replace(' ', '')
                line = line.replace('\n', '').split('\t')[2:5]
                print(line)
                if line_empty_flag == 10:
                    break
                line_empty_flag += 1
                if len(line) > 1 and line[2][:6] == '$PASHR' :

                    print(cnt)
                    roll = float(line[2].split(',')[5])
                    pitch = float(line[2].split(',')[6])
                    f.readline() # 빈줄

                    line = f.readline().replace(' ', '')
                    line = line.replace('\n', '').split('\t')[2:5]
                    if len(line) < 1:
                        break

                    if line[2][:6] == '$GPGGA':
                        GPGGA = line[2]
                        altitude = float(GPGGA.split(',')[9])
                        f.readline() # 빈줄
                    elif line[2][:6] == '$GPRMC':
                        GPRMC = line[2]
                        time = float(GPRMC.split(',')[1])
                        time = time + 90000  # 한국시간 +9시간
                        if time > 240000: time -= 240000  # 24시간 이상은 없으므로 초과하면 24시간 빼기

                        # gps 위경도 추출법 gprmc - > 도
                        latitude = float(GPRMC.split(',')[3])
                        latitude_1 = int(latitude / 100)
                        latitude_2 = (latitude - latitude_1 * 100) / 60
                        latitude = latitude_1 + latitude_2

                        longitude = float(GPRMC.split(',')[5])
                        longitude_1 = int(longitude / 100)
                        longitude_2 = (longitude - longitude_1 * 100) / 60
                        longitude = longitude_1 + longitude_2

                        speed = float(GPRMC.split(',')[7]) * 1.852  # knote to Km/h
                        heading = float(GPRMC.split(',')[8])
                        f.readline()  # 빈줄


                    line = f.readline().replace(' ', '')
                    line = line.replace('\n', '').split('\t')[2:5]
                    if len(line) < 1:
                        break
                    if line[2][:6] == '$GPRMC':
                        GPRMC = line[2]
                        time = float(GPRMC.split(',')[1])
                        time = time + 90000  # 한국시간 +9시간
                        if time > 240000: time -= 240000  # 24시간 이상은 없으므로 초과하면 24시간 빼기

                        # gps 위경도 추출법 gprmc - > 도
                        latitude = float(GPRMC.split(',')[3])
                        latitude_1 = int(latitude / 100)
                        latitude_2 = (latitude - latitude_1 * 100) / 60
                        latitude = latitude_1 + latitude_2

                        longitude = float(GPRMC.split(',')[5])
                        longitude_1 = int(longitude / 100)
                        longitude_2 = (longitude - longitude_1 * 100) / 60
                        longitude = longitude_1 + longitude_2

                        speed = float(GPRMC.split(',')[7]) * 1.852  # knote to Km/h
                        heading = float(GPRMC.split(',')[8])
                        f.readline() # 빈줄
                    elif line[2][:6] == '$GPGGA':
                        GPGGA = line[2]
                        altitude = float(GPGGA.split(',')[9])
                        f.readline() # 빈줄
                    wr.writerow([format(latitude,'.8f'), format(longitude,'.8f')])
                    print(latitude, longitude)

                    cnt += 1
                    line_empty_flag = 0
            CSV.close()
if __name__ == "__main__":
    function()