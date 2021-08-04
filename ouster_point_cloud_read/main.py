import numpy as np

vertical_angle = np.linspace(start=-11.25, stop=11.25, num=128)
print(vertical_angle)
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

Azimuth = np.zeros(16 * 128)
distance = np.zeros((16 * 128, 128)) # 128 = channel, 16 * 128 = block * packets
intensity = np.zeros((16 * 128, 128))
x = np.zeros(16 * 128 * 128)
y = np.zeros(16 * 128 * 128)
z = np.zeros(16 * 128 * 128)

def main():
    intensity_max = 0
    data  = read_packets()
    print(len(data), len(data)/24896)
    index = 0
    Encoder = 0
    for i in range(int(len(data)/24896 * 16)):
        index = index + 8 # timestamp
        Measure_ID_bytes = data[index : index + 2]
        Measure_ID = Measure_ID_bytes[1] * 256 + Measure_ID_bytes[0]
        frame_ID_bytes = data[index + 2 : index + 4]
        frame_ID = frame_ID_bytes[1] * 256 + frame_ID_bytes[0]
        prev_Encoder = Encoder
        Encoder = data[index + 4 : index + 8]
        Encoder = (Encoder[3] * 256**3 + Encoder[2] * 256**2 + Encoder[1] * 256 + Encoder[0])
        Encoder_diff = Encoder - prev_Encoder

        Azimuth[i] = Encoder / 88 / 1024 * 360
        print("Measure_ID : {}, frmae_ID : {}, Encoder : {}, Azimuth {}, tick diff {}".format(Measure_ID, frame_ID, Encoder, Azimuth, Encoder_diff))
        index = index + 8
        for j in range(128):
            Range_bytes = data[index : index + 4]
            distance[i][j] = (Range_bytes[2] * 256**2 + Range_bytes[1] * 256 + Range_bytes[0]) / 1000
            intensity_bytes = data[index + 6 : index + 8]
            intensity[i][j] = (intensity_bytes[1] * 256 + intensity_bytes[0]) / 65535
            # print("Range : {} meter, intensity : {:.4f}".format(Range, intensity))
            index = index + 12
        Block_stat = data[index : index + 4]
        index = index + 4
        if (Block_stat != [255, 255, 255, 255]):
            print("block status error!!")
            exit(1)

if __name__ == '__main__':
    main()