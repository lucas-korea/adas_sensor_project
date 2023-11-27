# 본 코드는 정제된 분할이미지 파일명을 이용해 all image 를 끌어온다
import numpy
import os
import csv
import shutil

file_list = os.listdir('E:\\15000set\\(to 김선임님)annotation and image restore dataset_15588frame')
yymmss = '20231108'
file_list = [file for file in file_list if file.startswith(yymmss)]

cnt = 0
for file in file_list:
    try:
        hhmmss = file.split('_')[1]
        frame = file.split('_')[2].split('.')[0]
        target_file = 'E:\\20231108,09_polardata\\polar\\All_angle\\' + yymmss + '_' + hhmmss + '_232000061_' + str(int(frame)) + '_all.png'
        print(target_file,'\t' ,cnt, '/' ,len(file_list))
        shutil.copy2(target_file, 'E:\\15000set\\annotation and image restore dataset_15588frame_all_angle\\' + file)
    except:
        print('#############################')
        print(target_file)

    cnt +=1
