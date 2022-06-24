import os
import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
import cv2
import pickle
if __name__ == '__main__':
    data = pd.read_csv("H:\\라이다 지그 장착 시 데이터 양상\\기둥 뗀거.csv")
    print(data.columns)
    print(data.iloc[0])


    RefImage = np.zeros((128,2048), dtype=np.uint8)
    RefImageScatter = [[]]
    SignalImage = np.zeros((128,2048), dtype=np.uint8)
    SignalImageScatter = [[]]
    AmbiantImage = np.zeros((128,2048), dtype=np.uint8)
    AmbiantImageScatter = [[]]
    RangeImage = np.zeros((128,2048), dtype=np.uint8)
    StackImage = [[]]
    StackImage = np.zeros((128,2048), dtype=np.uint8)

    HorizonResol = 360 / (1024)
    start = 1
    HorizonIndexAzimuth = []
    if start:
        for i in range(len(data)):
            if i % 5000 == 0:
                print(i / len(data))
            try:
                HorizonIndex = int((math.atan(data.iloc[i]["Point:0"] / data.iloc[i]["Point:1"]) / math.pi * 360.0 + 180 )/ HorizonResol)
                # HorizonIndexAzimuth.append(round((math.atan(data.iloc[i]["Point:0"] / data.iloc[i]["Point:1"]) / math.pi * 360.0 + 180 )/ HorizonResol, 3))

                if data.iloc[i]["Point:1"] < 0:
                    HorizonIndex += 1024
                HorizonIndex += 1024
                if HorizonIndex >2047:
                    HorizonIndex -= 2048
                RefImage[int(data.iloc[i].Channel)][HorizonIndex] += data.iloc[i].Reflectivity
                SignalImage[int(data.iloc[i].Channel)][HorizonIndex] += data.iloc[i]['Signal Photons']
                AmbiantImage[int(data.iloc[i].Channel)][HorizonIndex] += data.iloc[i]['Ambiant Photons']
                RangeImage[int(data.iloc[i].Channel)][HorizonIndex] += math.sqrt(data.iloc[i]["Point:0"] * data.iloc[i]["Point:0"] + data.iloc[i]["Point:0"] * data.iloc[i]["Point:0"]+
                                                                                data.iloc[i]["Point:0"] * + data.iloc[i]["Point:0"])
                # RangeImage[int(data.iloc[i].Channel)][HorizonIndex] = data.iloc[i]['Range']
            except:
                pass
        with open("RefImagePostoff.pickle", "wb") as fw:
            pickle.dump(RefImage, fw)
        with open("SignalImagePostoff.pickle", "wb") as fw:
            pickle.dump(SignalImage, fw)
        with open("AmbiantImagePostoff.pickle", "wb") as fw:
            pickle.dump(AmbiantImage, fw)
        with open("RangeImagePostoff.pickle", "wb") as fw:
            pickle.dump(RangeImage, fw)
            # print(HorizonIndex)
            # RefImage[int(data.iloc[i].Channel)][]
            # print(data.iloc[i]["Point:0"])
            # print(data.iloc[i]["Point:0"] / data.iloc[i]["Point:1"])
            # print(math.atan(data.iloc[i]["Point:0"] / data.iloc[i]["Point:1"]) / math.pi * 180.0 + 180)
    else:
        with open("RefImagePostoff.pickle", "rb") as fw:
            RefImage = pickle.load(fw)
        with open("SignalImagePostoff.pickle", "rb") as fw:
            SignalImage = pickle.load(fw)
        with open("AmbiantImagePostoff.pickle", "rb") as fw:
            AmbiantImage = pickle.load(fw)
        with open("RangeImagePostoff.pickle", "rb") as fw:
            RangeImage = pickle.load(fw)
    # cv2.normalize(RefImage, RefImage, 0, 255, cv2.NORM_MINMAX)
    # cv2.normalize(SignalImage, SignalImage, 0, 255, cv2.NORM_MINMAX)
    # cv2.normalize(AmbiantImage, AmbiantImage, 0, 255, cv2.NORM_MINMAX)

    MASKRef = RefImage == 0
    RefImage = cv2.applyColorMap(RefImage, cv2.COLORMAP_JET)
    RefImage[MASKRef] = [0, 0, 0]

    SignalImage = cv2.applyColorMap(SignalImage, cv2.COLORMAP_JET)

    AmbiantImage = cv2.applyColorMap(AmbiantImage, cv2.COLORMAP_JET)

    MASKRange = RangeImage > 50
    RangeImage[MASKRange] = [50]
    cv2.normalize(RangeImage, RangeImage, 0, 255, cv2.NORM_MINMAX)
    RangeImage = cv2.applyColorMap(RangeImage, cv2.COLORMAP_JET)
    # RangeImage[MASKRef] = [0, 0, 0]



    cv2.imshow('Refimage', RefImage)
    cv2.imshow('SignalImage', SignalImage)
    cv2.imshow('AmbiantImage', AmbiantImage)
    cv2.imshow('RangeImage', RangeImage)

    cv2.imwrite('RefimagePostoff.png', RefImage)
    cv2.imwrite('SignalImagePostoff.png', SignalImage)
    cv2.imwrite('AmbiantImagePostoff.png', AmbiantImage)
    cv2.imwrite('RangeImagePostoff.png', RangeImage)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # plt.scatter(data["Point:0"])