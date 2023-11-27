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

def function():
    # gps_bin_path = select_file('select GPS bin file')[0]
    # match = open(select_file('select mathch file')[0])
    # gps_save_path = select_folder("select save folder")
    gps_bin_path = 'E:\\20230822_outside_human_test\\20230822_122959\\20230822_122959\\GPS_20230822_165813.bin'
    match= open('E:\\20230821_parkinglog_test\\checkerboard\\PCD\\20230821_162110_match_list.txt')
    gps_save_path = 'E:\\GPS'
    lidar_tick = []
    lines = match.readlines()
    for i in range(len(lines)):
        lidar_tick.append(lines[i].split('\t')[2].replace('\n', ''))
    with open(gps_bin_path) as f:
        cnt = 0
        for tick in lidar_tick:
            print(cnt ,'/', len(lidar_tick))
            tick = int(tick)
            line = f.readline().replace(' ', '')
            line = line.replace('\n', '').split('\t')[2:5]
            print(line, tick)
            while(1):
                if line[2][:6] == '$PASHR' and int(line[0]) > tick -10 and int(line[0]) < tick + 30:
                    break
                f.readline() # 빈줄
                line = f.readline().replace(' ', '')
                line = line.replace('\n', '').split('\t')[2:5]
            if line[2][:6] == '$PASHR' and int(line[0]) > tick -10 and int(line[0]) < tick + 30:
                print("here")
                roll = float(line[2].split(',')[5])
                pitch = float(line[2].split(',')[6])
                f.readline() # 빈줄
                GPRMC = f.readline()
                time = float(GPRMC.split(',')[1])
                time = time + 90000 # 한국시간 +9시간
                if time >240000: time -= 240000 # 24시간 이상은 없으므로 초과하면 24시간 빼기

                latitude = float(GPRMC.split(',')[3])
                latitude_1 = int(latitude/100)
                latitude_2 = (latitude - latitude_1 * 100)/60
                latitude = latitude_1 + latitude_2

                longitude = float(GPRMC.split(',')[5])
                longitude_1 = int(longitude/100)
                longitude_2 = (longitude - longitude_1 * 100)/60
                longitude = longitude_1 + longitude_2

                speed = float(GPRMC.split(',')[7]) * 1.852 # knote to Km/h
                heading = float(GPRMC.split(',')[8])
                f.readline() # 빈줄
                GPGGA = f.readline()
                altitude = float(GPGGA.split(',')[9])
                CSV = open(gps_save_path + '\\GPS_' + gps_bin_path.split('\\')[-2][2:] + '_' + '{0:04d}'.format(cnt) + '.csv', 'w',
                           encoding='utf-8', newline='')
                wr = csv.writer(CSV)
                wr.writerow([format(time, '.3f'), format(latitude,'.8f'), format(longitude,'.8f'), format(altitude,'.2f'), format(speed,'.2f'),
                             format(heading,'.2f'), format(roll,'.2f'), format(pitch,'.2f')])
                CSV.close()
                print( latitude, longitude)
                f.readline() # 빈줄
                cnt += 1
    match.close()
if __name__ == "__main__":
    function()