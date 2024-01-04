import numpy as np
import ouster_header
import os
from tkinter import filedialog
from tkinter import messagebox
import struct
import time

Range_bytes = []
# ref_bytes = []
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

angle = np.zeros(128)
Azimuth_intrinsic = np.zeros(128)
beam_len = ouster_header.beam_intrinsics["lidar_origin_to_beam_origin_mm"] * 0.001

for header_i in range(128):
    angle[header_i] = ouster_header.beam_intrinsics["beam_altitude_angles"][header_i] * np.pi / 180
    Azimuth_intrinsic[header_i] = ouster_header.beam_intrinsics["beam_azimuth_angles"][header_i] * np.pi / 180


#data encoder 값이 0도 부터 시작하는지 확인 (NIA4차 에서는 pcd 접합부를 차량 후방으로 설정)
def find_start(data):
    index = 0
    index = index + 8  # timestamp
    encoder = data[index + 4: index + 8]
    encoder = (encoder[3] * 256 ** 3 + encoder[2] * 256 ** 2 + encoder[1] * 256 + encoder[0]) / TICKS / 1024 * 360
    if encoder == 0:
        return True
    else:
        return False


#data encoder 값이 180도 부터 시작하는지 확인
def find_180deg(data):
    index = 0
    index = index + 8  # timestamp
    encoder = data[index + 4: index + 8]
    encoder = (encoder[3] * 256 ** 3 + encoder[2] * 256 ** 2 + encoder[1] * 256 + encoder[0]) / TICKS / 1024 * 360
    if encoder == 180:
        return True
    else:
        return False

#연구용으로 npy 파일 생성하자.
def make_npyfile(lidar_list_dir_path, ymd, hms, frame_num, tick_ct):
    # image = np.zeros((924, 128))
    image = distance[50 :924+50]
    np.save(lidar_list_dir_path + "\\" + ymd + "_" + hms + "_" + '{0:06d}'.format(int(frame_num)) + "_" + '{0:06d}'.format(int(tick_ct)), image.T)

def select_lidar_list():
    files = filedialog.askopenfilenames(initialdir=os.getcwd(),
                                        title="파일을 선택 해 주세요",
                                        filetypes=(("*.txt", "*txt"), ("*.xls", "*xls"), ("*.csv", "*csv")))
    if files == '':
        messagebox.showwarning("경고", "파일을 추가 하세요")  # 파일 선택 안했을 때 메세지 출력
        exit(1)
    lidar_list_dir_path = ("\\".join(list(files)[0].split("/")[0: -1]))  # lidar 데이터 목록 위치 추출
    return files, lidar_list_dir_path


#lidar packet data 중 초반 쓸모없는 데이터 없애기
def crop_start_trash(f):
    while 1:
        try:
            f.read(2)  # 처음에 붙은 0x00 0x00은 없애는 작업
            f.read(50)  # katech header
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
    print(lidar_list_dir_path, files)
    with open(list(files)[0], 'r') as lidar_f:
        lidar_file_list = lidar_f.readlines()

    time1 = time.time()
    file_num = 0
    for file_name in lidar_file_list:

        packets = []
        file_name = file_name.replace("\n", "")
        print("now converting : ", file_name)
        packets_size = os.path.getsize(file_name) / 24948 / 64
        pcd_num = 0
        frame_number = -1
        frame_i = 0
        tick_ct = -1
        encoder_flag = False
        ymd = file_name.replace(".", "_").split("_")[-3]
        hms = file_name.replace(".", "_").split("_")[-2]
        with open(file_name, 'rb') as f:  # 취득데이터 이름
            crop_start_trash(f)
            error = 0
            while 1:
                encoder_dummy = -1
                try:
                    print(file_num+1,'/', len(lidar_file_list),'\t',pcd_num,"/",packets_size,"frame\t", format((packets_size - pcd_num)*(time.time() - time1)/60, '.2f'),"min left",
                          "   now converting : ", file_name)
                    time1 = time.time()
                    pcd_num = pcd_num + 1
                    for i in range(64):
                        f.read(2) # 처음에 붙은 0x00 0x00은 없애는 작업
                        header = f.read(50)  # katech header
                        print(header)
                        header = header.decode().replace(" ", "").split("\t")
                        data = list(f.read(24896))
                        ## encoder check ##
                        encoder = data[12: 16]
                        encoder = (encoder[3] * 256 ** 3 + encoder[2] * 256 ** 2 + encoder[1] * 256 + encoder[0]) / TICKS / 1024 * 360
                        if find_180deg(data):
                            frame_number = header[1]
                            tick_ct = header[2]
                        packets = packets + data
                        f.read(2)  # last enter
                        # encoder가 마지막 패킷을 감지하거나 혹은 encoder_dummy가 354.375인데 encoder가 5.625인, 그러니까 건너 뛴 상황에 break하여 모아둔 만큼만 pcd로.
                        if encoder == 354.375 or (encoder < encoder_dummy):
                            if i < 63:
                                print(error, '/', pcd_num)
                                error +=1
                            break
                        encoder_dummy = encoder
                    if (frame_i % 10 ==0 or 1):
                        parsing_packet(packets)
                        make_npyfile(lidar_list_dir_path, ymd, hms, frame_i, tick_ct)  # point cloud data를 pcd file로 변환
                    frame_i = frame_i + 1
                    packets = []
                except Exception as e:
                    print("error : ", e)
                    print("file finish")
                    break
        file_num = file_num + 1


