import os

PATH = "C:\\Users\\jcy37\\Documents\\카카오톡 받은 파일\\230905_front_lidar\\cam"

list = [file for file in os.listdir(PATH) if os.path.splitext(file)[1] == '.png']
print(list)
cnt = 0
for file in list:
    os.rename(PATH + '\\' + file, PATH + '\\' + '_'.join(file.split('.')[0].split('_')[1:4])  + '.png' )
    cnt += 1

PATH = "C:\\Users\\jcy37\\Documents\\카카오톡 받은 파일\\230905_front_lidar\\lidar"

list = [file for file in os.listdir(PATH) if os.path.splitext(file)[1] == '.pcd']
cnt = 0
for file in list:
    os.rename(PATH + '\\' + file, PATH + '\\' + '_'.join(file.split('.')[0].split('_')[1:4]) + '.pcd')
    cnt += 1
