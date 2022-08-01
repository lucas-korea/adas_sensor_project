import numpy as np
import os
import shutil

# path = "I:\\20220726test\\20220726_134553\\PNGmatched4"
# for file in (os.listdir(path)):
#        # print('_'.join(file.split('_')[0:3]))
#        # print('_{0:04d}'.format(int(file.split('_')[2].split('.')[0])))
#        new_name = '_'.join(file.split('_')[0:2]) + '_{0:04d}'.format(int(file.split('_')[2].split('.')[0])) + '_L.png'
#        os.rename(path + '\\' + file, path + '\\' + new_name)

path = "I:\\20220726test\\20220726_134553\\pcdmatched dummy low resolution"
for file in (os.listdir(path)):
       # print('_'.join(file.split('_')[0:3]))
       # print('_{0:04d}'.format(int(file.split('_')[2].split('.')[0])))
       new_name = '_'.join(file.split('_')[0:2]) + '_{0:04d}'.format(
              int(file.split('_')[2].split('.')[0])) + '_L.pcd'
       os.rename(path + '\\' + file, path + '\\' + new_name)