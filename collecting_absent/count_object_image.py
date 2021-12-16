import os
import shutil

import pandas as pd
import math
from PIL import Image
pd.set_option('display.max_rows', 1000)
path = "D:\\GT 생성 업무\\[참고]Heptacam_가이드문서 및 작업자관리시트\\미첨부(내부문서)_온라인 작업자별_할당및통계.xlsx"

def main():
    data = pd.read_excel(path, sheet_name=1)
    worker_list = ['권미애','김민서','노수진','노은영','노화중','박윤미','성미애','성선영','신성례','윤가영','오연주',
                   '이민희','정성미','강인선','고지연','김다예','배은이','윤기주','이상미','정금연','정다운','정유림','정혜림']
    df = pd.DataFrame(data = worker_list, columns=['name'])
    # print(data)
    df['image_num'] = 0
    df['pay'] = 0

    # print(data.sort_values(by='폴더명')['폴더명'][(data['작업상태'] != "객체생성 진행중")])

    for name in worker_list:
        df.loc[df['name'] == name, 'image_num'] = sum(data['프레임 개수'][(data['작업상태'] != "객체생성 진행중") & (data['작업자'] == name)])
        df.loc[df['name'] == name, 'pay'] += sum(data['프레임 개수'][(data['작업상태'] != "객체생성 진행중") & (data['작업자'] == name) & (data['구분'] == '복합')]) * 150
        df.loc[df['name'] == name, 'pay'] += sum(data['프레임 개수'][(data['작업상태'] != "객체생성 진행중") & (data['작업자'] == name) & (data['구분'] == '도심로')]) * 150
        df.loc[df['name'] == name, 'pay'] += sum(data['프레임 개수'][(data['작업상태'] != "객체생성 진행중") & (data['작업자'] == name) & (data['구분'] == '자전로')]) * 10
    print(df)

def main2():
    PATH = "D:\\GT 생성 업무\\객체생성-검수\\생성완\\새 Microsoft Excel 워크시트 (2).xlsx"
    data = pd.read_excel(PATH)
    PATH2 = "D:\\GT 생성 업무\\[참고]Heptacam_가이드문서 및 작업자관리시트\\미첨부(내부문서)_온라인 작업자별_할당및통계.xlsx"
    data2 = pd.read_excel(PATH2, sheet_name=1)
    worker_list = ['권미애', '김민서', '노수진', '노은영', '노화중', '박윤미', '성미애', '성선영', '신성례', '윤가영', '오연주',
                   '이민희', '정성미', '강인선', '고지연', '김다예', '배은이', '윤기주', '이상미', '정금연', '정다운', '정유림', '정혜림']
    df = pd.DataFrame(data = worker_list, columns=['name'])
    df['image_num'] = 0
    df['obj_num'] = 0
    df['pay'] = 0
    df['line'] = 0
    df['bbox'] = 0
    df['paper num'] = 0
    for name in worker_list:
        df.loc[df['name'] == name, 'image_num'] = sum(data['이미지개수'][(data['이름'] == name)])
        for i in range(len((data[data['이름'] == name]) == True)):
            gubun = data2[data2['폴더명'] == data['폴더명'][(data['이름'] == name)].values[i]]['구분']
            folder_name = data2[data2['폴더명'] == data['폴더명'][(data['이름'] == name)].values[i]]['폴더명'].values[0]
            if gubun.values[0] == '복합':
                df.loc[df['name'] == name, 'pay'] += data['총 객체개수'][(data['폴더명'] == folder_name)].values[0] * 150
                df.loc[df['name'] == name, 'bbox'] += data['bbox'][(data['폴더명'] == folder_name)].values[0]
                df.loc[df['name'] == name, 'line'] += data['line'][(data['폴더명'] == folder_name)].values[0]
            elif gubun.values[0] == '도심로':
                df.loc[df['name'] == name, 'pay'] += data['총 객체개수'][(data['폴더명'] == folder_name)].values[0] * 150
                df.loc[df['name'] == name, 'bbox'] += data['bbox'][(data['폴더명'] == folder_name)].values[0]
                df.loc[df['name'] == name, 'line'] += data['line'][(data['폴더명'] == folder_name)].values[0]
            elif gubun.values[0] == '자전로':
                df.loc[df['name'] == name, 'pay'] += data['총 객체개수'][(data['폴더명'] == folder_name)].values[0] * 100
                df.loc[df['name'] == name, 'bbox'] += data['bbox'][(data['폴더명'] == folder_name)].values[0]
                df.loc[df['name'] == name, 'line'] += data['line'][(data['폴더명'] == folder_name)].values[0]
            df['paper num'][df['name'] == name] = math.ceil(df['pay'][df['name'] == name] / 300000)
    print(df)
    df.to_excel("작업자 pay계산 (2).xlsx")

