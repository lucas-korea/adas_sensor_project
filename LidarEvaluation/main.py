import numpy as np
from open3d import *
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
    path = "C:\\Users\\jcy37\\PycharmProjects\\LidarEvaluation\\newJig_underlidar.csv"
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

radius = 3
def mouse_event(event, x, y, flags, param):
    global radius

    if event == cv2.EVENT_FLAG_LBUTTON:
        cv2.circle(param, (x, y), radius, (255, 0, 0), 2)
        cv2.imshow("Refimage", RefImage)

    elif event == cv2.EVENT_MOUSEWHEEL:
        if flags > 0:
            radius += 1
        elif radius > 1:
            radius -= 1


if __name__ == '__main__':


    path = "C:\\Users\\jcy37\\PycharmProjects\\LidarEvaluation\\oldJig_underlidar_outside3.csv"
    data = pd.read_csv(path)

    RefImage = np.zeros((128,2048), dtype=np.uint8)
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
            try:
                HorizonIndex = int((math.atan(data.iloc[i]["Point:0"] / data.iloc[i]["Point:1"]) / math.pi * 360.0 + 180 )/ HorizonResol)

                if data.iloc[i]["Point:1"] < 0:
                    HorizonIndex += 1024
                HorizonIndex += 1024
                if HorizonIndex >2047:
                    HorizonIndex -= 2048
                RefImage[int(data.iloc[i].Channel)][HorizonIndex] += data.iloc[i]['Reflectivity']
                RangeImage[int(data.iloc[i].Channel)][HorizonIndex] += math.sqrt(data.iloc[i]["Point:0"] * data.iloc[i]["Point:0"] + data.iloc[i]["Point:0"] * data.iloc[i]["Point:0"]+
                                                                                data.iloc[i]["Point:0"] * + data.iloc[i]["Point:0"])
            except:
                pass

        with open(file_start_name + "RefImage" + file_end_name + ".pickle", "wb") as fw:
            pickle.dump(RefImage, fw)
        with open(file_start_name + "RangeImage" + file_end_name + ".pickle", "wb") as fw:
            pickle.dump(RangeImage, fw)
    else:
        with open(file_start_name + "RefImage" + file_end_name + ".pickle", "rb") as fw:
            RefImage = pickle.load(fw)
        with open(file_start_name + "RangeImage" + file_end_name + ".pickle", "rb") as fw:
            RangeImage = pickle.load(fw)


    newimage = np.zeros((128, 2048), dtype=np.uint8)
    ANGLERANGE = 69
    newimage[:,ANGLERANGE:2048] = RefImage[:,0:2048-ANGLERANGE]
    newimage[:, 0:ANGLERANGE] = RefImage[:, 2048-ANGLERANGE:2048]
    newimage = cv2.applyColorMap(newimage, cv2.COLORMAP_JET)

    RefImage = cv2.applyColorMap(RefImage, cv2.COLORMAP_JET)

    MASKRange = RangeImage > 50
    RangeImage[MASKRange] = [50]
    cv2.normalize(RangeImage, RangeImage, 0, 255, cv2.NORM_MINMAX)
    RangeImage = cv2.applyColorMap(RangeImage, cv2.COLORMAP_JET)

    cv2.imshow('Refimage', RefImage)
    cv2.setMouseCallback("Refimage", mouse_event, RefImage)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
