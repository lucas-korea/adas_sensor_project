import pandas as pd
import csv
import numpy as np
import os

HEADER = '''\
# .PCD v0.7 - Point Cloud Data file format
VERSION 0.7
FIELDS x y z intensity
SIZE 4 4 4 4 
TYPE F F F F 
COUNT 1 1 1 1 
WIDTH {}
HEIGHT 1
VIEWPOINT 0 0 0 1 0 0 0
POINTS {}
DATA ascii
'''

def write_pcd(x, y, z, i, save_pcd_path):
    n = len(x)
    lines = []
    for j in range(n):
        lines.append('{:.6f} {:.6f} {:.6f} {:.6f}'.format(x[j], y[j], z[j], i[j])) # xyz, intesity를 lines에 추가
    with open(save_pcd_path, 'w') as f:
        f.write(HEADER.format(n, n)) #헤더에서 비어있던 WIDTH, POINTS 정보를 넣어준다
        f.write('\n'.join(lines)) # lines 배열을 파일에 쓰되 배열간 구분은 '\n'

def parse_xyzi_from_csv():
    dir_path = "D:\\7.14_LIDAR_CAMERA"
    file_list = os.listdir(dir_path)
    file_list = [file for file in file_list if file.endswith(".csv")]
    list =[]
    j = 0
    for file in file_list:
        x = []
        y = []
        z = []
        i = []
        print(file)
        f = open(dir_path + '\\' + file)
        rdr = csv.reader(f)
        for line in rdr:
            x.append(line[0])
            y.append(line[1])
            z.append(line[2])
            i.append(line[4])
        x.pop(0)
        y.pop(0)
        z.pop(0)
        i.pop(0)
        x = np.asarray(x).astype(np.float32)
        y = np.asarray(y).astype(np.float32)
        z = np.asarray(z).astype(np.float32)
        i = np.asarray(i).astype(np.float32)
        i = i / 65535
        write_pcd(x, y, z, i, dir_path + '\\' + file.rstrip('.csv') + '.pcd')
        j = j + 1
        f.close()

if __name__ == "__main__":
    parse_xyzi_from_csv()