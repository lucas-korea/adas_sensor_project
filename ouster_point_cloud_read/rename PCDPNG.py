import os

PATH = "D:\\NIA3차\\NIA4차 대비 실도로 주행 sample PNGPCD"

list = [file for file in os.listdir(PATH) if os.path.splitext(file)[1] == '.png']
print(list)
cnt = 0
for file in list:
    os.rename(PATH + '\\' + file, PATH + '\\'+ str(cnt) + '_' + '_'.join(file.split('_')[0:2]) + '_' + file.split('_')[3])
    cnt += 1

list = [file for file in os.listdir(PATH) if os.path.splitext(file)[1] == '.pcd']
cnt = 0
for file in list:
    os.rename(PATH + '\\' + file, PATH + '\\' + str(cnt) + '_' + '_'.join(file.split('_')[0:2]) + '_' + file.split('_')[4])
    cnt += 1
