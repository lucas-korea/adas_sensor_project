import os
import shutil

srcPATH = "I:\\20220824_calib\\PCDmatched"
ImgPATH = "I:\\20220824_calib\\calibration 쌍\\distortion"
Img = os.listdir(ImgPATH)
for i in range(len(Img)):
    Img[i] = '_'.join(Img[i].split('_')[:-1])
    shutil.copy2(srcPATH + '\\' + Img[i]+'_H.pcd', ImgPATH + '\\' + Img[i]+'_H.pcd')
    print(Img[i])
