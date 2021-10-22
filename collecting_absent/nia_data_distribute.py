import os
import random
import shutil

path = "D:\\공주대  gt 데이터 정제\\45_NIA3)Hep)_87_211007_pyeongtaek_2(44)\\Src_PNG"
# 작업자명단 = ['성미애','성선영','신성례','노수진','오연주','윤가영', '노화중','박윤미','정성미','권미애','김민서','이민희']
작업자명단 = ['강인선','고지연', '김다예', '배은이', '윤기주', '이상미', '정금연', '정다운', '정유림', '정혜림']
for i in 작업자명단:
    try:
        os.mkdir(path + "\\" + i)
    except:
        pass
list = [_ for _ in os.listdir(path) if _.endswith('.png')]

# random.shuffle(list)
# for i in range(len(list)):
#     print(i/len(list))
#     shutil.copy2(path + '\\' + str(list[i]), path + '\\' + 작업자명단[i % len(작업자명단)])

image_number = 185
for i in range(len(작업자명단)):
    for v in range(image_number):
        print(v + i * image_number, '/', len(작업자명단) * image_number)
        shutil.move(path + '\\' + str(list[v + i * image_number]), path + '\\' + 작업자명단[i])
