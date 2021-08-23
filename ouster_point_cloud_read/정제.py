import numpy as np
from matplotlib import pyplot as plt
import ouster_header
import os
from tqdm import tqdm
import os
from tkinter import filedialog
from tkinter import messagebox
import struct

HEADER = '''# .PCD v0.7 - Point Cloud Data file format
VERSION 0.7
FIELDS x y z intensity
SIZE 4 4 4 4
TYPE F F F F
COUNT 1 1 1 1
WIDTH {}
HEIGHT 1
VIEWPOINT 0 0 0 1 0 0 0
POINTS {}
DATA binary
'''

HEADER_time = '''# .PCD v0.7 - Point Cloud Data file format
VERSION 0.7
FIELDS x y z intensity time
SIZE 4 4 4 4 4
TYPE F F F F U
COUNT 1 1 1 1 1
WIDTH {}
HEIGHT 1
VIEWPOINT 0 0 0 1 0 0 0
POINTS {}
DATA binary
'''

HEADER_ref = '''# .PCD v0.7 - Point Cloud Data file format
VERSION 0.7
FIELDS x y z intensity ref
SIZE 4 4 4 4 4
TYPE F F F F F 
COUNT 1 1 1 1 1
WIDTH {}
HEIGHT 1
VIEWPOINT 0 0 0 1 0 0 0
POINTS {}
DATA bin
'''

Range_bytes = []
ref_bytes = []
signal_photon_bytes = []
Range_list = []
ref_list = []
signal_photon_list = []

PACKETS_COUNT = 64
BLOCKS = 16
CHANNEL = 128
BYTES = 24896
TICKS = 88
START_PACKET = 700

Azimuth = np.zeros((BLOCKS * PACKETS_COUNT, CHANNEL))
Azimuth_sum = np.zeros((BLOCKS * PACKETS_COUNT, CHANNEL))
distance = np.zeros((BLOCKS * PACKETS_COUNT, CHANNEL))  # 128 = channel, 16 * 128 = block * packets
reflectivity = np.zeros((BLOCKS * PACKETS_COUNT, CHANNEL))
signal_photon = np.zeros((BLOCKS * PACKETS_COUNT, CHANNEL))
timestamp = np.zeros((BLOCKS * PACKETS_COUNT, CHANNEL))

x = np.zeros(BLOCKS * PACKETS_COUNT * CHANNEL)
y = np.zeros(BLOCKS * PACKETS_COUNT * CHANNEL)
z = np.zeros(BLOCKS * PACKETS_COUNT * CHANNEL)

angle = np.zeros(128)
Azimuth_intrinsic = np.zeros(128)
beam_len = ouster_header.list["lidar_origin_to_beam_origin_mm"] * 0.001

for header_i in range(128):
    angle[header_i] = ouster_header.list["beam_altitude_angles"][header_i] * np.pi / 180
    Azimuth_intrinsic[header_i] = ouster_header.list["beam_azimuth_angles"][header_i] * np.pi / 180

def find_start(data):
    index = 0
    index = index + 8  # timestamp
    encoder = data[index + 4: index + 8]
    encoder = (encoder[3] * 256 ** 3 + encoder[2] * 256 ** 2 + encoder[1] * 256 + encoder[0]) / TICKS / 1024 * 360
    if encoder == 309.375:
        return True
    else:
        return False

def find_0deg(data):
    index = 0
    index = index + 8  # timestamp
    encoder = data[index + 4: index + 8]
    encoder = (encoder[3] * 256 ** 3 + encoder[2] * 256 ** 2 + encoder[1] * 256 + encoder[0]) / TICKS / 1024 * 360
    if encoder == 0:
        return True
    else:
        return False

def cal_lidar_pos():
    x_ = (distance - beam_len) * np.cos(angle) * np.cos(Azimuth_sum) + beam_len * np.cos(Azimuth)
    y_ = ((distance - beam_len) * np.cos(angle) * np.sin(Azimuth_sum) + beam_len * np.sin(Azimuth)) * -1
    z_ = (distance - beam_len) * np.sin(angle)
    # return np.stack([x_, y_, z_, reflectivity], axis=-1).reshape(-1, 4)
    return np.stack([x_, y_, z_, reflectivity, timestamp], axis=-1).reshape(-1, 5)


