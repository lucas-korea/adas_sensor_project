import os
import shutil

PCD_matched_path = 'E:\\20230825_cam_lidar_calibration\\PCD_matched'
PCD_matched_list = os.listdir(PCD_matched_path)

camera_path ='E:\\20230825_cam_lidar_calibration\\calibration_pair\\right_추가\\cam'
camera_list = os.listdir(camera_path)
for i in range(len(camera_list)):
    os.rename(camera_path + '\\' + camera_list[i], camera_path + '\\' + '_'.join(camera_list[i].split('.')[0].split('_')[0:3]) + '.png')
    file_name_frame = '_'.join(camera_list[i].split('.')[0].split('_')[0:3])
    pcd_matched_file_name = [file for file in PCD_matched_list if '_'.join(file.split('.')[0].split('_')[0:3]) == file_name_frame][-1]
    shutil.copy2(PCD_matched_path + '\\' + pcd_matched_file_name,'E:\\20230825_cam_lidar_calibration\\calibration_pair\\right_추가\\lidar')



# camera_path = 'E:\\20230825_cam_lidar_calibration\\calibration_pair\\rear\\camera'e
# camera_list = os.listdir(camera_path)
# print(camera_list)
# for i in range(len(camera_list)):
#     os.rename(camera_path + '\\' + camera_list[i], camera_path + '\\' + '_'.join(camera_list[i].split('.')[0].split('_')[0:3]) + '.png')
#     file_name_frame = '_'.join(camera_list[i].split('.')[0].split('_')[0:3])
#     pcd_matched_file_name = [file for file in PCD_matched_list if '_'.join(file.split('.')[0].split('_')[0:3]) == file_name_frame][-1]
#     shutil.copy2(PCD_matched_path + '\\' + pcd_matched_file_name, 'E:\\20230825_cam_lidar_calibration\\calibration_pair\\rear\\lidar')
#
# camera_path = 'E:\\20230825_cam_lidar_calibration\\calibration_pair\\front\\camera'
# camera_list = os.listdir(camera_path)
# for i in range(len(camera_list)):
#     os.rename(camera_path + '\\' + camera_list[i], camera_path + '\\' + '_'.join(camera_list[i].split('.')[0].split('_')[0:3]) + '.png')
#     file_name_frame = '_'.join(camera_list[i].split('.')[0].split('_')[0:3])
#     pcd_matched_file_name = [file for file in PCD_matched_list if '_'.join(file.split('.')[0].split('_')[0:3]) == file_name_frame][-1]
#     shutil.copy2(PCD_matched_path + '\\' + pcd_matched_file_name,'E:\\20230825_cam_lidar_calibration\\calibration_pair\\front\\lidar')
#
# camera_path = 'E:\\20230825_cam_lidar_calibration\\calibration_pair\\right\\camera'
# camera_list = os.listdir(camera_path)
# for i in range(len(camera_list)):
#     os.rename(camera_path + '\\' + camera_list[i], camera_path + '\\' + '_'.join(camera_list[i].split('.')[0].split('_')[0:3]) + '.png')
#     file_name_frame = '_'.join(camera_list[i].split('.')[0].split('_')[0:3])
#     pcd_matched_file_name = [file for file in PCD_matched_list if '_'.join(file.split('.')[0].split('_')[0:3]) == file_name_frame][-1]
#     shutil.copy2(PCD_matched_path + '\\' + pcd_matched_file_name, 'E:\\20230825_cam_lidar_calibration\\calibration_pair\\right\\lidar')
#
# camera_path ='E:\\20230825_cam_lidar_calibration\\calibration_pair\\left\\camera'
# camera_list = os.listdir(camera_path)
# for i in range(len(camera_list)):
#     os.rename(camera_path + '\\' + camera_list[i], camera_path + '\\' + '_'.join(camera_list[i].split('.')[0].split('_')[0:3]) + '.png')
#     file_name_frame = '_'.join(camera_list[i].split('.')[0].split('_')[0:3])
#     pcd_matched_file_name = [file for file in PCD_matched_list if '_'.join(file.split('.')[0].split('_')[0:3]) == file_name_frame][-1]
#     shutil.copy2(PCD_matched_path + '\\' + pcd_matched_file_name,'E:\\20230825_cam_lidar_calibration\\calibration_pair\\left\\lidar')
