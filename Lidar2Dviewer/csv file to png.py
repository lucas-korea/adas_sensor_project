import os
import csv
import sys

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
import cv2
import pickle
import datetime
np.set_printoptions(threshold=sys.maxsize)

def PCDangleCrop():
    path = "C:\\Users\\jcy37\\PycharmProjects\\ouster_viewer_3layer\\upper_lidar.csv"
    data = pd.read_csv(path)
    HorizonResol = 360 / (1024)
    DropIndex = []
    HorizonIndex = 0
    for i in range(len(data)):
        if i % 5000 == 0:
            print(i / len(data))
        try:HorizonIndex = int((math.atan(data.iloc[i]["Point:0"] / data.iloc[i]["Point:1"]) / math.pi * 360.0 + 180) / HorizonResol)
        except:pass
        if data.iloc[i]["Point:1"] < 0:
            HorizonIndex += 1024
        HorizonIndex += 1024
        if HorizonIndex > 2047:
            HorizonIndex -= 2048

        if HorizonIndex < 50 or HorizonIndex > 2048-50:
            DropIndex.append(i)
    data = data.drop(DropIndex)
    print(data.shape)
    # data = data.drop(data.columns[0], axis=1)
    data.to_csv(path.split('.')[0] + '_anglecrop50.csv', index=False)
    # with open(path, 'w'):
    #     pass

if __name__ == '__main__':
    # PCDangleCrop()
    # exit(1)
    path = "C:\\Users\\jcy37\\PycharmProjects\\ouster_viewer_3layer\\upper_lidar.csv"
    data = pd.read_csv(path)

    RefImage = np.zeros((128,2048), dtype=np.uint8)
    SignalImage = np.zeros((128,2048), dtype=np.uint8)
    AmbiantImage = np.zeros((128,2048), dtype=np.uint8)
    RangeImage = np.zeros((128,2048), dtype=np.uint8)

    file_start_name = ''
    file_end_name = path.split('\\')[-1].split('.')[0]

    HorizonResol = 360 / (1024)
    start = 0
    HorizonIndexAzimuth = []
    if start:
        for i in range(len(data)):
            if i % 5000 == 0:
                print(i / len(data))
            HorizonIndex = int((math.atan(data.iloc[i]["Point:0"] / data.iloc[i]["Point:1"]) / math.pi * 360.0 + 180 )/ HorizonResol)
            # HorizonIndexAzimuth.append(round((math.atan(data.iloc[i]["Point:0"] / data.iloc[i]["Point:1"]) / math.pi * 360.0 + 180 )/ HorizonResol, 3))

            if data.iloc[i]["Point:1"] < 0:
                HorizonIndex += 1024
            HorizonIndex += 1024
            if HorizonIndex >2047:
                HorizonIndex -= 2048
            RefImage[int(data.iloc[i].Channel)][HorizonIndex] += data.iloc[i]['Reflectivity']
            # print(data.iloc[i]['Reflectivity'])
            SignalImage[int(data.iloc[i].Channel)][HorizonIndex] += data.iloc[i]['Signal Photons']
            AmbiantImage[int(data.iloc[i].Channel)][HorizonIndex] += data.iloc[i]['Ambiant Photons']
            RangeImage[int(data.iloc[i].Channel)][HorizonIndex] += math.sqrt(data.iloc[i]["Point:0"] * data.iloc[i]["Point:0"] + data.iloc[i]["Point:0"] * data.iloc[i]["Point:0"]+
                                                                            data.iloc[i]["Point:0"] * + data.iloc[i]["Point:0"])
            # RangeImage[int(data.iloc[i].Channel)][HorizonIndex] = data.iloc[i]['Range']

        # print(max(RefImage))
        with open(file_start_name + "RefImage" + file_end_name + ".pickle", "wb") as fw:
            pickle.dump(RefImage, fw)
        with open(file_start_name + "SignalImage" + file_end_name + ".pickle", "wb") as fw:
            pickle.dump(SignalImage, fw)
        with open(file_start_name + "AmbiantImage" + file_end_name + ".pickle", "wb") as fw:
            pickle.dump(AmbiantImage, fw)
        with open(file_start_name + "RangeImage" + file_end_name + ".pickle", "wb") as fw:
            pickle.dump(RangeImage, fw)
    else:
        with open(file_start_name + "RefImage" + file_end_name + ".pickle", "rb") as fw:
            RefImage = pickle.load(fw)
        with open(file_start_name + "SignalImage" + file_end_name + ".pickle", "rb") as fw:
            SignalImage = pickle.load(fw)
        with open(file_start_name + "AmbiantImage" + file_end_name + ".pickle", "rb") as fw:
            AmbiantImage = pickle.load(fw)
        with open(file_start_name + "RangeImage" + file_end_name + ".pickle", "rb") as fw:
            RangeImage = pickle.load(fw)
    # cv2.normalize(RefImage, RefImage, 0, 255, cv2.NORM_MINMAX)
    # cv2.normalize(SignalImage, SignalImage, 0, 255, cv2.NORM_MINMAX)
    # cv2.normalize(AmbiantImage, AmbiantImage, 0, 255, cv2.NORM_MINMAX)

    newimage = np.zeros((128, 2048), dtype=np.uint8)
    ANGLERANGE = 69
    newimage[:,ANGLERANGE:2048] = RefImage[:,0:2048-ANGLERANGE]
    newimage[:, 0:ANGLERANGE] = RefImage[:, 2048-ANGLERANGE:2048]
    newimage = cv2.applyColorMap(newimage, cv2.COLORMAP_JET)
    # print(RefImage)
    # print(RefImage.shape)
    # print(max(RefImage[1]))
    # MASKRef = RefImage == 0
    RefImage = cv2.applyColorMap(RefImage, cv2.COLORMAP_JET)
    # RefImage[MASKRef] = [0, 0, 0]

    SignalImage = cv2.applyColorMap(SignalImage, cv2.COLORMAP_JET)
    AmbiantImage = cv2.applyColorMap(AmbiantImage, cv2.COLORMAP_JET)

    MASKRange = RangeImage > 50
    RangeImage[MASKRange] = [50]
    cv2.normalize(RangeImage, RangeImage, 0, 255, cv2.NORM_MINMAX)
    RangeImage = cv2.applyColorMap(RangeImage, cv2.COLORMAP_JET)
    # RangeImage[MASKRef] = [0, 0, 0]

    cv2.imshow('newimage', newimage)
    cv2.imshow('Refimage', RefImage)
    cv2.imshow('SignalImage', SignalImage)
    # cv2.imshow('AmbiantImage', AmbiantImage)
    cv2.imshow('RangeImage', RangeImage)

    cv2.imwrite(file_start_name + 'newimage' + file_end_name + '.png', newimage)
    cv2.imwrite(file_start_name + 'Refimage' + file_end_name + '.png', RefImage)
    cv2.imwrite(file_start_name + 'SignalImage' + file_end_name + '.png', SignalImage)
    cv2.imwrite(file_start_name + 'AmbiantImage' + file_end_name + '.png', AmbiantImage)
    cv2.imwrite(file_start_name + 'RangeImage' + file_end_name + '.png', RangeImage)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
