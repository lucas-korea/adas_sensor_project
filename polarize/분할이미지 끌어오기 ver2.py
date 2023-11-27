
# 본 코드는 정제된 all angle 이미지에서, 엑셀파일을 참고하여 4분할 이미지 중 하나를 끌어오는 코드이다
# file for file in ... minimize finding process, upgrade speed version
import numpy
import os
import csv
import shutil
# files_path = "E:\\20231108_polardata\\정제된 데이터"
# file = [file for file in os.listdir(files_path) if file.endswith('png') or file.endswith('bmp')]

f = open("Z:\\katech\\polar_data\\annotation data prosessed\\file_list.csv", "r")
rdr = csv.reader(f)
cnt =0
for line in rdr:  #csv file을 한줄씩 리스트형식([])으로 읽어들인다..
    if cnt % 2 == 0:
        target_file_basename = '_'.join(line[0].split('_')[0:4]) # 연월일_시분초_프레임 이름을 가져온다
        if target_file_basename.split('_')[0] == '20231106':
            print(target_file_basename,'\t' ,cnt)
            try:
                if line[1] == '1': #0도
                    target_file = 'Z:\\katech\\polar_data\\20231106_old\\polar\\0\\' + target_file_basename + '_0.png'
                    shutil.copy2(target_file,
                                 'E:\\15000장\\preprocessed data2\\' +
                                 '_'.join(target_file_basename.split('_')[0:2]) + '_' + '{:0>6}'.format(target_file_basename.split('_')[-1])+'.png')
                elif line[1] == '2': #45도
                    target_file = 'Z:\\katech\\polar_data\\20231106_old\\polar\\45\\' + target_file_basename + '_45.png'
                    shutil.copy2(target_file,
                                 'E:\\15000장\\preprocessed data2\\' +
                                 '_'.join(target_file_basename.split('_')[0:2]) + '_' + '{:0>6}'.format(target_file_basename.split('_')[-1])+'.png')
                elif line[1] == '3': #90도
                    target_file = 'Z:\\katech\\polar_data\\20231106_old\\polar\\90\\' + target_file_basename + '_90.png'
                    shutil.copy2(target_file,
                                 'E:\\15000장\\preprocessed data2\\' +
                                 '_'.join(target_file_basename.split('_')[0:2]) + '_' + '{:0>6}'.format(target_file_basename.split('_')[-1])+'.png')
                elif line[1] == '4':  # 135도
                    target_file = 'Z:\\katech\\polar_data\\20231106_old\\polar\\135\\' + target_file_basename + '_135.png'
                    shutil.copy2(target_file,
                                 'E:\\15000장\\preprocessed data2\\' +
                                 '_'.join(target_file_basename.split('_')[0:2]) + '_' + '{:0>6}'.format(target_file_basename.split('_')[-1])+'.png')
            except:
                print("error")
    cnt +=1
f.close()
