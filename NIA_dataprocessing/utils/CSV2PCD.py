import numpy as np
import pandas as pd
import os
import glob
import pcd추출_ver4 as HEADER_
import struct

def CSV2PCD(file):
    CSVData = pd.read_csv(file)
    LEN = len(CSVData)
    if LEN == 131072:
        print(file)
        make_bin_PCDfile(file, CSVData)

#bin style로 생성
def make_bin_PCDfile(file, CSVData):
    with open(file[:-4] + ".pcd", 'w') as f:  # 생성될 pcd file 이름
        f.write(HEADER_.HEADER.format(len(CSVData), len(CSVData))) # 미리 지정한 header를 pcd file 위에 write
    with open(file[:-4] + ".pcd", 'ab') as f:
        for i in range(len(CSVData)):
            f.write(struct.pack("ffff", CSVData['Point:0'][i], CSVData['Point:1'][i], CSVData['Point:2'][i], CSVData['Reflectivity'][i]))

if __name__ == '__main__':
    files = glob.glob('C:\\Users\\jcy37\\PycharmProjects\\ouster_viewer_3layer\\newjig*.csv')
    for file in files:
        CSV2PCD(file)
