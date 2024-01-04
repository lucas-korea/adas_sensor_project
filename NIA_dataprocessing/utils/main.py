import numpy as np
from matplotlib import pyplot as plt
import ouster_header

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
DATA ascii
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
DATA ascii
'''

angle = np.zeros(128)
Azimuth_intrinsic = np.zeros(128)
beam_len = ouster_header.list["lidar_origin_to_beam_origin_mm"] * 0.001

for i in range(128):
    angle[i] = ouster_header.list["beam_altitude_angles"][i] * np.pi / 180
    Azimuth_intrinsic[i] = ouster_header.list["beam_azimuth_angles"][i] * np.pi / 180

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

x = np.zeros(BLOCKS * PACKETS_COUNT * CHANNEL)
y = np.zeros(BLOCKS * PACKETS_COUNT * CHANNEL)
z = np.zeros(BLOCKS * PACKETS_COUNT * CHANNEL)


def read_packets(): # 1 패킷 1 파일 형태의 데이터들을 모아서 읽기j
    print("read packets...")
    packets = []
    for i in range(START_PACKET, START_PACKET + PACKETS_COUNT):
        with open("data\\ouster_packet_" + str(i), 'rb') as f:
            packets = packets + list(f.read())
    return packets


def read_packets2(): # labview에서 읽어오듯 1 파일에 다수의 패킷이 들어있는 데이터를 읽기
    print("read packets...")
    packets = []
    with open("Lidar_20210809_155001.txt", 'rb') as f: # 취득데이터 이름
        for i in range(64):
            f.read(2)  # 처음에 붙은 0x00 0x00은 없애는 작업
            f.read(48) # katech header
            packets = packets + list(f.read(24896))
            f.read(2)  # last enter
    return packets


def cal_lidar_pos():
    print("calculate point cloud...")
    x_ =  (distance - beam_len) * np.cos(angle) * np.cos(Azimuth_sum) + beam_len * np.cos(Azimuth)
    y_ = ((distance - beam_len) * np.cos(angle) * np.sin(Azimuth_sum) + beam_len * np.sin(Azimuth)) * -1
    z_ =  (distance - beam_len) * np.sin(angle)

    # x_ = (distance) * np.cos(angle) * np.cos(Azimuth_sum)
    # y_ = (distance) * np.cos(angle) * np.sin(Azimuth_sum) * -1
    # z_ = (distance) * np.sin(angle)
    return (np.stack([x_, y_, z_, signal_photon, reflectivity], axis=-1).reshape(-1, 5))


def rm_zero_point(point_cloud):  ## xyz가 전부 0이거나 Intensity = 0인 경우를 삭제
    mask_array1 = point_cloud[:, 0] == 0
    mask_array2 = point_cloud[:, 1] == 0
    mask_array3 = point_cloud[:, 2] == 0
    mask_array4 = point_cloud[:, 3] == 0
    mask_all = np.logical_and(mask_array1, mask_array2)
    mask_all = np.logical_and(mask_all, mask_array3)
    mask_all = np.logical_or(mask_all, mask_array4)
    point_cloud = point_cloud[~mask_all]
    return point_cloud


def main():
    print("main start...")
    data = read_packets()
    index = 0
    for i in range(PACKETS_COUNT * BLOCKS):
        index = index + 8  # timestamp
        Encoder = data[index + 4: index + 8]
        Encoder = (Encoder[3] * 256 ** 3 + Encoder[2] * 256 ** 2 + Encoder[1] * 256 + Encoder[0])
        Azimuth[i][:] = Encoder / TICKS / 1024 * 2 * np.pi
        Azimuth_sum[i][:] = Azimuth[i][:] + Azimuth_intrinsic
        index = index + 8
        for j in range(CHANNEL):
            Range_bytes = data[index: index + 4]
            ref_bytes = data[index + 4 : index + 6]
            signal_photon_bytes = data[index + 6: index + 8]
            distance[i][j] = (Range_bytes[2] * 256 ** 2 + Range_bytes[1] * 256 + Range_bytes[0]) / 1000
            reflectivity[i][j] = ref_bytes[1] * 256 + ref_bytes[0]
            signal_photon[i][j] = (signal_photon_bytes[1] * 256 + signal_photon_bytes[0]) / 65535
            index = index + 12
        block_stat = data[index: index + 4]
        index = index + 4
        if (block_stat != [0xff, 0xff, 0xff, 0xff]):
            print("block status error!!")
            exit(1)
    point_cloud = cal_lidar_pos() # global로 선언된 distance, reflectivity, signal_photon, Azimuth를 조합하여 point cloud data 생성
    make_PCDfile(point_cloud) # point cloud data를 pcd file로 변환

def figure_PCD(point_cloud):
    fig = plt.figure()
    plt.style.use(['dark_background'])
    ax = fig.add_subplot(111, projection='3d')
    xyz_lim = 20
    # ax.scatter(point_cloud[:, 0], point_cloud[:, 1], point_cloud[:, 2], s=0.2)
    ax.plot(point_cloud[:, 0], point_cloud[:, 1], point_cloud[:, 2], 'b.')
    ax.set_xlim(-xyz_lim, xyz_lim)
    ax.set_ylim(-xyz_lim, xyz_lim)
    ax.set_zlim(-xyz_lim, xyz_lim)
    plt.show()


def make_PCDfile(point_cloud):
    with open("test.pcd", 'w') as f: # 생성될 pcd file 이름
        f.write(HEADER_ref.format(len(point_cloud), len(point_cloud))) # 미리 지정한 header를 pcd file 위에 write
        for i in range(len(point_cloud)):
            for j in range(3):
                point_cloud[i][j] = round(point_cloud[i][j], 4)
            f.write(str(point_cloud[i][0]) + ' ' + str(point_cloud[i][1]) + ' ' + str(point_cloud[i][2]) + ' ' + str(
                point_cloud[i][3]) + ' ' + str(point_cloud[i][4])+ '\n')
    print("makeing PCD file done!!!")


if __name__ == '__main__':
    main()
