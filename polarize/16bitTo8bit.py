# 본 코드는 16비트 이미지를 8비트 이미지로 변환하는 코드이다

import os
import cv2
import numpy as np

files = os.listdir('E:\\lfit_lane')

cnt = 0
for file in files:
    print(file, '\t' , cnt)
    # Read the 16-bit image
    image_16bit = cv2.imread('E:\\lfit_lane\\' + file, cv2.IMREAD_UNCHANGED)

    # Convert the 16-bit image to an 8-bit image
    min_val = np.min(image_16bit)
    max_val = np.max(image_16bit)
    scaled_image = np.uint8((image_16bit - min_val) / (max_val - min_val) * 255)

    # Save the 8-bit image
    cv2.imwrite('E:\\lfit_lane_8bit\\'+ file, scaled_image)
    cnt += 1
