import os
import numpy as np
import shutil

def matching_HighLow(match_list_path_list, lidar_ts_path, pcd_move_dir):
    range_ = 50
    for match_list in match_list_path_list:
        camera_match_frame = []
        lidar_match_stamp = []
        with open(match_list, 'r') as f:
            lines = f.readlines()
        for i in range(len(lines)):
            lidar_match_stamp.append(lines[i].split('\t')[2].replace('\n', ''))
        lidar_match_stamp_list = np.asarray(lidar_match_stamp, dtype=np.uint32)
        LowLidarList = [file for file in os.listdir(lidar_ts_path)
                        if file.startswith('_'.join(match_list.split('\\')[-1].split('_')[0:2]))
                        and file.endswith("L_under.pcd")]
        lidar_match_stamp_list = np.asarray(lidar_match_stamp, dtype=np.uint32)
        LowLidar_stamp_List = np.asarray(LowLidarList.split('_')[3], dtype=np.uint32)

        for i in range(len(LowLidarList)):
            mask_arr1 = lidar_match_stamp_list[:] > LowLidar_stamp_List[i] - range_
            mask_arr2 = lidar_match_stamp_list[:] <= LowLidar_stamp_List[i] + range_
            mask_all = np.logical_and(mask_arr1, mask_arr2)
            if len(lidar_match_stamp_list[mask_all]):
                shutil.copy2(lidar_ts_path + '\\' + LowLidarList[i], pcd_move_dir + '\\' + + LowLidarList[i])

if __name__ == '__main__':
    pass