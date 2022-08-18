import numpy as np
from open3d import *

def main():
    cloud = read_point_cloud("20210922_125016_000003_R.pcd") # Read the point cloud
    draw_geometries([cloud]) # Visualize the point cloud

if __name__ == "__main__":
    main()