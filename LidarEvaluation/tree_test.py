import cv2
import PCD2PNG
from PIL import Image

intensity_1, distance_1, real_1 = PCD2PNG.MakePCDimg("C:\\Users\\jcy37\\Downloads\\220824_171943_K (3)_태양광\\lidar_H\\1K_B08_O128_clear_sunset_summer_03010095.pcd")
intensity_2, distance_2, real_2 = PCD2PNG.MakePCDimg("C:\\Users\\jcy37\\Downloads\\220824_171943_K (3)_태양광\\lidar_H\\1K_B08_O128_clear_sunset_summer_03010096.pcd")
intensity_3, distance_3, real_3 = PCD2PNG.MakePCDimg("C:\\Users\\jcy37\\Downloads\\220824_171943_K (3)_태양광\\lidar_H\\1K_B08_O128_clear_sunset_summer_03010097.pcd")
intensity_4, distance_4, real_4 = PCD2PNG.MakePCDimg("C:\\Users\\jcy37\\Downloads\\220824_171943_K (3)_태양광\\lidar_H\\1K_B08_O128_clear_sunset_summer_03010098.pcd")

real_1 = cv2.applyColorMap(real_1, cv2.COLORMAP_JET)
cv2.imshow("real_1", real_1)
real_2 = cv2.applyColorMap(real_2, cv2.COLORMAP_JET)
cv2.imshow("real_2", real_2)
real_3 = cv2.applyColorMap(real_3, cv2.COLORMAP_JET)
cv2.imshow("real_3", real_3)
real_4 = cv2.applyColorMap(real_4, cv2.COLORMAP_JET)
cv2.imshow("real_4", real_4)

cv2.waitKey(0)