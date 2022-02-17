import os

PATH = 'G:\\0215_calib\\캘리브레이션용\\캘리브레이션용1\\캘리브레이션용'

list = [file for file in os.listdir(PATH) if file.split('.')[-1] == 'pcd']
for i in range(len(list)):
    # os.rename(PATH + '\\' + list[i], PATH + '\\' + '_'.join(list[i].split('_')[0:2]) + '_' + list[i].split('_')[4])
    os.rename(PATH + '\\' + list[i], PATH + '\\' + str(i) + '_' + list[i])
list = [file for file in os.listdir(PATH) if file.split('.')[-1] == 'png']
for i in range(len(list)):
    # os.rename(PATH + '\\' + list[i], PATH + '\\' + '_'.join(list[i].split('_')[0:2]) + '_' + list[i].split('_')[3])
    os.rename(PATH + '\\' + list[i], PATH + '\\' + str(i) + '_' + list[i])