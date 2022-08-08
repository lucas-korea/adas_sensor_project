import os
import pandas as pd
import csv

def function():
    match = open("F:\\20220802 1cycle sample\\20220802_110747\\20220802_110747\\PCD\\20220802_110747_match_list.txt")
    lidar_tick = []
    lines = match.readlines()
    for i in range(len(lines)):
        lidar_tick.append(lines[i].split('\t')[-1].replace('\n', ''))
    roll = -1
    pitch = -1
    time = -1
    latitude = -1
    longitude = -1
    speed = -1
    heading = -1
    altitude = -1
    gps_path = "F:\\20220802 1cycle sample\\220802\\220802_110747_K\\gps"
    gps_bin_path = "F:\\20220802 1cycle sample\\20220802_110747\\20220802_110747\\GPS_20220802_110747.bin"
    with open(gps_bin_path) as f:
        cnt = 0
        for tick in lidar_tick:
            print(cnt ,'/', len(lidar_tick))
            # print(tick)
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
                time = float(GPRMC.split(',')[1])
                time = time + 90000 # 한국시간 +9시간
                if time >240000: time -= 240000 # 24시간 이상은 없으므로 초과하면 24시간 빼기
                # print(time)
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
                CSV = open(gps_path + '\\GPS_' + gps_bin_path.split('\\')[-2][2:] + '_' + '{0:04d}'.format(cnt) + '.csv', 'w',
                           encoding='utf-8', newline='')
                wr = csv.writer(CSV)
                wr.writerow([time, latitude, longitude, altitude, speed, heading, roll, pitch,yaw])
                CSV.close()
                f.readline()
                cnt += 1
    match.close()
if __name__ == "__main__":
    function()