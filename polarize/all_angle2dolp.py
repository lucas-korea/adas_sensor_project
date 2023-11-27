import os
import matplotlib.pyplot as plt
import cv2
import numpy as np
import time
import sys


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


def DOLP(polar_image):
    Szero_img_ = S_0_img(polar_image)
    Sone_img_ = S_1_img(polar_image)
    Stwo_img_ = S_2_img(polar_image)
    plt.figure(7);plt.imshow(Szero_img_)
    plt.figure(8);plt.imshow(Sone_img_)
    plt.figure(9);plt.imshow(Stwo_img_)
    DOLP_img_ = np.sqrt(Sone_img_*Sone_img_ + Stwo_img_*Stwo_img_) / Szero_img_
    DOLP_finite_arr = np.isfinite(DOLP_img_)
    return DOLP_img_


if __name__ == '__main__':
    PATH = "E:\\polar_data\\20230922\\polar\\All_angle"
    file_list = [file for file in os.listdir(PATH) if file.endswith('bmp')]
    for file_name in file_list :
        print(file_name)
        img_path = PATH +"\\" + file_name
        img = cv2.imread(img_path, -1)
        raw_image = np.zeros(2048, 2248)
        for i in range(2048/4):
            for j in range(2248/4):
                raw_image[i, j] = img[i, j, 0]
                raw_image[i+1, j] = img[i + 2048/8, j, 0]
                raw_image[i, j + 1] = img[i, j + 2248/8, 0]
                raw_image[i + 1, j + 1] = img[i + 2048/8, j + 2248/8, 0]

                raw_image[i + 2, j] = img[i, j, 1]
                raw_image[i + 2 + 1, j] = img[i + 2048 / 8, j, 1]
                raw_image[i + 2, j + 1] = img[i, j + 2248 / 8, 1]
                raw_image[i + 2 + 1, j + 1] = img[i + 2048 / 8, j + 2248 / 8, 1]
        DOLP_img  = DOLP(img)
        cv2.imwrite('E:\\polar_data\\20230922\\polar\\Dolp\\' + file_name.split('.')[0] + '_DOLP.bmp',DOLP_img*255.0)