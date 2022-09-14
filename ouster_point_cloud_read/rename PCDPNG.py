import os

PATH = "I:\\20220824_calib\\calibration 쌍\\cam-lidar cali\\추가 데이터 3"

list = [file for file in os.listdir(PATH) if os.path.splitext(file)[1] == '.png']
print(list)
cnt = 0
for file in list:
    os.rename(PATH + '\\' + file, PATH + '\\' + '_'.join(file.split('.')[0].split('_')[0:3])  + '.png' )
    cnt += 1

list = [file for file in os.listdir(PATH) if os.path.splitext(file)[1] == '.pcd']
cnt = 0
for file in list:
    os.rename(PATH + '\\' + file, PATH + '\\' + '_'.join(file.split('.')[0].split('_')[0:3]) + '.pcd')
    cnt += 1
