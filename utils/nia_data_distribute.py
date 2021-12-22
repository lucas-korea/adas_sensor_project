import os
import shutil

path = "D:\\GT 생성 업무\\객체생성-검수\\공주대  gt 데이터 정제\\대구_전방_결과_CAM123\\3"
# 작업자명단 = ['성미애','성선영','신성례','노수진','오연주','윤가영', '노화중','박윤미','정성미','권미애','김민서','이민희']
# 작업자명단 = ['강인선','고지연', '김다예', '배은이', '윤기주', '이상미', '정금연', '정다운', '정유림', '정혜림']
작업자명단 = ['이민희' ]
날짜 = '1221'
image_number =400
for i in 작업자명단:
    try:
        os.mkdir(path + "\\" + i + 날짜)
    except:
        pass
list = [_ for _ in os.listdir(path) if _.endswith('.png') or _.endswith('.jpg')]
for i in range(len(작업자명단)):
    for v in range(image_number):
        print(작업자명단[i], 날짜, end='__')
        print(v + i * image_number, '/', len(작업자명단) * image_number)
        shutil.move(path + '\\' + str(list[v + i * image_number]), path + '\\' + 작업자명단[i] + 날짜)
