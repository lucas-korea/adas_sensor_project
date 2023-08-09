import PolarizeCam
import os
import matplotlib.pyplot as plt
import cv2
import numpy as np


img = cv2.imread("Y:\\PolarRealRoadDataBMP\\selected data\\raw_polar\\20230418_095505_21159646_file0_3150.bmp", -1)
image90, image45, image135, image0 = PolarizeCam.polar_analysis(img, "Y:\\PolarRealRoadDataBMP\\selected data")
# plt.show()
cv2.imwrite("image90.bmp", image90)
cv2.imwrite("image45.bmp", image45)
cv2.imwrite("image135.bmp", image135)
cv2.imwrite("image0.bmp", image0)
