import os
import numpy as np
from matplotlib import pyplot as plt
# import PointCloud2
#
# Pointcloud2 = []
#
#
# def to_pointcloud2(self, timestamp: float, pointcloud_filename: str) -> PointCloud2:
#     '''
#     reference : https://github.com/seoulrobotics/argos-evaluator/blob/master/scripts/utils/conversion.py
#     Definition: http://docs.ros.org/en/melodic/api/sensor_msgs/html/msg/PointCloud2.html
#     '''
#     lidar_file_path = os.path.join(
#         self.input_lidar_directory, pointcloud_filename)
#     pointcloud_np = np.fromfile(lidar_file_path, dtype=np.float32)
#     pointcloud_np_reshape = pointcloud_np.reshape(
#         (int(pointcloud_np.shape[0] / self.num_attribute), self.num_attribute))
#
#     pointcloud2 = PointCloud2()
#     pointcloud2.header = self.to_header(timestamp)
#
#     length_pointcloud = len(pointcloud_np_reshape)
#     pointcloud_data = pointcloud_np_reshape.astype(np.float32)
#     pointcloud2.height = 1
#     pointcloud2.width = length_pointcloud
#
#     pointcloud2.fields = self.pointfield
#     pointcloud2.is_bigendian = False
#     pointcloud2.point_step = self.point_step
#     pointcloud2.row_step = pointcloud2.point_step * length_pointcloud
#     pointcloud2.is_dense = True
#     pointcloud2.data = pointcloud_data.tostring()
#
#     return pointcloud2

def to_pointcloud():
    PATH = "C:\\Users\\jcy37\\Desktop\\과제\\3D High resolution 라이다\\라이다 평가 Tool sw 개발\\sunny[seoul robotics]\\south_to_west\\lidar\\2021_12_05_14_39_07_952.bin"
    lidar_file_path = PATH
    pointcloud_np = np.fromfile(lidar_file_path, dtype=np.float32)
    print(pointcloud_np.shape)
    pointcloud_np_reshape = pointcloud_np.reshape((int(pointcloud_np.shape[0] / 4), 4))
    pointcloud_data = pointcloud_np_reshape.astype(np.float32)
    return pointcloud_data
xyz_lim = 20

if __name__=="__main__":
    point_cloud = to_pointcloud()
    fig = plt.figure()
    plt.style.use(['dark_background'])
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(point_cloud[:, 0], point_cloud[:, 1], point_cloud[:, 2], 'b.')
    ax.set_xlim(-xyz_lim, xyz_lim)
    ax.set_ylim(-xyz_lim, xyz_lim)
    ax.set_zlim(-xyz_lim, xyz_lim)
    plt.show()