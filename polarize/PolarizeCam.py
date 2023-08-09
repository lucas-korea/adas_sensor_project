import os
import matplotlib.pyplot as plt
import cv2
import numpy as np
import time
import sys

np.set_printoptions(threshold=sys.maxsize)

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


def bayerRGpolarize8_RGB_distribute(polar_image):
    height_ = polar_image.shape[0]
    length_ = polar_image.shape[1]
    print(height_, length_)
    original = np.zeros((int(height_/4), int(length_/4) , 3), dtype=np.uint8)
    RedImg_ = np.zeros((int(height_/4), int(length_/4)), dtype=np.uint8)
    GreenImg_ = np.zeros((int(height_/4), int(length_/4)), dtype=np.uint8)
    BlueImg_ = np.zeros((int(height_/4), int(length_/4)), dtype=np.uint8)
    for i in range(int(height_/4)):
        for j in range(int(length_/4)):
            RedImg_[i,j] = int(polar_image[i * 4, j * 4]/4 + polar_image[i * 4 + 1, j * 4]/4 + polar_image[i * 4, j * 4 + 1]/4 + polar_image[i * 4 + 1, j * 4 + 1]/4)
            GreenImg_[i, j] = int(polar_image[i * 4 + 2, j * 4]/8 + polar_image[i * 4 + 2 + 1, j * 4]/8 + polar_image[i * 4 + 2, j * 4 + 1]/8 + polar_image[i * 4 + 2 + 1, j * 4 + 1]/8
                                  +polar_image[i * 4, j * 4 + 2]/8 + polar_image[i * 4 + 1, j * 4 + 2]/8 + polar_image[i * 4, j * 4 + 2 + 1]/8 + polar_image[i * 4 + 1, j * 4 + 2 + 1]/8)
            BlueImg_[i,j] = int(polar_image[i * 4 + 2, j * 4 + 2]/4 + polar_image[i * 4 + 2 + 1, j * 4 + 2]/4 + polar_image[i * 4 + 2, j * 4 + 2 + 1]/4 + polar_image[i * 4 + 2 + 1, j * 4 + 2 + 1]/4)
    original[:, :, 0] = RedImg_
    original[:, :, 1] = GreenImg_
    original[:, :, 2] = BlueImg_

    plt.subplot(141);plt.title("original");plt.axis('off');plt.imshow(original);plt.xticks([]); plt.yticks([])
    plt.subplot(142);plt.title("RedImg");plt.axis('off');plt.imshow(RedImg_, cmap='gray');plt.xticks([]); plt.yticks([])
    plt.subplot(143);plt.title("GreenImg");plt.axis('off');plt.imshow(GreenImg_, cmap='gray');plt.xticks([]); plt.yticks([])
    plt.subplot(144);plt.title("BlueImg");plt.axis('off');plt.imshow(BlueImg_, cmap='gray');plt.xticks([]); plt.yticks([])
    plt.subplots_adjust(left = 0, bottom = 0, right = 1, top = 0.85, hspace = 0.1, wspace =0.1)
    return original, RedImg_, GreenImg_, BlueImg_

def distribute_RGBplus(polar_image):
    height_ = polar_image.shape[0]
    length_ = polar_image.shape[1]
    print(height_, length_)
    RedImg_ = np.zeros((height_, length_), dtype=np.uint8)
    GreenImg_ = np.zeros((height_, length_), dtype=np.uint8)
    BlueImg_ = np.zeros((height_, length_), dtype=np.uint8)
    PlusImg_ = np.zeros((height_, length_), dtype=np.uint8)
    for i in range(height_):
        for j in range(length_):
            RedImg_[i,j] = polar_image[i, j, 0]
            GreenImg_[i, j] = polar_image[i, j, 1]
            BlueImg_[i,j] = polar_image[i, j, 2]
            if polar_image.shape[2] == 4:
                PlusImg_[i,j] = polar_image[i,j,3]
    return RedImg_, GreenImg_, BlueImg_, PlusImg_


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

