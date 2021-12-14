import xml.etree.ElementTree as ET
import os

# tree = ET.parse("Z:\\NIA1차_2021온라인콘테스트_선별자료\\2021온라인콘테스트_배포데이터(4만장)_211206\\"
#                 "학습데이터(40,034장)\\20200602_140054\\1_annotations_v001_1\\1_20200602_140054_000000_v001_1.xml")
# root = tree.getroot()
# print(root)
# print(root.tag)
# for child in root:
#     print(child.tag, child.attrib)
# for obj in root.findall('object'):
#     print(obj.find('name').text)
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

PATH = "Z:\\NIA1차_2021온라인콘테스트_선별자료\\2021온라인콘테스트_배포데이터(4만장)_211206\\학습데이터(40,034장)"
i = 0
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


