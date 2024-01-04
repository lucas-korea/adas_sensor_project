#gps 하나의 파일에 대해 경로를 그려보는 코드이다.
from matplotlib import pyplot as plt
import numpy as np
gps_bin_path = 'E:\\GPS_20230822_165813.bin'



roll = -1
pitch = -1
time = -1
latitude = -1
longitude = -1
speed = -1
heading = -1
altitude = -1
latitude_arr = []
longitude_arr = []
with open(gps_bin_path) as f:
    cnt = 0
    GPGGA = f.readline().replace(' ', '') #첫줄
    GPGGA = GPGGA.replace('\n', '').split('\t')[2:5]
    print(GPGGA)
    while(1):
        try :
            f.readline() #빈줄
            PASHR = f.readline().replace(' ', '')
            PASHR = PASHR.replace('\n', '').split('\t')[2:5]
            print(PASHR)
            roll = float(PASHR[2].split(',')[5])
            pitch = float(PASHR[2].split(',')[6])
            f.readline() #빈줄
            GPRMC = f.readline().replace(' ', '')
            print(GPRMC.replace('\n', '').split('\t')[2:5])
            time = float(GPRMC.split(',')[1])
            time = time + 90000 # 한국시간 +9시간
            if time >240000: time -= 240000 # 24시간 이상은 없으므로 초과하면 24시간 빼기
            # print(time)

            latitude = float(GPRMC.split(',')[3])
            latitude_1 = int(latitude / 100)
            latitude_2 = (latitude - latitude_1 * 100) / 60
            print(latitude - latitude_1 * 100, latitude_1, latitude_2)
            latitude = latitude_1 + latitude_2
            latitude_arr.append(latitude)
            longitude = float(GPRMC.split(',')[5])
            longitude_1 = int(longitude / 100)
            longitude_2 = (longitude - longitude_1 * 100) / 60
            longitude = longitude_1 + longitude_2
            longitude_arr.append(longitude)
            print(latitude, longitude)
            speed = float(GPRMC.split(',')[7]) * 1.852 # knote to Km/h
            heading = float(GPRMC.split(',')[8])
            f.readline() #빈줄
            GPGGA = f.readline().replace(' ', '')
            print(GPGGA.replace('\n', '').split('\t')[2:5])
            altitude = float(GPGGA.split(',')[9])

            yaw = "NULL"
            cnt += 1
        except:
            plt.plot(latitude_arr, longitude_arr)
            plt.show()