def color_analysis(polarize_img, img_path_):
    OriginImg, RedImg, GreenImg, BlueImg= bayerRGpolarize8_RGB_distribute(polarize_img)
    plt.suptitle(img_path_.split('\\')[-1],fontsize=20)
    plt.subplot(141);plt.title("original");plt.axis('off');plt.imshow(OriginImg);plt.xticks([]); plt.yticks([])
    plt.subplot(142);plt.title("RedImg");plt.axis('off');plt.imshow(RedImg, cmap='gray');plt.xticks([]); plt.yticks([])
    plt.subplot(143);plt.title("GreenImg");plt.axis('off');plt.imshow(GreenImg, cmap='gray');plt.xticks([]); plt.yticks([])
    plt.subplot(144);plt.title("BlueImg");plt.axis('off');plt.imshow(BlueImg, cmap='gray');plt.xticks([]); plt.yticks([])
    plt.subplots_adjust(left = 0, bottom = 0, right = 1, top = 0.85, hspace = 0.1, wspace =0.1)


def color_polar_analysis(polarize_img_color, img_path_):
    image90, image45, image135, image0 = distribute_polarize_img(polarize_img_color)

    plt.suptitle(img_path_.split('\\')[-1],fontsize=20)
    plt.subplot(231);plt.title("original");plt.axis('off');plt.imshow(polarize_img_color[:,:,::-1]);plt.xticks([]); plt.yticks([])
    plt.subplot(232);plt.title("image90");plt.axis('off');plt.imshow(image90[:,:,::-1]);plt.xticks([]); plt.yticks([])
    plt.subplot(233);plt.title("image45");plt.axis('off');plt.imshow(image45[:,:,::-1]);plt.xticks([]); plt.yticks([])
    plt.subplot(235);plt.title("image135");plt.axis('off');plt.imshow(image135[:,:,::-1]);plt.xticks([]); plt.yticks([])
    plt.subplot(236);plt.title("image0");plt.axis('off');plt.imshow(image0[:,:,::-1]);plt.xticks([]); plt.yticks([])
    plt.subplots_adjust(left = 0, bottom = 0, right = 1, top = 0.85, hspace = 0.1, wspace =0.1)


def AllAngle(polar_image):
    height_ = polar_image.shape[0]
    length_ = polar_image.shape[1]
    AllAngle_img_ = np.zeros((int(height_ / 2), int(length_ / 2)), dtype=np.float64)
    for i in range(int(height_ / 2)):
        for j in range(int(length_ / 2)):
            AllAngle_img_[i, j] = (int(polar_image[i * 2, j * 2]) + int(polar_image[i * 2 + 1, j * 2 + 1]) + int(polar_image[i * 2 + 1, j * 2]) + int(polar_image[i * 2, j * 2 + 1])) / 4
    return AllAngle_img_

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


def DOLP(polar_image):
    Szero_img_ = S_0_img(polar_image)
    Sone_img_ = S_1_img(polar_image)
    Stwo_img_ = S_2_img(polar_image)
    plt.figure(7);plt.imshow(Szero_img_)
    plt.figure(8);plt.imshow(Sone_img_)
    plt.figure(9);plt.imshow(Stwo_img_)
    print(np.isfinite(Szero_img_).all())
    print(np.isfinite(Sone_img_).all())
    print(np.isfinite(Stwo_img_).all())
    DOLP_img_ = np.sqrt(Sone_img_*Sone_img_ + Stwo_img_*Stwo_img_) / Szero_img_
    DOLP_finite_arr = np.isfinite(DOLP_img_)
    print(np.where(DOLP_finite_arr == False))
    return DOLP_img_


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
    print(AOLP_img_.shape)
    print(DOLP_img_.shape)
    print(result_img_.shape)
    for i in range(int(height_/2)):
        for j in range(int(length_/2)):
            result_img_[i, j, 0] = float(AOLP_hsv_img_[i, j, 0])
            result_img_[i, j, 1] = float(DOLP_img_[i, j] * 255 / max_DOLP_img)
            result_img_[i, j, 2] = float(AOLP_hsv_img_[i, j, 2])
    print(result_img_.shape)
    plt.figure(4);plt.imshow(result_img_)
    plt.figure(6);plt.imshow(result_img_.astype('uint8'))
    plt.figure(5);plt.imshow(DOLP_img_)

    print(result_img_.shape)
    print(result_img_[0][0][0], result_img_[0][0][1], result_img_[0][0][2])
    print(DOLP_img_[0][0])
    print(DOLP_img_[0][0] * 255 / max_DOLP_img)
    print(DOLP_img_[0][0] * 255)
    print(max_DOLP_img)
    return cv2.cvtColor(result_img_.astype("uint8"), cv2.COLOR_HSV2RGB), DOLP_img_, AOLP_img_, HSV_color_mapping(AOLP_img_)