def make_bin_PCDfile(point_cloud, lidar_list_dir_path, ymd, hms, frame_num):
    with open(lidar_list_dir_path + "\\" + ymd + "_" + hms + "_" + '{0:06d}'.format(int(frame_num)) + ".pcd", 'w') as f:  # 생성될 pcd file 이름
        f.write(HEADER.format(len(point_cloud), len(point_cloud))) # 미리 지정한 header를 pcd file 위에 write
    with open(lidar_list_dir_path + "\\" + ymd + "_" + hms + "_" + '{0:06d}'.format(int(frame_num)) + ".pcd", 'ab') as f:
        for i in range(len(point_cloud)):
            for j in range(3):
                point_cloud[i][j] = round(point_cloud[i][j], 4)
            f.write(struct.pack("ffff", point_cloud[i][0], point_cloud[i][1], point_cloud[i][2], point_cloud[i][3]))
            # f.write(str(point_cloud[i][0]) + ' ' + str(point_cloud[i][1]) + ' ' + str(point_cloud[i][2]) + ' ' + str(
            #     point_cloud[i][3]) + '\n')


def make_ascii_PCDfile(point_cloud, lidar_list_dir_path, ymd, hms, frame_num):
    with open(lidar_list_dir_path + "\\" + ymd + "_" + hms + "_" + '{0:06d}'.format(int(frame_num)) + "ts.pcd", 'w') as f:  # 생성될 pcd file 이름
        f.write(HEADER.format(len(point_cloud), len(point_cloud))) # 미리 지정한 header를 pcd file 위에 write
    with open(lidar_list_dir_path + "\\" + ymd + "_" + hms + "_" + '{0:06d}'.format(int(frame_num)) + "ts.pcd", 'a') as f:
        for i in range(len(point_cloud)):
            for j in range(3):
                point_cloud[i][j] = round(point_cloud[i][j], 4)
            f.write(str(point_cloud[i][0]) + ' ' + str(point_cloud[i][1]) + ' ' + str(point_cloud[i][2])
                    + ' ' + str(point_cloud[i][3]) + ' ' + str(point_cloud[i][4]) + '\n')


def rm_zero_point(point_cloud):  # xyz가 전부 0이거나 Intensity = 0인 경우를 삭제
    mask_array1 = point_cloud[:, 0] == 0
    mask_array2 = point_cloud[:, 1] == 0
    mask_array3 = point_cloud[:, 2] == 0
    mask_array4 = point_cloud[:, 3] == 0
    mask_all = np.logical_and(mask_array1, mask_array2)
    mask_all = np.logical_and(mask_all, mask_array3)
    mask_all = np.logical_or(mask_all, mask_array4)
    point_cloud = point_cloud[~mask_all]
    return point_cloud


def select_lidar_list():
    files = filedialog.askopenfilenames(initialdir="\\",
                                        title="파일을 선택 해 주세요",
                                        filetypes=(("*.txt", "*txt"), ("*.xls", "*xls"), ("*.csv", "*csv")))
    if files == '':
        messagebox.showwarning("경고", "파일을 추가 하세요")  # 파일 선택 안했을 때 메세지 출력
        exit(1)
    lidar_list_dir_path = ("\\".join(list(files)[0].split("/")[0: -1]))  # lidar 데이터 목록 위치 추출
    return files, lidar_list_dir_path


def crop_start_trash(f):
    while 1:
        try:
            f.read(2)  # 처음에 붙은 0x00 0x00은 없애는 작업
            f.read(48)  # katech header
            if find_start(list(f.read(24896))):
                f.read(2)  # last enter
                break
            f.read(2)  # last enter
        except Exception as e:
            print("error : ", e)
            print("file didn't started. finish")
            break


