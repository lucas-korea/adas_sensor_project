# 본 코드는 raw image를 aolp. dolp로 변환하여 저장하는 코드이다
import os
import PolarizeCam
from PolarizeCam import cv2
import matplotlib.pyplot as plt
if __name__ == '__main__':
    PATH = "E:\\polar_data\\20230922\\polar\\All_angle"
    file_list = [file for file in os.listdir(PATH) if file.endswith('bmp')]
    for file_name in file_list :
        print(file_name)
        img_path = PATH +"\\" + file_name
        img = PolarizeCam.cv2.imread(img_path, -1)
        DOLPplusAOLP_img, DOLP_img, AOLP_img, AOLP_hsv_img = PolarizeCam.DOLPplusAOLP(img)
        PolarizeCam.cv2.imwrite('E:\\polar_data\\20230922\\polar\\Dolp\\' + file_name.split('.')[0] + '_DOLP.bmp',DOLP_img*255.0)
        # PolarizeCam.cv2.imwrite(PATH + '\\polar factor\\' + file_name.split('.')[0] + '_AOLP.bmp',AOLP_hsv_img)
        # PolarizeCam.cv2.imwrite(PATH + '\\polar factor\\' + file_name.split('.')[0] + '_DOLPplusAOLP.bmp', DOLPplusAOLP_img)