if __name__ == "__main__":

    img_path = "C:\\Users\\jcy37\\source\\repos\\Project2\\data\\trigger data\\20230620_151321_232000061_28.bmp"
    img = cv2.imread(img_path, -1)
    # img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    polar_analysis(img, img_path)
    plt.show()
    # print(img_path)
    # polar_analysis(img, img_path)
    # color_analysis(img, img_path)
    # plt.savefig(img_path.split('\\')[-1].split('.')[0] + '.png', facecolor='#eeeeee', pad_inches=0.5, dpi=300)
    # plt.show()
    # plt.savefig(img_path.split('\\')[-1].split('.')[0] + '.png', facecolor='#eeeeee', pad_inches=0.5, dpi=300)
    # DOLPplusAOLP_img, DOLP_img, AOLP_img, AOLP_hsv_img = DOLPplusAOLP(img)

    # plt.figure(2);plt.imshow(AOLP_img)
    # # color_map = cv2.imread("color_map.PNG")
    # plt.figure(1);plt.suptitle(img_path.split('\\')[-1].split('.')[0])
    # plt.subplot(231);plt.imshow(img, cmap='gray');plt.title("Original"); plt.axis('off');plt.xticks([]);plt.yticks([])
    # # plt.subplot(232);plt.imshow(color_map[:,:,::-1]);plt.title("color_map"); plt.axis('off');plt.xticks([]);plt.yticks([])
    # plt.subplot(234);plt.imshow(DOLP_img, cmap='gray');plt.title("DOLP"); plt.axis('off');plt.xticks([]);plt.yticks([])
    # plt.subplot(235);plt.imshow(AOLP_hsv_img);plt.title("AOLP"); plt.axis('off');plt.xticks([]);plt.yticks([])
    # plt.subplot(236);plt.imshow(DOLPplusAOLP_img);plt.title("DOLP+AOLP"); plt.axis('off');plt.xticks([]);plt.yticks([])
    # plt.subplots_adjust(left=0.03, bottom=0.02, right=0.97, top=0.9, hspace=0.1, wspace=0.1)
    # plt.savefig(img_path + '.png', facecolor='#eeeeee', pad_inches=0.5, dpi=300)
    # plt.show()
    # for file_name in os.listdir("I:\\20220825_cheonan_polarize_target_experiment"):
    #     if 'raw_bayerRGp' in file_name:
    #         # img_path = "I:\\20220825_cheonan_polarize_target_experiment\\bright255_raw_bayerRG8.bmp"
    #         # img_path = "I:\\20220825_cheonan_polarize_target_experiment\\bright255_raw_bayerRGpolarized8.bmp"
    #         # img_path = "I:\\SampleCode\\25.MakePolarImg\\TestDB2\\input2\\road_original.bmp"
    #         img_path = "I:\\20220825_cheonan_polarize_target_experiment\\" + file_name
    #         print(img_path)
    #         img = cv2.imread(img_path, -1) # 원형 그대로 읽기
    #         DOLPplusAOLP_img, DOLP_img, AOLP_img, AOLP_hsv_img = DOLPplusAOLP(img)
    #
    #         plt.figure(2);plt.imshow(AOLP_img)
    #         color_map = cv2.imread("color_map.PNG")
    #         plt.figure(1);plt.suptitle(img_path.split('\\')[-1].split('.')[0])
    #         plt.subplot(231);plt.imshow(img, cmap='gray');plt.title("Original"); plt.axis('off');plt.xticks([]);plt.yticks([])
    #         plt.subplot(232);plt.imshow(color_map[:,:,::-1]);plt.title("color_map"); plt.axis('off');plt.xticks([]);plt.yticks([])
    #         plt.subplot(234);plt.imshow(DOLP_img, cmap='gray');plt.title("DOLP"); plt.axis('off');plt.xticks([]);plt.yticks([])
    #         plt.subplot(235);plt.imshow(AOLP_hsv_img);plt.title("AOLP"); plt.axis('off');plt.xticks([]);plt.yticks([])
    #         plt.subplot(236);plt.imshow(DOLPplusAOLP_img);plt.title("DOLP+AOLP"); plt.axis('off');plt.xticks([]);plt.yticks([])
    #         plt.subplots_adjust(left=0.03, bottom=0.02, right=0.97, top=0.9, hspace=0.1, wspace=0.1)
    #         plt.savefig(img_path.split('\\')[-1].split('.')[0] + '2.png', facecolor='#eeeeee', pad_inches=0.5, dpi=300)



