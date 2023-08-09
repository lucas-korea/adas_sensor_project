# 본 코드는 raw image를 aolp. dolp로 변환하여 저장하는 코드이다
import os
import PolarizeCam
from PolarizeCam import cv2
import matplotlib.pyplot as plt

PATH = "Y:\\PolarRealRoadDataBMP\\selected data\\raw_polar"
file_list = [file for file in os.listdir(PATH) if file.endswith('bmp')]
for file_name in file_list :
    print(file_name)
    img_path = PATH +"\\" + file_name
    img = PolarizeCam.cv2.imread(img_path, -1)
    Glare_reduction_img = PolarizeCam.Glare_reduction(img)
    DOLP_AOLP, DOLP, _, AOLP = PolarizeCam.DOLPplusAOLP(img)
    PolarizeCam.cv2.imwrite('Y:\\PolarRealRoadDataBMP\\selected data\\glare reduction_polar\\' + file_name.split('.')[0] + '_Glare_reduction.bmp',
                            Glare_reduction_img)
    PolarizeCam.cv2.imwrite('Y:\\PolarRealRoadDataBMP\\selected data\\DOLP+AOLP_polar\\' + file_name.split('.')[0] + '_DOLPplusAOLP.bmp',
                            DOLP_AOLP)
    PolarizeCam.cv2.imwrite('Y:\\PolarRealRoadDataBMP\\selected data\\AOLP_polar\\' + file_name.split('.')[0] + '_AOLP.bmp',
                            AOLP)
    PolarizeCam.cv2.imwrite('Y:\\PolarRealRoadDataBMP\\selected data\\DOLP_polar\\' + file_name.split('.')[0] + '_DOLP.bmp',
                            DOLP*255.0)