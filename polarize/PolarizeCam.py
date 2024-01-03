import os
import matplotlib.pyplot as plt
import cv2
import numpy as np
import time
import sys

np.set_printoptions(threshold=sys.maxsize)

# 각 각도별로 이미지 분리
def distribute_polarize_img(polar_image):
    height_ = polar_image.shape[0]
    length_ = polar_image.shape[1]
    image90_ = np.zeros((int(height_/2), int(length_/2)), dtype=np.uint8)
    image45_ = np.zeros((int(height_/2), int(length_/2)), dtype=np.uint8)
    image135_ = np.zeros((int(height_/2), int(length_/2)), dtype=np.uint8)
    image0_ = np.zeros((int(height_/2), int(length_/2)), dtype=np.uint8)
    for i in range(int(height_ / 2)):
        for j in range(int(length_ / 2)):
            image90_[i, j] = polar_image[i * 2, j * 2]
            image45_[i, j] = polar_image[i * 2, j * 2 + 1]
            image135_[i, j] = polar_image[i * 2 + 1, j * 2]
            image0_[i, j] = polar_image[i * 2 + 1, j * 2 + 1]
    return image90_, image45_, image135_, image0_

# 각 각도별로 이미지 분리 및 뷰잉
def polar_analysis(polar_image_gray, img_path_):
    image90, image45, image135, image0 = distribute_polarize_img(polar_image_gray)
    plt.suptitle(img_path_.split('\\')[-1], fontsize=20)
    plt.subplot(231);    plt.title("original");    plt.axis('off');    plt.imshow(polar_image_gray, cmap='gray');    plt.xticks([]);    plt.yticks([])
    plt.subplot(232);    plt.title("image90");    plt.axis('off');    plt.imshow(image90, cmap='gray');    plt.xticks([]);    plt.yticks([])
    plt.subplot(233);    plt.title("image45");    plt.axis('off');    plt.imshow(image45, cmap='gray');    plt.xticks([]);    plt.yticks([])
    plt.subplot(235);    plt.title("image135");    plt.axis('off');    plt.imshow(image135, cmap='gray');    plt.xticks([]);    plt.yticks([])
    plt.subplot(236);    plt.title("image0");    plt.axis('off');    plt.imshow(image0, cmap='gray');    plt.xticks([]);    plt.yticks([])
    plt.subplots_adjust(left=0, bottom=0, right=1, top=0.85, hspace=0.1, wspace=0.1)
    return image90, image45, image135, image0


# 4가지 방향 데이터 중, 가장 값이 작은 데이터를 반사광이 없는 픽셀로 간주
# 만약 편광 성분이 하나도 없다면, 픽셀간 데이터 차이는 없을 것.
def Glare_reduction(polar_image):
    height_ = polar_image.shape[0]
    length_ = polar_image.shape[1]
    Glare_reduction_img_ = np.zeros((int(height_ / 2), int(length_ / 2)), dtype=np.float64)
    for i in range(int(height_ / 2)):
        for j in range(int(length_ / 2)):
            Glare_reduction_img_[i, j] = np.min([polar_image[i * 2, j * 2], polar_image[i * 2 + 1, j * 2],
                                           polar_image[i * 2, j * 2 + 1], polar_image[i * 2 + 1, j * 2 + 1]])
    return Glare_reduction_img_

# S_0 = I = P_0 + P_90
def S_0_img(polar_image):
    height_ = polar_image.shape[0]
    length_ = polar_image.shape[1]
    Szero_img_ = np.zeros((int(height_ / 2), int(length_ / 2)), dtype=np.float64)
    for i in range(int(height_ / 2)):
        for j in range(int(length_ / 2)):
            Szero_img_[i, j] = (float(polar_image[i * 2, j * 2]) + float(polar_image[i * 2 + 1, j * 2 + 1]) +
                               float(polar_image[i * 2 + 1, j * 2]) + float(polar_image[i * 2 , j * 2 + 1]))/2
    return Szero_img_


# S_1 = Q = P_0 - P_90
def S_1_img(polar_image):
    height_ = polar_image.shape[0]
    length_ = polar_image.shape[1]
    Sone_img_ = np.zeros((int(height_ / 2), int(length_ / 2)), dtype=np.float64)
    for i in range(int(height_ / 2)):
        for j in range(int(length_ / 2)):
            Sone_img_[i, j] = float(polar_image[i * 2 + 1, j * 2 + 1]) - float(polar_image[i * 2, j * 2])
    return Sone_img_


# S_2 = P_45 - P_135
def S_2_img(polar_image):
    height_ = polar_image.shape[0]
    length_ = polar_image.shape[1]
    Stwo_img_ = np.zeros((int(height_ / 2), int(length_ / 2)), dtype=np.float64)
    for i in range(int(height_ / 2)):
        for j in range(int(length_ / 2)):
            Stwo_img_[i, j] = float(polar_image[i * 2 + 1, j * 2]) - float(polar_image[i * 2, j * 2 + 1])
    return Stwo_img_

# Degree of linear Polarize, 편광의 정도
def DOLP(polar_image):
    Szero_img_ = S_0_img(polar_image)
    Sone_img_ = S_1_img(polar_image)
    Stwo_img_ = S_2_img(polar_image)
    DOLP_img_ = np.sqrt(Sone_img_*Sone_img_ + Stwo_img_*Stwo_img_) / Szero_img_
    DOLP_finite_arr = np.isfinite(DOLP_img_)
    return DOLP_img_

