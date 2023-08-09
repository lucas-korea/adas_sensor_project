import os
import shutil
import numpy as np
import cv2

# path = 'Y:\\PolarRealRoadDataBMP\\selected data\\raw_RGB'
# RGB_list = os.listdir(path)
# for file in RGB_list:
#     img = cv2.imread(path + '\\' + file, -1)
#     height_ = img.shape[0]
#     length_ = img.shape[1]
#     new_image = np.zeros((int(height_ / 2), int(length_ / 2), 3), dtype=np.uint8)
#     for i in range(int(height_ / 2)):
#         for j in range(int(length_ / 2)):
#             new_image[i][j][2] = img[i*2][j*2]
#             new_image[i][j][1] = (img[i*2+1][j*2]/2 + img[i*2][j*2+1]/2)
#             new_image[i][j][0] = img[i*2+1][j*2+1]
#     cv2.imshow("test", new_image)
#     cv2.waitKey(10)
#     cv2.imwrite('Y:\\PolarRealRoadDataBMP\\selected data\\raw_RGB_demosicing\\' + file, new_image)


path = 'Z:\\PolarRealRoadDataBMP\\selected data\\raw_polar'
polar_list = os.listdir(path)
cnt = 1
for file in polar_list:
    print(file, cnt)
    cnt+=1
    img = cv2.imread(path + '\\' + file, -1)
    height_ = img.shape[0]
    length_ = img.shape[1]
    image_0 = np.zeros((int(height_ / 4), int(length_ / 4), 3), dtype=np.uint8)
    image_45 = np.zeros((int(height_ / 4), int(length_ / 4), 3), dtype=np.uint8)
    image_135 = np.zeros((int(height_ / 4), int(length_ / 4), 3), dtype=np.uint8)
    image_90 = np.zeros((int(height_ / 4), int(length_ / 4), 3), dtype=np.uint8)
    for i in range(int(height_ / 4)):
        for j in range(int(length_ / 4)):
            image_0[i][j][2] = img[i*4][j*4]
            image_0[i][j][1] = (img[i*4+2][j*4]/2 + img[i*4][j*4+2]/2)
            image_0[i][j][0] = img[i*4+2][j*4+2]

            image_45[i][j][2] = img[i*4+1][j*4]
            image_45[i][j][1] = (img[i*4+2+1][j*4]/2 + img[i*4+1][j*4+2]/2)
            image_45[i][j][0] = img[i*4+2+1][j*4+2]

            image_135[i][j][2] = img[i*4][j*4+1]
            image_135[i][j][1] = (img[i*4+2][j*4+1]/2 + img[i*4][j*4+2+1]/2)
            image_135[i][j][0] = img[i*4+2][j*4+2+1]

            image_90[i][j][2] = img[i*4+1][j*4+1]
            image_90[i][j][1] = (img[i*4+2+1][j*4+1]/2 + img[i*4+1][j*4+2+1]/2)
            image_90[i][j][0] = img[i*4+2+1][j*4+2+1]

    # cv2.imshow("image_0", image_0)
    # cv2.imshow("image_45", image_45)
    # cv2.imshow("image_135", image_135)
    # cv2.imshow("image_90", image_90)
    image0_45 = np.hstack((image_0,image_45))
    image135_90 = np.hstack((image_135, image_90))
    image_all = np.vstack((image0_45, image135_90))
    # cv2.imshow("image_all", image_all)
    # cv2.waitKey()
    cv2.imwrite('Z:\\PolarRealRoadDataBMP\\selected data\\split_polar\\' + file.split('.')[0] + '_split.bmp', image_all)