import numpy as np
import os
def main(lidar_ts_filelist, lidar_ts_path ,camera_ts_filelist, camera_ts_path):
    for file_i in range(len(lidar_ts_filelist)):
        with open(lidar_ts_path + '\\' + lidar_ts_filelist[file_i], 'r') as f:
            lidar_ts_list = f.readlines()
            lidar_ts_list = np.asarray(lidar_ts_list, dtype=np.uint32)
            camera_ts_file = [file for file in os.listdir(camera_ts_path) if (file.endswith(('_').join(lidar_ts_filelist[file_i].split('_')[0:2]) + ".bin"))]
        with open(camera_ts_path + '\\' + camera_ts_file[0], 'r') as f:
            camera_ts_frame_list = f.readlines()
            camera_ts_list = [0 for i in range(len(camera_ts_frame_list))]
            camera_fr_list = [0 for i in range(len(camera_ts_frame_list))]
            for k in range(len(camera_ts_frame_list)):
                camera_ts_list[k] = camera_ts_frame_list[k].split('_')[0]
                camera_fr_list[k] = camera_ts_frame_list[k].split('_')[1]
            camera_ts_list = np.asarray(camera_ts_list, dtype=np.uint32)
            camera_fr_list = np.asarray(camera_fr_list, dtype=np.uint32)


        k,j,q,y = 0, 0 ,0 ,0
        range_ = 17
        lidar_matched_list = []
        camera_matched_tick_list = []
        camera_matched_fr_list = []
        for i in range(len(lidar_ts_list)):
            mask_arr1 = camera_ts_list[:] > lidar_ts_list[i] - range_
            mask_arr2 = camera_ts_list[:] < lidar_ts_list[i] + range_
            mask_all = np.logical_and(mask_arr1, mask_arr2)
            tick = camera_ts_list[mask_all]
            frame = camera_fr_list[mask_all]

            if len(tick) == 0:
                q = q + 1
            elif len(tick) == 1:
                lidar_matched_list.append(lidar_ts_list[i])
                camera_matched_tick_list.append(tick[0])
                camera_matched_fr_list.append(frame[0])
                k = k + 1
            elif len(tick) == 2:
                lidar_matched_list.append(lidar_ts_list[i])
                camera_matched_tick_list.append(tick[0])
                camera_matched_fr_list.append(frame[0])
                j = j + 1
            else:
                y = y + 1
        # print("q, k, j , y = ", q, k, j , y)
        # print("matching : ", k + j + y)
        # print(lidar_ts_filelist[file_i])
        # print("len(camera_matched_tick_list), len(lidar_matched_list)", len(camera_matched_tick_list), len(lidar_matched_list))
        with open(lidar_ts_path + '\\' + ('_').join(lidar_ts_filelist[file_i].split('_')[0:2]) + "_match_list.txt", 'w') as f:
            for i in range(len(lidar_matched_list)):
                f.write(str(camera_matched_tick_list[i]) + '\t' + str(camera_matched_fr_list[i]) + '\t' +
                        str(lidar_matched_list[i]) + '\n')


if __name__ == "__main__":
    main()