# Angle of linear Polarize, 편광의 각도
def AOLP(polar_image):
    Sone_img_ = S_1_img(polar_image)
    Stwo_img_ = S_2_img(polar_image)
    AOLP_img_ = np.arctan(Stwo_img_ / Sone_img_)
    return AOLP_img_

def HSV_color_mapping(AOLP_img_):
    height_ = AOLP_img_.shape[0]
    length_ = AOLP_img_.shape[1]
    HSV_img_ = np.zeros((height_, length_, 3), dtype=np.uint8)
    EDGE = np.pi/2
    UNIT = np.pi/12
    for i in range(height_):
        for j in range(length_):
            if -EDGE + UNIT*0 <= AOLP_img_[i, j] < -EDGE + UNIT*1:
                HSV_img_[i,j] = [255, np.uint8((AOLP_img_[i, j] - (-EDGE + UNIT*0))*255/UNIT), 0]
            elif -EDGE + UNIT*1 <= AOLP_img_[i, j] < -EDGE + UNIT*2:
                HSV_img_[i,j] = [255 - np.uint8((AOLP_img_[i, j] - (-EDGE + UNIT*0))*255/UNIT), 255, 0]
            elif -EDGE + UNIT*2 <= AOLP_img_[i, j] < -EDGE + UNIT*3:
                HSV_img_[i,j] = [0, 255, np.uint8((AOLP_img_[i, j] - (-EDGE + UNIT*0))*255/UNIT)]
            elif -EDGE + UNIT*3 <= AOLP_img_[i, j] < -EDGE + UNIT*4:
                HSV_img_[i,j] = [0, 255-np.uint8((AOLP_img_[i, j] - (-EDGE + UNIT*0))*255/UNIT), 255]
            elif -EDGE + UNIT*4 <= AOLP_img_[i, j] < -EDGE + UNIT*5:
                HSV_img_[i,j] = [np.uint8((AOLP_img_[i, j] - (-EDGE + UNIT*0))*255/UNIT), 0, 255]
            elif -EDGE + UNIT*5 <= AOLP_img_[i, j] < -EDGE + UNIT*6:
                HSV_img_[i,j] = [255, 0, 255-np.uint8((AOLP_img_[i, j] - (-EDGE + UNIT*0))*255/UNIT)]
            elif -EDGE + UNIT*6 <= AOLP_img_[i, j] < -EDGE + UNIT*7:
                HSV_img_[i,j] = [255, np.uint8((AOLP_img_[i, j] - (-EDGE + UNIT*0))*255/UNIT), 0]
            elif -EDGE + UNIT*7 <= AOLP_img_[i, j] < -EDGE + UNIT*8:
                HSV_img_[i,j] = [255 - np.uint8((AOLP_img_[i, j] - (-EDGE + UNIT*0))*255/UNIT), 255, 0]
            elif -EDGE + UNIT*8 <= AOLP_img_[i, j] < -EDGE + UNIT*9:
                HSV_img_[i,j] = [0, 255, np.uint8((AOLP_img_[i, j] - (-EDGE + UNIT*0))*255/UNIT)]
            elif -EDGE + UNIT*9 <= AOLP_img_[i, j] < -EDGE + UNIT*10:
                HSV_img_[i,j] = [0, 255-np.uint8((AOLP_img_[i, j] - (-EDGE + UNIT*0))*255/UNIT), 255]
            elif -EDGE + UNIT*10 <= AOLP_img_[i, j] < -EDGE + UNIT*11:
                HSV_img_[i,j] = [np.uint8((AOLP_img_[i, j] - (-EDGE + UNIT*0))*255/UNIT), 0, 255]
            elif -EDGE + UNIT*11 <= AOLP_img_[i, j] < -EDGE + UNIT*12:
                HSV_img_[i,j] = [255, 0, 255-np.uint8((AOLP_img_[i, j] - (-EDGE + UNIT*0))*255/UNIT)]

    return HSV_img_


def DOLPplusAOLP(polar_img):
    height_ = polar_img.shape[0]
    length_ = polar_img.shape[1]
    result_img_ = np.zeros((int(height_/2), int(length_/2), 3), dtype=np.float64)
    DOLP_img_ = DOLP(polar_img)
    AOLP_img_ = AOLP(polar_img)
    AOLP_hsv_img_ = cv2.cvtColor(HSV_color_mapping(AOLP_img_), cv2.COLOR_RGB2HSV)
    max_DOLP_img = np.nanmax(DOLP_img_)

    for i in range(int(height_/2)):
        for j in range(int(length_/2)):
            result_img_[i, j, 0] = float(AOLP_hsv_img_[i, j, 0])
            result_img_[i, j, 1] = float(DOLP_img_[i, j] * 255 / max_DOLP_img)
            result_img_[i, j, 2] = float(AOLP_hsv_img_[i, j, 2])
    plt.figure();plt.imshow(DOLP_img_, cmap='gray')
    plt.figure();plt.imshow(HSV_color_mapping(AOLP_img_))
    plt.figure();plt.imshow(cv2.cvtColor(result_img_.astype("uint8"), cv2.COLOR_HSV2RGB))
    return cv2.cvtColor(result_img_.astype("uint8"), cv2.COLOR_HSV2RGB), DOLP_img_, AOLP_img_, HSV_color_mapping(AOLP_img_)

if __name__ == "__main__":
    img_path = "C:\\Users\\jcy37\\Desktop\\bright63_raw_bayerRGpolarized8.bmp"
    img = cv2.imread(img_path, -1)
    polar_analysis(img, img_path)
    DOLPplusAOLP(img)
    plt.show()


