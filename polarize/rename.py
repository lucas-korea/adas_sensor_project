import os
import shutil

path = 'E:\\최대인지거리 실험 lfit전달 데이터_2안'
# for (root, dirs, files) in os.walk(path):

file_list = os.listdir(path)
for file in file_list:
    os.rename(path + '\\' + file, path + '\\' + '_'.join(file.split('_')[:-1])  + '.png')
