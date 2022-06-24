import os
import numpy as np
import matplotlib.pyplot as plt
import time
import gc
import color_arr

np.set_printoptions(threshold=np.inf, linewidth=np.inf)
image_rows_low = 16 # 8, 16, 32
image_rows_high = 64 # 16, 32, 64
image_rows_full = 64
image_cols = 1024

# ouster
ang_res_x = 360.0/float(image_cols) # horizontal resolution
ang_res_y = 33.2/float(image_rows_high-1) # vertical resolution
ang_start_y = 16.6 # bottom beam angle
sensor_noise = 0.03
max_range = 80.0
min_range = 2.0

upscaling_factor = int(image_rows_high / image_rows_low)

rowList = []
colList = []
for i in range(image_rows_high):
    rowList = np.append(rowList, np.ones(image_cols)*i)
    colList = np.append(colList, np.arange(image_cols))

verticalAngle = np.float32(rowList * ang_res_y) - ang_start_y
horizonAngle = - np.float32(colList + 1 - (image_cols/2)) * ang_res_x + 90.0
intensity = rowList + colList / image_cols

if __name__ == "__main__":
    print("katech")
    PointClouds = np.load("ouster_range_image.npy")
    fig = plt.figure()
    plt.style.use(['dark_background'])
    ax = fig.add_subplot(111, projection='3d')
    xyz_lim = 10
    time1 = 0
    index = 0
    for thisimage in PointClouds:
        index += 1
        if index >= 100:break
        if len(thisimage.shape) == 3:
            thisimage = thisimage[:,:,0]

        lengthList = thisimage.reshape(image_rows_high*image_cols)
        lengthList[lengthList > max_range] = 0.0
        lengthList[lengthList < min_range] = 0.0

        x = np.sin(horizonAngle / 180.0 * np.pi) * np.cos(verticalAngle / 180.0 * np.pi) * lengthList
        y = np.cos(horizonAngle / 180.0 * np.pi) * np.cos(verticalAngle / 180.0 * np.pi) * lengthList
        z = np.sin(verticalAngle / 180.0 * np.pi) * lengthList

        points = np.column_stack((x, y, z, intensity))
        points = np.delete(points, np.where(lengthList == 0), axis=0)
        plt.cla()
        # 느리지만 옵션을 다양하게 줄 수 있는 함수
        # ax.scatter(points[:, 0], points[:, 1], points[:, 2], s=0.2, c=color_arr.intensity_color(points))
        # 빠르지만 시각화 옵션이 별로 없는 함수
        ax.plot(points[:, 0], points[:, 1], points[:, 2], 'b.')
        ax.set_xlim(-xyz_lim, xyz_lim)
        ax.set_ylim(-xyz_lim, xyz_lim)
        ax.set_zlim(-xyz_lim, xyz_lim)
        # ax.set_xlabel('$X$', fontsize=20, rotation=150)
        # ax.set_ylabel('$Y$')
        # ax.set_zlabel(r'$\gamma$', fontsize=30, rotation=60)
        time2 = time.time()
        ax.text(-10, 0, 7, 'FPS:' + str(round(1 / (time2 - time1), 2))+ "    image# :" + str(index))
        time1 = time.time()
        plt.axis('off')
        plt.pause(0.001)
        gc.collect()
    plt.show()