# color_analysis(img)

# img[0,0] = (255,0,0)
# img[0,1] = (0,255,0)
# img[1,1] = (0,0,255)
# img[1,0] = (255,255,255)


# for i in range(0, int(h/2),2):
#     for j in range(0, int(l/2),2):
#         image90[i, j] = img[i * 2,j * 2]
#         image90[i + 1, j] = img[i * 2 + 1, j * 2]
#         image90[i, j + 1] = img[i * 2, j * 2 + 1]
#         image90[i + 1, j + 1] = img[i * 2 + 1, j * 2 + 1]
#
#         image45[i, j] = img[i * 2, j * 2 + 2]
#         image45[i + 1, j] = img[i * 2 + 1, j * 2 + 2]
#         image45[i, j + 1] = img[i * 2, j * 2 + 2 + 1]
#         image45[i + 1, j + 1] = img[i * 2 + 1, j * 2 + 2 + 1]
#
#         image135[i, j] = img[i * 2 + 2, j * 2]
#         image135[i + 1, j] = img[i * 2 + 2 + 1, j * 2]
#         image135[i, j + 1] = img[i * 2 + 2, j * 2 + 1]
#         image135[i + 1, j + 1] = img[i * 2 + 2 + 1, j * 2 + 1]
#
#         image0[i, j] = img[i * 2 + 2, j * 2 + 2]
#         image0[i + 1, j] = img[i * 2 + 2 + 1, j * 2 + 2]
#         image0[i, j + 1] = img[i * 2 + 2, j * 2 + 2 + 1]
#         image0[i + 1, j + 1] = img[i * 2 + 2 + 1, j * 2 + 2 + 1]
# if img is None:
#     print("이미지 로드가 실패 했습니다.")
#     sys.exit()

# print(img[1820,1020])
# img[0,0] = [255, 0 , 0]
# cv2.imshow('image', cv2.resize(img, (0, 0), fx=0.5/2, fy=0.5/2))
# cv2.imshow('image90', cv2.resize(image90, (0, 0), fx=0.5, fy=0.5))
# cv2.imshow('image45', cv2.resize(image45, (0, 0), fx=0.5, fy=0.5))
# cv2.imshow('image135', cv2.resize(image135, (0, 0), fx=0.5, fy=0.5))
# cv2.imshow('image0', cv2.resize(image0, (0, 0), fx=0.5, fy=0.5))
# cv2.waitKey()
# cv2.destroyWindow()