def main():
    files, lidar_list_dir_path = select_lidar_list()
    print(lidar_list_dir_path)
    with open(list(files)[0], 'r') as lidar_f:
        lidar_file_list = lidar_f.readlines()
    for file_name in lidar_file_list:
        packets = []
        file_name = file_name.replace("\n", "")
        print("now converting : ", file_name)
        packets_size = os.path.getsize(file_name) / 24948 / 64
        pcd_num = 0
        image_number = -1
        frame_i = 0
        ymd = file_name.replace(".", "_").split("_")[-3]
        hms = file_name.replace(".", "_").split("_")[-2]
        if os.path.isfile('image_frame_number.txt'):
            os.remove('image_frame_number.txt')
        with open(file_name, 'rb') as f:  # 취득데이터 이름
            crop_start_trash(f)
            while 1:
                try:
                    print(pcd_num,"/",packets_size, "now converting : ", file_name)
                    # print(format(pcd_num / packets_size, "5.2f"),"/", 100)
                    pcd_num = pcd_num + 1
                    for i in range(64):
                        f.read(2)  # 처음에 붙은 0x00 0x00은 없애는 작업
                        header = f.read(48)  # katech header
                        data = list(f.read(24896))
                        if find_0deg(data):
                            header = header.decode().replace(" ", "").split("\t")
                            image_number = header[1]
                        packets = packets + data
                        f.read(2)  # last enter
                    if frame_i % 10 == 0 or frame_i % 10 == 3 or frame_i % 10 == 6 or 1:
                        parsing_packet(packets)
                        # point_cloud = cal_lidar_pos()  # global로 선언된 distance, reflectivity, signal_photon, Azimuth를 조합하여 point cloud data 생성
                        # point_cloud = rm_zero_point(point_cloud)
                        with open(lidar_list_dir_path + "\\" + "image_frame_number.txt", 'a') as frame_f:
                            frame_f.write(image_number)
                            frame_f.write('\n')
                        # make_ascii_PCDfile(point_cloud, lidar_list_dir_path, ymd, hms, image_number)  # point cloud data를 pcd file로 변환
                    frame_i = frame_i + 1
                    packets = []
                except Exception as e:
                    print("error : ", e)
                    print("file finish")
                    break


def parsing_packet(data):
    index = 0
    global timestamp
    for i in range(PACKETS_COUNT * BLOCKS):
        t_bytes = data[index : index + 8]
        timestamp[i][0] = t_bytes[7] * 256 ** 7 + t_bytes[6] * 256 ** 6 + t_bytes[5] * 256 ** 5 + t_bytes[4] * 256 ** 4 + \
                          t_bytes[3] * 256 ** 3 + t_bytes[2] * 256 ** 2 + t_bytes[1] * 256 + t_bytes[0]
        if i == 0:
            with open("timestamp.txt", 'a') as f:
                f.write(str(timestamp[i][0]) + '\n')
                break
        index = index + 8  # timestamp
        Encoder = data[index + 4: index + 8]
        Encoder = (Encoder[3] * 256 ** 3 + Encoder[2] * 256 ** 2 + Encoder[1] * 256 + Encoder[0])
        Azimuth[i][:] = Encoder / TICKS / 1024 * 2 * np.pi
        Azimuth_sum[i][:] = Azimuth[i][:] + Azimuth_intrinsic
        index = index + 8
        for j in range(CHANNEL):
            timestamp[i][j] = timestamp[i][0]
            Range_bytes = data[index: index + 4]
            ref_bytes = data[index + 4 : index + 6]
            # signal_photon_bytes = data[index + 6: index + 8]
            distance[i][j] = (Range_bytes[2] * 256 ** 2 + Range_bytes[1] * 256 + Range_bytes[0]) / 1000
            reflectivity[i][j] = ref_bytes[1] * 256 + ref_bytes[0]
            # signal_photon[i][j] = (signal_photon_bytes[1] * 256 + signal_photon_bytes[0]) #/ 65535
            index = index + 12
        block_stat = data[index: index + 4]
        index = index + 4
        if block_stat != [0xff, 0xff, 0xff, 0xff]:
            print("block status error!!")
            exit(1)


if __name__ == '__main__':
    main()
