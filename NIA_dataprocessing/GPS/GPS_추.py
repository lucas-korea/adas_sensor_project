import os
import pandas as pd
import csv

def function():
    root_path = "F:\\20220802 1cycle sample\\20220802_110747\\20220802_110747\\"
    match = open(root_path + "PCD\\20220802_110747_match_list.txt")
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
    gps_path = root_path + "GPS_test"
    gps_bin_path = root_path + "GPS_20220802_110747.bin"
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
                roll = float(line[2].split(',')[5])
                pitch = float(line[2].split(',')[6])
                f.readline()
                GPRMC = f.readline()
                time = float(GPRMC.split(',')[1])
                time = time + 90000 # 한국시간 +9시간
                if time >240000: time -= 240000 # 24시간 이상은 없으므로 초과하면 24시간 빼기
                # print(time)

                latitude = float(GPRMC.split(',')[3])
                latitude_1 = int(latitude/100)
                latitude_2 = int(latitude - latitude_1 * 100)/60
                latitude_3 = (latitude - latitude_1 * 100 - latitude_2 * 60) * 100 / 3600
                latitude = latitude_1 + latitude_2 + latitude_3

                longitude = float(GPRMC.split(',')[5])
                longitude_1 = int(longitude/100)
                longitude_2 = int(longitude - longitude_1 * 100)/60
                longitude_3 = (longitude - longitude_1 * 100 - longitude_2 * 60) * 100 / 3600
                longitude = longitude_1 + longitude_2 + longitude_3

                speed = float(GPRMC.split(',')[7]) * 1.852 # knote to Km/h
                heading = float(GPRMC.split(',')[8])
                f.readline()
                f.readline()
                f.readline()
                GPGGA = f.readline()
                altitude = float(GPGGA.split(',')[9])
                yaw = "NULL"
                CSV = open(gps_path + '\\GPS_' + gps_bin_path.split('\\')[-2][2:] + '_' + '{0:04d}'.format(cnt) + '.csv', 'w',
                           encoding='utf-8', newline='')
                wr = csv.writer(CSV)
                wr.writerow([format(time, '.3f'), format(latitude,'.8f'), format(longitude,'.8f'), format(altitude,'.2f'), format(speed,'.2f'),
                             format(heading,'.2f'), format(roll,'.2f'), format(pitch,'.2f'),yaw])
                CSV.close()
                f.readline()
                cnt += 1
    match.close()
if __name__ == "__main__":
    function()