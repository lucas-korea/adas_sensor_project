import os
import pandas as pd
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
    PATH = "D:\\GT 생성 업무\\객체생성-검수\\생성완\\새 Microsoft Excel 워크시트.xlsx"
    data = pd.read_excel(PATH)
    PATH2 = "D:\\GT 생성 업무\\[참고]Heptacam_가이드문서 및 작업자관리시트\\미첨부(내부문서)_온라인 작업자별_할당및통계.xlsx"
    data2 = pd.read_excel(PATH2, sheet_name=1)
    worker_list = ['권미애', '김민서', '노수진', '노은영', '노화중', '박윤미', '성미애', '성선영', '신성례', '윤가영', '오연주',
                   '이민희', '정성미', '강인선', '고지연', '김다예', '배은이', '윤기주', '이상미', '정금연', '정다운', '정유림', '정혜림']
    df = pd.DataFrame(data = worker_list, columns=['name'])
    df['image_num'] = 0
    df['obj_num'] = 0
    df['pay'] = 0
    for name in worker_list:
        df.loc[df['name'] == name, 'image_num'] = sum(data['이미지개수'][(data['이름'] == name)])
        df.loc[df['name'] == name, 'obj_num'] = sum(data['총 객체개수'][data['이름'] == name])
        # print(len(data['총 객체개수'][(data['이름'] == name)]))
        # print(data['폴더명'][(data['이름'] == name)].values)
        for i in range(len((data[data['이름'] == name]) == True)):
            # print(len((data[data['이름'] == name]) == True), name)
            # print(i)
            # print( name, data['폴더명'][(data['이름'] == name)].values[i])
            # print(data2[data2['폴더명'] == data['폴더명'][(data['이름'] == name)].values[i]]['구분'])
            gubun = data2[data2['폴더명'] == data['폴더명'][(data['이름'] == name)].values[i]]['구분']
            # print("gunun,", gubun)

            folder_name = data2[data2['폴더명'] == data['폴더명'][(data['이름'] == name)].values[i]]['폴더명'].values[0]
            # print("gunun,", gubun)
            # print("folder name", folder_name)
            if gubun.values[0] == '복합':
                # print("here", data['총 객체개수'][(data['폴더명'] == folder_name)].values[0] * 150)
                # print("복합")
                df.loc[df['name'] == name, 'pay'] += data['총 객체개수'][(data['폴더명'] == folder_name)].values[0] * 150
            elif gubun.values[0] == '도심로':
                # print("도심로")
                df.loc[df['name'] == name, 'pay'] += data['총 객체개수'][(data['폴더명'] == folder_name)].values[0] * 150
            elif gubun.values[0] == '자전로':
                # print("자전로")
                df.loc[df['name'] == name, 'pay'] += data['총 객체개수'][(data['폴더명'] == folder_name)].values[0] * 100
    print(df)
    print(sum(df['pay']))

if __name__ == "__main__":
    main2()