import os

import numpy as np
import pandas as pd
worker_list = ['권미애', '김민서', '노수진', '노은영', '노화중', '박윤미', '성미애', '성선영', '신성례', '윤가영', '오연주',
                   '이민희', '정성미', '강인선', '고지연', '김다예', '배은이', '윤기주', '이상미', '정금연', '정다운', '정유림', '정혜림']

PATH = "Z:\\NIA1차_2021온라인콘테스트_선별자료\\2021온라인콘테스트_배포데이터(4만장)_211206\\학습데이터(40,034장)"
path_ = PATH + "\\"
folder_name = "학습데이터(40,034장)"

def make_txt_for_objectCounting():
    List = os.listdir(PATH)
    with open("Z:\\NIA1차_2021온라인콘테스트_선별자료\\2021온라인콘테스트_배포데이터(4만장)_211206\\" + "test.txt", 'w') as f:
        for i in List:
            if os.path.isdir(path_ + i):
                f.write('.\\' + folder_name + '\\' + i + ' ' + i[:3] + '\n')

# 생성완 폴더 내 폴더 구조 이름 변경
def rename_images_xml_create_folder():
    PATH = "D:\\GT 생성 업무\\객체생성-검수\\생성완"
    for (path, dir, files) in os.walk(PATH):
        if len(dir) == 2 and dir[1][-4:] == 'v001':
            print(os.listdir(path + "\\" + dir[0])[0][0:2])
            print(dir)
            cam_num = os.listdir(path + "\\" + dir[0])[0][0]
            if os.listdir(path + "\\" + dir[0])[0][1] == '_':
                os.rename(path + '\\' + dir[0], path + '\\' + cam_num)
                os.rename(path + '\\' + dir[1], path + '\\' + cam_num + '_annotations_v001')
            else:
                os.rename(path + '\\' + dir[0], path + '\\4')
                os.rename(path + '\\' + dir[1], path + '\\4_annotations_v001')
        elif len(dir) == 1:
            print(path, dir)

# 검수완 폴더 내 폴더 구조 이름 변경
def rename_images_xml_modify_folder():
    PATH = "D:\\GT 생성 업무\\객체생성-검수\\검수완"
    for (path, dir, files) in os.walk(PATH):
        if path.split('\\')[-1][0:3] in worker_list and len(dir) != 3:
            print('================== ')
            print('wrong file tree!!! ', path, dir)
        elif len(dir) == 3 and dir[1][-4:] == 'v001':
            cam_num = os.listdir(path + "\\" + dir[0])[0][0]
            if os.listdir(path + "\\" + dir[0])[0][1] == '_':
                os.rename(path + '\\' + dir[0], path + '\\' + cam_num)
                os.rename(path + '\\' + dir[1], path + '\\' + cam_num + '_annotations_v001')
                os.rename(path + '\\' + dir[2], path + '\\' + cam_num + '_annotations_v001_1')
            else:
                os.rename(path + '\\' + dir[0], path + '\\4')
                os.rename(path + '\\' + dir[1], path + '\\4_annotations_v001')
                os.rename(path + '\\' + dir[2], path + '\\4_annotations_v001_1')


def getCaseNamebyFolderName():
    SidecamList = np.array(['윤기주0110','성미애0110','성선영0110','박윤미0111','노수진0112','오연주0112','박윤미0113','이민희0113','정다운0114','정다운0117','성미애0117','신성례0118'])
    FrontcamList = np.array(['윤가영1122', '성미애1210', '윤가영1210','정다운1118','정다운1130','권미애1206','이민희0118','박윤미0118'
                                ,'정성미0117','강인선0117','김다예0117','정성미1125','강인선1130','성미애1207','윤가영1207','윤기주0118','이상미0114','배은이0114'])
    print(len(SidecamList), len(FrontcamList))
    PATH = 'D:\\GT 생성 업무\\객체생성-검수'
    SidecamCaseList = []
    FrontcamCaseList = []
    cnt = 0
    for (path, dir, files) in os.walk(PATH):
        if path.split('\\')[-1] in SidecamList:
            if len(files) > 10:
                for file in files:
                    if '_'.join(file.split('_')[0:3]) not in SidecamCaseList:
                        SidecamCaseList.append('_'.join(file.split('_')[0:3]))
            cnt = cnt + 1
            print(path)
            # print(path.split('\\')[-1] , np.where(SidecamList == path.split('\\')[-1]))
            SidecamList = np.delete(SidecamList, np.where(SidecamList == path.split('\\')[-1]))
        elif path.split('\\')[-1] in FrontcamList:
            if len(files) > 10:
                for file in files:
                    if '_'.join(file.split('_')[0:3]) not in FrontcamCaseList:
                        FrontcamCaseList.append('_'.join(file.split('_')[0:3]))
            cnt = cnt + 1
            print(path)
            # print(path.split('\\')[-1] , np.where(FrontcamList == path.split('\\')[-1]))
            FrontcamList = np.delete(FrontcamList, np.where(FrontcamList == path.split('\\')[-1]))
    print('cnt = ', cnt)
    print('SidecamList : ', SidecamList, len(SidecamList))
    print(SidecamCaseList)
    print('FrontcamList : ', FrontcamList, len(FrontcamList))
    print(FrontcamCaseList)


    with open("camCaseList.txt", 'w') as f:
        f.write('sidecamlist '+ '\n')
        for i in SidecamCaseList:
            f.write(i + '\n')
        f.write('frontcamlist' + '\n')
        for i in FrontcamCaseList:
            f.write(i + '\n')

def CheckCaseExist():
    pd.set_option('display.max_rows', 500)
    df = pd.read_excel("D:\\GT 생성 업무\\[참고]Heptacam_가이드문서 및 작업자관리시트\\미첨부(내부문서)_온라인 작업자별_할당및통계.xlsx", sheet_name='작업자통계_정찬영')
    CaseList =  df[df['작업상태'] == '검수 완료']['폴더명'].values
    print(CaseList, len(CaseList))
    for path, dirs, files in os.walk("D:\\GT 생성 업무\\객체생성-검수\\검수완"):
        for dir in dirs:
            if dir in CaseList:
                CaseList = np.delete(CaseList, np.where(CaseList == dir))
    print(CaseList, len(CaseList))

def RenameBusCams():
    PATH = "D:\\GT 생성 업무\\객체생성-검수\\검수완\\1\\정다운0108\\4"
    for file in os.listdir(PATH):
        # if file[0:2] == '2_':
        #     pass
        # else:
        os.rename(PATH + '\\' + file, PATH + '\\' + '2_' + file)

if __name__ == "__main__":
    getCaseNamebyFolderName()