def CountInspection():
    PATH2 = "D:\\GT 생성 업무\\[참고]Heptacam_가이드문서 및 작업자관리시트\\미첨부(내부문서)_온라인 작업자별_할당및통계.xlsx"
    data2 = pd.read_excel(PATH2, sheet_name=1)
    worker_list = ['성선영', '성미애', '신성례', '김민서']
    df = pd.DataFrame(data=worker_list, columns=['name'])
    df['image_num'] = 0
    df['pre_image_num'] = 0
    for name in worker_list:
        condition = (data2['작업상태'] == '검수 완료') & (data2['검수자'] == name)
        df['image_num'][df['name'] == name] = sum(data2[condition]['프레임 개수'])
        condition = (data2['작업상태'] == '검수 중') & (data2['검수자'] == name)
        df['pre_image_num'][df['name'] == name] = sum(data2[condition]['프레임 개수'])
    print(df)
    print(sum(df['image_num']) , sum(df['pre_image_num']))

def build_contest_filetree():
    file_source = "Z:\\Heptacam_2021온라인콘테스트_평가데이터\\컨테스트용2_야간"
    dst = "Z:\\Heptacam_2021온라인콘테스트_평가데이터\\컨테스트_학습용_야간_img_파일구조 완성"
    dst = dst + '\\'
    cnt = 0
    # print(os.listdir(dst))
    # for name in os.listdir(dst):
    #     if len(os.listdir(dst + name)) == 0:
    #         print( name)
    # exit(1)
    for (path, dir, files) in os.walk(file_source):
        print(path)
        print(len(os.listdir(path)))
        for file in files:
            print(cnt)
            cnt = cnt + 1
            if file.split('.')[1] == 'jpg' or file.split('.')[1] == 'png':
                if file[1] == '_':
                    try:
                        shutil.copy(path + '\\' + file, dst + file.split('_')[1] + '_' + file.split('_')[2] + '\\' + file[0] + '\\' + file)
                    except FileNotFoundError:
                        os.makedirs(dst + file.split('_')[1] + '_' + file.split('_')[2] + '\\' + file[0])
                        shutil.copy(path + '\\' + file , dst + file.split('_')[1] + '_' + file.split('_')[2] + '\\' + file[0] + '\\' + file)
                else:
                    print('wrong file')
                    print(file)
            # if file.split('.')[1] == 'png':
            #     im = Image.open(path + '\\' + file).convert('RGB')
            #     im.save(path + '\\' + file.split('.')[0] + '.jpg', 'jpeg')
            elif file[-10:] == "v001_1.xml_nonono":
                if file[1] == '_':
                    try:
                        shutil.copy(path + '\\' + file , dst + file.split('_')[1] + '_' + file.split('_')[2] + '\\' + file[0] + '_annotations_v001_1' + '\\' + file)
                    except FileNotFoundError:
                        os.makedirs(dst + file.split('_')[1] + '_' + file.split('_')[2] + '\\' + file[0] + '_annotations_v001_1')
                        shutil.copy(path + '\\' + file , dst + file.split('_')[1] + '_' + file.split('_')[2] + '\\' + file[0] + '_annotations_v001_1' + '\\' + file)
                else:
                    print('wrong file')
                    print(file)

if __name__ == "__main__":
    build_contest_filetree()