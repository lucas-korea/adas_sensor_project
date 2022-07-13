import os
import numpy as np
import matplotlib.pyplot as plt
import time
import gc

np.set_printoptions(threshold=np.inf, linewidth=np.inf)
image_rows_low = 16 # 8, 16, 32
image_rows_high = 32 # 16, 32, 64
image_rows_full = 64
image_cols = 1024
np.set_printoptions(threshold=np.inf, linewidth=np.inf)
# ouster
ang_res_x = 360.0/float(image_cols) # horizontal resolution
ang_res_y = 22.5/float(image_rows_high-1) # vertical resolution
ang_start_y = 22.5/2 # bottom beam angle
sensor_noise = 0.03
max_range = 80.0
min_range = 2.0

upscaling_factor = int(image_rows_high / image_rows_low)

rowList = []
colList = []
for i in range(image_rows_high):
    rowList = np.append(rowList, np.ones(image_cols)*i)
    colList = np.append(colList, np.arange(image_cols))

verticalAngle = (np.float32(rowList * ang_res_y) - ang_start_y) * np.pi / 180.0
horizonAngle = - (np.float32(colList + 1 - (image_cols/2)) * ang_res_x + 90.0)
# print(horizonAngle.shape)
# exit(1)
intensity = rowList + colList / image_cols

if __name__ == "__main__":
    print("katech")
    PointClouds = np.load("result.npy")
    fig = plt.figure()
    plt.style.use(['dark_background'])
    ax = fig.add_subplot(111, projection='3d')
    xyz_lim = 30
    time1 = 0
    index = 0
    print(PointClouds.shape)
    for PointCloud in PointClouds:
        index += 1
        if index >= 10:
            break
        lengthList = PointCloud.reshape(image_rows_high*image_cols)
        print(lengthList)
        lengthList[lengthList > max_range] = 0.0
        lengthList[lengthList < min_range] = 0.0
        x = np.sin(horizonAngle) * np.cos(verticalAngle) * lengthList
        y = np.cos(horizonAngle) * np.cos(verticalAngle) * lengthList
        z = np.sin(verticalAngle) * lengthList

        beam_len = 13.762
        x = (lengthList - beam_len) * np.cos(verticalAngle) * np.cos(horizonAngle) + beam_len * np.cos(horizonAngle)
        y = ((lengthList - beam_len) * np.cos(verticalAngle) * np.sin(horizonAngle) + beam_len * np.sin(horizonAngle)) * -1
        z = (lengthList - beam_len) * np.sin(verticalAngle)
        print(PointCloud.shape)
        PointCloud = np.column_stack((x,y,z,intensity))
        PointCloud = np.delete(PointCloud, np.where(lengthList==0), axis=0)
        plt.cla()
        # 느리지만 옵션을 다양하게 줄 수 있는 함수
        # ax.scatter(point_cloud[:, 0], point_cloud[:, 1], point_cloud[:, 2], s=0.2, c=color_arr.intensity_color(point_cloud))
        # 빠르지만 시각화 옵션이 별로 없는 함수
        print(PointCloud.shape)
        ax.plot(PointCloud[:, 0], PointCloud[:, 1], PointCloud[:, 2], 'b.')
        ax.set_xlim(-xyz_lim, xyz_lim)
        ax.set_ylim(-xyz_lim, xyz_lim)
        ax.set_zlim(-xyz_lim, xyz_lim)
        # ax.set_xlabel('$X$', fontsize=20, rotation=150)
        # ax.set_ylabel('$Y$')
        # ax.set_zlabel(r'$\gamma$', fontsize=30, rotation=60)
        time2 = time.time()
        ax.text(-10, 0, 7, 'FPS:' + str(round(1 / (time2 - time1), 2))+ "    image# :" + str(index))
        time1 = time.time()
        # plt.axis('off')
        plt.pause(0.001)
        gc.collect()
    plt.show()