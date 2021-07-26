import numpy as np
import struct
import sys

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

def bin_to_arr(binFileName):
    size_float = 4 # float 데이터의 크기는 4
    list_pcd = []
    with open(binFileName, "rb") as f:
        #======#
        byte = f.read(0xcb)
        #======#
        byte = f.read(size_float * 4) # x,y,z,i 데이터이므로 4개의 float을 읽어와 byte에 저장
        print(byte)
        while byte:
            x, y, z, intensity = struct.unpack("ffff", byte) # byte를 float 형태로 unpack
            list_pcd.append([x, y, z, intensity])
            byte = f.read(size_float * 4)
    np_pcd = np.asarray(list_pcd)
    return np_pcd

def write_pcd(points, save_pcd_path):
    n = len(points)
    lines = []
    for i in range(n):
        x, y, z, i = points[i]
        lines.append('{:.6f} {:.6f} {:.6f} {:.6f}'.format(x, y, z, i)) # xyz, intesity를 lines에 추가
    with open(save_pcd_path, 'w') as f:
        f.write(HEADER.format(n, n)) #헤더에서 비어있던 WIDTH, POINTS 정보를 넣어준다
        f.write('\n'.join(lines)) # lines 배열을 파일에 쓰되 배열간 구분은 '\n'

def main(binFileName, pcdFileName):
    write_pcd(bin_to_arr(binFileName), pcdFileName)

## argv[1] = 변환할 bin file 이름 및 경로
## argv[2] = 저장할 pcd file 이름 및 경로
if __name__ == "__main__":
    a = sys.argv[1]
    b = sys.argv[2]
    main(a, b)