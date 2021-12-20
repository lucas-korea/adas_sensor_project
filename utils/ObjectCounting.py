import xml.etree.ElementTree as ET
import os
import cv2
import numpy as np

Vehicle_Car = 0
Vehicle_Bus = 0
Vehicle_Motorcycle= 0
Vehicle_Unknown = 0
Pedestrian_Pedestrian = 0
Pedestrian_Bicycle = 0
TrafficLight_Red = 0
TrafficLight_Yellow = 0
TrafficLight_Green = 0
TrafficLight_Arrow = 0
TrafficLight_RedArrow = 0
TrafficLight_YellowArrow = 0
TrafficLight_GreenArrow = 0
TrafficSign_Speed = 0
TrafficSign_Else = 0
RoadMark_StopLine = 0
RoadMark_Crosswalk = 0
RoadMark_Number = 0
RoadMark_Character = 0
RoadMarkArrow_Straight = 0
RoadMarkArrow_Left = 0
RoadMarkArrow_Right = 0
RoadMarkArrow_StraightLeft = 0
RoadMarkArrow_StraightRight = 0
RoadMarkArrow_Uturn = 0
RoadMarkArrow_Else = 0

# ================================================================
Lane_White_Dash = 0
Lane_Yellow_Dash = 0
PATH = "Z:\\NIA1차_2021온라인콘테스트_선별자료\\2021온라인콘테스트_배포데이터(4만장)_211206\\학습데이터(40,034장)"
i = 0

def CountingObject():
    for (path, dir, files) in os.walk(PATH):
        if(path[-5:] == "001_1"):
            print(i , 'th image')
            print(path)
            for file in os.listdir(path):
                i = i + 1
                tree = ET.parse(path + '\\' + file)
                root = tree.getroot()
                for obj in root.findall('object'):
                    # print(obj.find('name').text)
                    try:
                        globals()[obj.find('name').text] = globals()[obj.find('name').text] + 1
                    except:
                        print(obj.find('name').text)
                    # print(globals()[obj.find('name').text])

    print(Vehicle_Car, Vehicle_Bus, Vehicle_Motorcycle, Vehicle_Unknown, Pedestrian_Pedestrian, Pedestrian_Bicycle,
                  TrafficLight_Red, TrafficLight_Yellow, TrafficLight_Green, TrafficLight_Arrow, TrafficLight_RedArrow,
                  TrafficLight_YellowArrow, TrafficLight_GreenArrow, TrafficSign_Speed, TrafficSign_Else, RoadMark_StopLine,
                  RoadMark_Crosswalk, RoadMark_Number, RoadMark_Character, RoadMarkArrow_Straight, RoadMarkArrow_Left,
                  RoadMarkArrow_Right, RoadMarkArrow_StraightLeft, RoadMarkArrow_StraightRight, RoadMarkArrow_Uturn,
                  RoadMarkArrow_Else)

def main():
    PATH = "C:\\Users\\jcy37\\Desktop\\과제\\전측방\\수당수령증_자동화\\수당수령이미지_파일명검수버전"
    i = 0
    for (path, dirs, files) in os.walk(PATH):
        if (path[-5:] == "001_1"):
            for file in os.listdir(path):
                full_path = '\\'.join(path.split('\\')[0:-1]) + '\\' + path.split('\\')[-1][0] + '\\' + file[:-11] + '.jpg'
                img_array = np.fromfile(full_path, np.uint8)
                img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
                if img is None:
                    print('Image load failed')
                    exit()
                i = i + 1
                tree = ET.parse(path + '\\' + file)
                root = tree.getroot()
                for obj in root.findall('object'):
                    for bbox in obj.findall('bndbox'):
                        cv2.rectangle(img, (int(bbox.find('xmin').text), int(bbox.find('ymin').text)), (int(bbox.find('xmax').text), int(bbox.find('ymax').text)), (255, 255,0), 2)
                for line in root.findall('line'):
                    for controlPt in line.findall('controlPt'):
                        spot_list = { 'x' : [], 'y' : []}
                        for xlist in controlPt.findall('x'):
                            spot_list['x'].append(int(xlist.text))
                        for ylist in controlPt.findall('y'):
                            spot_list['y'].append(int(ylist.text))
                        for i in range(len(spot_list['x']) - 1):
                            cv2.line(img, (spot_list['x'][i] , spot_list['y'][i]), (spot_list['x'][i+1] , spot_list['y'][i+1]), (0, 255, 255), 5)
                try:
                    os.mkdir('\\'.join(path.split('\\')[0:-1]) + '\\' + "JungBing")
                except:
                    pass
                print('\\'.join(path.split('\\')[0:-1]) + '\\' + "JungBing" + '\\' + file[:-11] + '.jpg')
                result, encoded_img = cv2.imencode('.jpg', img)
                if result:
                    with open('\\'.join(path.split('\\')[0:-1]) + '\\' + "JungBing" + '\\' + file[:-11] + '.jpg', mode='w+b') as f:
                        encoded_img.tofile(f)
                # cv2.imwrite('\\'.join(path.split('\\')[0:-1]) + '\\' + "JungBing" + '\\' + file[:-11] + '.jpg', img)
                # print(cv2.imwrite('\\'.join(path.split('\\')[0:-1]) + '\\' + "JungBing" + '\\' + file[:-11] + '.jpg' ,img))
                # cv2.imshow("ff", img)
                # cv2.waitKey()

if __name__ == "__main__":
    main()

