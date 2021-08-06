import numpy as np
from matplotlib import pyplot as plt

angle = np.linspace(start=-11.25 * np.pi / 180, stop=11.25 * np.pi / 180, num=128)
cos_angle = np.cos(angle)
sin_angle = np.sin(angle)

def read_packets():
    packets = []
    for i in range(128):
        with open("ouster_packet_" + str(i), 'rb') as f:
            packets = packets + list(f.read())
    return packets

Measure_ID_bytes = []
frame_ID_bytes = []
Range_bytes = []
intensity_bytes = []
Range_list = []
intensity_list = []

PACKETS_COUNT = 128
BLOCKS = 16
CHANNEL = 128
BYTES = 24896
TICKS = 88

Azimuth = np.zeros((BLOCKS * PACKETS_COUNT, 1))
distance = np.zeros((BLOCKS * PACKETS_COUNT, CHANNEL)) # 128 = channel, 16 * 128 = block * packets
intensity = np.zeros((BLOCKS * PACKETS_COUNT, CHANNEL))

x = np.zeros(BLOCKS * PACKETS_COUNT * CHANNEL)
y = np.zeros(BLOCKS * PACKETS_COUNT * CHANNEL)
z = np.zeros(BLOCKS * PACKETS_COUNT * CHANNEL)

append_data = np.empty((1, 4), dtype=float)

def cal_lidar_pos():
    dist_cos_angle = distance * cos_angle
    x_ = dist_cos_angle * np.sin(Azimuth)
    y_ = dist_cos_angle * np.cos(Azimuth)
    z_ = distance * sin_angle
    return(np.stack([x_, y_, z_, intensity], axis=-1).reshape(-1, 4))


def main():
    data  = read_packets()
    index = 0
    Encoder = 0
    for i in range(PACKETS_COUNT * BLOCKS):
        index = index + 8 # timestamp
        # Measure_ID_bytes = data[index : index + 2]
        # Measure_ID = Measure_ID_bytes[1] * 256 + Measure_ID_bytes[0]
        # frame_ID_bytes = data[index + 2 : index + 4]
        # frame_ID = frame_ID_bytes[1] * 256 + frame_ID_bytes[0]
        # prev_Encoder = Encoder
        Encoder = data[index + 4 : index + 8]
        Encoder = (Encoder[3] * 256**3 + Encoder[2] * 256**2 + Encoder[1] * 256 + Encoder[0])
        Azimuth[i] = Encoder / TICKS / 1024 * 2 * np.pi
        # Encoder_diff = Encoder - prev_Encoder
        # print("Measure_ID : {}, frmae_ID : {}, Encoder : {}, Azimuth {}, tick diff {}".format(Measure_ID, frame_ID, Encoder, Azimuth[i], Encoder_diff))
        index = index + 8
        for j in range(CHANNEL):
            Range_bytes = data[index : index + 4]
            distance[i][j] = (Range_bytes[2] * 256**2 + Range_bytes[1] * 256 + Range_bytes[0]) / 1000
            intensity_bytes = data[index + 6 : index + 8]
            intensity[i][j] = (intensity_bytes[1] * 256 + intensity_bytes[0]) / 65535
            index = index + 12
        Block_stat = data[index : index + 4]
        index = index + 4
        if (Block_stat != [255, 255, 255, 255]):
            print("block status error!!")
            exit(1)
    # print(Azimuth, Azimuth.shape)
    # print(intensity, intensity.shape)
    # print(distance, distance.shape)
    print(((distance * cos_angle)*Azimuth).shape)
    point_cloud = cal_lidar_pos()
    print(point_cloud, point_cloud.shape)

    fig = plt.figure()
    plt.style.use(['dark_background'])
    ax = fig.add_subplot(111, projection='3d')
    xyz_lim = 10
    # ax.scatter(point_cloud[:, 0], point_cloud[:, 1], point_cloud[:, 2], s=0.2)

    ax.plot(point_cloud[:, 0], point_cloud[:, 1], point_cloud[:, 2], 'b.')
    ax.set_xlim(-xyz_lim, xyz_lim)
    ax.set_ylim(-xyz_lim, xyz_lim)
    ax.set_zlim(-xyz_lim, xyz_lim)
    plt.show()
if __name__ == '__main__':
    main()