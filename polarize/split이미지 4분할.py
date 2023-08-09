import os
import shutil
import numpy as np
import cv2

path = "C:\\Users\\jcy37\\Pictures"
img = cv2.imread(path + '\\' + '1111.bmp', -1)
height_ = img.shape[0]
length_ = img.shape[1]
new_image1 = np.zeros((int(height_ / 2), int(length_ / 2), 3), dtype=np.uint8)
new_image2 = np.zeros((int(height_ / 2), int(length_ / 2), 3), dtype=np.uint8)
new_image3 = np.zeros((int(height_ / 2), int(length_ / 2), 3), dtype=np.uint8)
new_image4 = np.zeros((int(height_ / 2), int(length_ / 2), 3), dtype=np.uint8)
for i in range(int(height_)):
    for j in range(int(length_)):