# ouster lidar packet을 manual에 맞게 parsing
def parsing_packet(data):
    global Azimuth,Azimuth_sum,Azimuth_sum_low,distance,reflectivity
    Azimuth = np.zeros((BLOCKS * PACKETS_COUNT, CHANNEL))
    Azimuth_sum = np.zeros((BLOCKS * PACKETS_COUNT, CHANNEL))
    distance = np.zeros((BLOCKS * PACKETS_COUNT, CHANNEL))  # 128 = channel, 16 * 128 = block * packets
    index = 0
    horizontal_res = len(data) / 24896
    for i in range(int(horizontal_res+0.001) * BLOCKS): #본래는 1024여야 하나, 이제는 확실하지가 않다.
        index = index + 8  # timestamp
        Encoder = data[index + 4: index + 8]
        Encoder = (Encoder[3] * 256 ** 3 + Encoder[2] * 256 ** 2 + Encoder[1] * 256 + Encoder[0])
        Azimuth[i][:] = Encoder / TICKS / 1024 * 2 * np.pi
        Azimuth_sum[i][:] = Azimuth[i][:] + Azimuth_intrinsic
        index = index + 8
        for j in range(CHANNEL):
            Range_bytes = data[index: index + 4]
            real_i = i - (j % 4) * 4
            if real_i < 0:
                real_i += 1024
            distance[real_i][j] = (Range_bytes[2] * 256 ** 2 + Range_bytes[1] * 256 + Range_bytes[0]) / 1000
            index = index + 12
        block_stat = data[index: index + 4]
        index = index + 4
        if block_stat != [0xff, 0xff, 0xff, 0xff]:
            print("block status error!!")
            exit(1)


if __name__ == '__main__':
    # lidar_list_files = ["Z:\\2022 NIA 49-1 superresolution raw data\\220810\\src\\PCD_new\\202304271009_list.txt",
    #                        "Z:\\2022 NIA 49-1 superresolution raw data\\220812\\src\\PCD_new\\202304271009_list.txt",
    #                        "Z:\\2022 NIA 49-1 superresolution raw data\\220824\\src\\PCD_new\\202304271009_list.txt",
    #                        "Z:\\2022 NIA 49-1 superresolution raw data\\220825\\src\\PCD_new\\202304271012_list.txt",
    #                        "Z:\\2022 NIA 49-1 superresolution raw data\\220905\\src\\PCD_new\\202304271012_list.txt",
    #                        "Z:\\2022 NIA 49-1 superresolution raw data\\220906\\src\\PCD_new\\202304271016_list.txt",
    #                        "Z:\\2022 NIA 49-1 superresolution raw data\\220915\\src\\PCD_new\\202304271016_list.txt",
    #                        "Z:\\2022 NIA 49-1 superresolution raw data\\220916\\src\\PCD_new\\202304271016_list.txt",
    #                        "Z:\\2022 NIA 49-1 superresolution raw data\\220919\\src\\PCD_new\\202304271017_list.txt",
    #                        "Z:\\2022 NIA 49-1 superresolution raw data\\220922\\src\\PCD_new\\202304271017_list.txt",
    #                        "Z:\\2022 NIA 49-1 superresolution raw data\\221003\\src\\PCD_new\\202304271018_list.txt"]
    main()
