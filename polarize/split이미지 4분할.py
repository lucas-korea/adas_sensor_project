import os
import cv2

path = "E:\\max distance experiment\\20231109_polar_Experiment\\rain\\person\\polarize"
file_list = os.listdir(path)
cnt = 0
for file in file_list:
    print(file, cnt)
    cnt += 1
    img = cv2.imread(path + '\\' + file, -1)
    height_ = img.shape[0]
    length_ = img.shape[1]

    new_image0 = img[0 : int(height_/2) ,0:int(length_/2)]
    new_image45 = img[0 : int(height_/2),int(length_/2):length_]
    new_image90 = img[int(height_/2) : height_ , int(length_/2):length_]
    new_image135 = img[int(height_/2) : height_ ,0:int(length_/2)]

    os.makedirs(path + "\\0", exist_ok=True)
    os.makedirs(path + "\\45", exist_ok=True)
    os.makedirs(path + "\\90", exist_ok=True)
    os.makedirs(path + "\\135", exist_ok=True)

    cv2.imwrite(path + '\\0\\' + file.split('.')[0] + '_0.png', new_image0)
    cv2.imwrite(path + '\\45\\' + file.split('.')[0] + '_45.png', new_image45)
    cv2.imwrite(path + '\\90\\' + file.split('.')[0] + '_90.png', new_image90)
    cv2.imwrite(path + '\\135\\' + file.split('.')[0] + '_135.png', new_image135)
