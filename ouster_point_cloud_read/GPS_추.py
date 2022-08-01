import os
import pandas as pd
import csv

def function():
    match = open("I:\\20220726test\\20220726_134553\\PCD\\20220726_134553_lidar_TimeStamp.txt")
    lidar_tick = []
    lines = match.readlines()
    for i in range(len(lines)):
        lidar_tick.append(lines[i].replace('\n', ''))
    roll = -1
    pitch = -1
    time = -1
    latitude = -1
    longitude = -1
    speed = -1
    heading = -1
    altitude = -1
    gps_path = "D:\\2022NIA2차 라이다 super resolution, denosing\\브레인컨테이너 샘플 데이터\\220726\\220726_134553_K\\gps"
    with open("I:\\20220726test\\20220726_134553\\GPS_20220726_134553.bin") as f:
        cnt = 0
        for tick in lidar_tick:
            print(tick)
            tick = int(tick)
            line = f.readline().replace(' ', '')
            line = line.replace('\n', '').split('\t')[2:5]
            while(1):
                if line[2][:6] == '$PASHR' and int(line[0]) > tick -10 and int(line[0]) < tick + 30:
                    break
                f.readline()
                line = f.readline().replace(' ', '')
                line = line.replace('\n', '').split('\t')[2:5]
            if line[2][:6] == '$PASHR' and int(line[0]) > tick -10 and int(line[0]) < tick + 30:
                roll = line[2].split(',')[5]
                pitch = line[2].split(',')[6]
                f.readline()
                GPRMC = f.readline()
                time = GPRMC.split(',')[1]
                print(time)
                latitude = GPRMC.split(',')[3]
                longitude = GPRMC.split(',')[5]
                speed = float(GPRMC.split(',')[7]) * 1.852 # knote to Km/h
                heading = GPRMC.split(',')[8]
                f.readline()
                f.readline()
                f.readline()
                GPGGA = f.readline()
                altitude = GPGGA.split(',')[9]
                yaw = heading
                CSV = open(gps_path + '\\GPS_' + '220726_134553' + '_' + '{0:04d}'.format(cnt) + '.csv', 'w',
                           encoding='utf-8', newline='')
                wr = csv.writer(CSV)
                wr.writerow([time, latitude, longitude, altitude, speed, heading, roll, pitch,yaw])
                CSV.close()
                f.readline()
                cnt += 1
    match.close()
if __name__ == "__main__":
    function()