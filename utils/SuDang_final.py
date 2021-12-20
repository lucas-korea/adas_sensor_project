import os
import pandas as pd
import csv
import shutil

worker_list = ['권미애', '김민서', '노수진', '노은영', '노화중', '박윤미', '성미애', '성선영', '신성례', '윤가영', '윤점동', '오연주'
                   '이민희', '정성미', '강인선', '고지연', '김다예', '배은이', '윤기주', '이상미', '정금연', '정다운', '정유림', '정혜림']
result = []
paper_num_ = 0
day_list = [1,2,3,4,5,8,9,10,11,12,15,16,17,18,19,22,23,24,25,26,29,41,42,43,46,47,48,49,410,413,414]

def main():
    PATH_Wan = "D:\\GT 생성 업무\\객체생성-검수\\생성완"
    for (path, dirs, files) in os.walk(PATH_Wan): #생성완 폴더 진입
        if path[-4:-1] in worker_list: #현재 폴더가 "작업자"_ 인지 확인
            if path[-4:-1] == '권미애':
                pass
            for file in files:
                if file[-7:] == "sub.csv": #*sub.csv file 찾기
                    OpenCsv_ObjCounting(file,path)
    print(paper_num_)
    f = open('example3.csv', 'w', newline='')
    wr = csv.writer(f)
    wr.writerow(['이름', '시험명', '프레임수', '금액','오브젝트 개수'])
    name = ''
    name2 = ''
    day_i = 0
    for i in range(len(result)):
        name2 = result[i][0]
        if name != name2:
            day_i = 0
        name = name2
        wr.writerow(result[i][:4] + ["Object개수:  차선_{}/  차량 _{}/ 보행자_{}/  신호등_{}/  표지판_{}/  노면표식_{}/ 노면화살표_{}".format((result[i][4]), (result[i][5]),
                                                                                       (result[i][6]),
                                                                                       (result[i][7]),
                                                                                       (result[i][8]),
                                                                                       (result[i][9]),
                                                                                       (result[i][10]))]
                                                                                        + [sum(result[i][4:11])]
                                                                                        + [day_list[day_i]])
        day_i = day_i + 1

def OpenCsv_ObjCounting(file, PATH):
    Lane_num = []
    Vehicle_num = []
    Pedestrian_num = []
    TraficLight_num = []
    TraficSign_num = []
    RoadMark_num = []
    RoadMarkArrow = []

    gubun = LoadGubun(file.split('_')[0])
    fee = DefineFee(gubun)
    Sub_data = pd.read_csv(PATH + '\\' + file, encoding='euc-kr', sep='\t')
    properate_divined_pay = DefProperate_divined_pay(file, PATH)
    img_cnt = 0
    ing_cnt2 = 0
    img_num = 0
    total = 0
    exp_num = 0
    img_name = ImageName(file.split('_')[0], PATH, 0)

    for i in range(len(Sub_data)):
        if Sub_data.iloc[i].values[0].split(',')[0] != 'total' and Sub_data.iloc[i].values[0].split(',')[0][:-1] != 'subtotal' and len(Sub_data.iloc[i].values[0].split(',')[0]) > 2:
            Lane_num.append(int(Sub_data.iloc[i].values[0].split(',')[4]))
            Vehicle_num.append(int(Sub_data.iloc[i].values[0].split(',')[5]))
            Pedestrian_num.append(int(Sub_data.iloc[i].values[0].split(',')[6]))
            TraficLight_num.append(int(Sub_data.iloc[i].values[0].split(',')[7]))
            TraficSign_num.append(int(Sub_data.iloc[i].values[0].split(',')[8]))
            RoadMark_num.append(int(Sub_data.iloc[i].values[0].split(',')[9]))
            RoadMarkArrow.append(int(Sub_data.iloc[i].values[0].split(',')[10]))
            total = (sum(Lane_num) + sum(Vehicle_num) + sum(Pedestrian_num) + sum(TraficLight_num) + sum(
                TraficSign_num) + sum(RoadMark_num) + sum(RoadMarkArrow)) * fee
            if total > properate_divined_pay:
                img_num = ing_cnt2 - img_cnt
                img_cnt = ing_cnt2
                write_mail_merge_excel(file.split('_')[0][:3], img_name, img_num, total, Lane_num, Vehicle_num, Pedestrian_num, TraficLight_num, TraficSign_num, RoadMark_num, RoadMarkArrow)
                img_name = ImageName(file.split('_')[0], PATH, i)
                exp_num = exp_num + 1
                Lane_num = []
                Vehicle_num = []
                Pedestrian_num = []
                TraficLight_num = []
                TraficSign_num = []
                RoadMark_num = []
                RoadMarkArrow = []
            ing_cnt2 = ing_cnt2 + 1
    img_num = ing_cnt2 - img_cnt
    write_mail_merge_excel(file.split('_')[0][:3], img_name, img_num, total, Lane_num, Vehicle_num, Pedestrian_num, TraficLight_num, TraficSign_num,
                           RoadMark_num, RoadMarkArrow)


def write_mail_merge_excel(name, img_name, img_num, total, Lane_num, Vehicle_num, Pedestrian_num, TraficLight_num, TraficSign_num, RoadMark_num, RoadMarkArrow):
    global paper_num_
    global result
    paper_num_ = paper_num_ + 1
    result.append([name, img_name, img_num, total, sum(Lane_num), sum(Vehicle_num), sum(Pedestrian_num), sum(TraficLight_num), sum(TraficSign_num), sum(RoadMark_num), sum(RoadMarkArrow)])
    print(name, img_name, img_num, total, sum(Lane_num), sum(Vehicle_num), sum(Pedestrian_num), sum(TraficLight_num), sum(TraficSign_num), sum(RoadMark_num), sum(RoadMarkArrow))

def DefProperate_divined_pay(file, PATH):
    Lane_num = []
    Vehicle_num = []
    Pedestrian_num = []
    TraficLight_num = []
    TraficSign_num = []
    RoadMark_num = []
    RoadMarkArrow = []

    gubun = LoadGubun(file.split('_')[0])
    fee = DefineFee(gubun)
    Sub_data = pd.read_csv(PATH + '\\' + file, encoding='euc-kr', sep='\t')
    for i in range(len(Sub_data)):
        if Sub_data.iloc[i].values[0].split(',')[0] != 'total' and Sub_data.iloc[i].values[0].split(',')[0][:-1] != 'subtotal' and len(Sub_data.iloc[i].values[0].split(',')[0]) > 2:
            Lane_num.append(int(Sub_data.iloc[i].values[0].split(',')[4]))
            Vehicle_num.append(int(Sub_data.iloc[i].values[0].split(',')[5]))
            Pedestrian_num.append(int(Sub_data.iloc[i].values[0].split(',')[6]))
            TraficLight_num.append(int(Sub_data.iloc[i].values[0].split(',')[7]))
            TraficSign_num.append(int(Sub_data.iloc[i].values[0].split(',')[8]))
            RoadMark_num.append(int(Sub_data.iloc[i].values[0].split(',')[9]))
            RoadMarkArrow.append(int(Sub_data.iloc[i].values[0].split(',')[10]))

    total = (sum(Lane_num) + sum(Vehicle_num) + sum(Pedestrian_num) + sum(TraficLight_num) + sum(TraficSign_num) + sum(
        RoadMark_num) + sum(RoadMarkArrow)) * fee
    paper_num = 1
    while total/paper_num > 295000:
        paper_num = paper_num + 1
    properate_divined_pay = total / paper_num
    return properate_divined_pay


def DefineFee(gubun):
    if gubun == '자전로':
        return 100
    elif gubun == '도심로':
        return 150
    elif gubun == '복합':
        return 150
    print("fee never be 0")
    exit(1)
    return 0

def LoadGubun(case_name = '배은이1206'):
    PATH = "D:\\GT 생성 업무\\[참고]Heptacam_가이드문서 및 작업자관리시트\\미첨부(내부문서)_온라인 작업자별_할당및통계.xlsx"
    data = pd.read_excel(PATH, sheet_name=1)
    return data[data['폴더명'] == case_name]['구분'].values[0]


def ImageName(case_name, PATH, i):
    for (path, dirs, files) in os.walk(PATH+'\\'+case_name):
        if len(path.split('\\')[-1]) == 1:
            return files[i].split('.')[0]

def GetJungBingImgXml():
    PATH_auto = "C:\\Users\\jcy37\\Desktop\\과제\\전측방\\수당수령증_자동화"
    PATH_inspec = "D:\\GT 생성 업무\\객체생성-검수\\생성완"
    dst = "C:\\Users\\jcy37\\Desktop\\과제\\전측방\\수당수령증_자동화\\수당수령이미지_파일명생성버전"
    df_sudang = pd.read_excel(PATH_auto + '\\' + "수당수령증_2021_전측방시트.xlsx")
    cnt = 0
    BREAK = False
    for i in range(len(df_sudang)):
        print(cnt)
        cnt = cnt + 1
        cur_exp_name = df_sudang.iloc[i]['시험명']
        cam_num = cur_exp_name[0]
        if cam_num not in ['1', '2', '3']:
            cam_num = '4'
        NAME = df_sudang.iloc[i]['작업자']
        if NAME == '윤점동':
            NAME = '윤가영'
        suc = 0
        for (path, dirs, files) in os.walk(PATH_inspec):
            if BREAK:
                BREAK = False
                break
            if path.split('\\')[-2][0:3] == NAME and path.split('\\')[-4] == '생성완': #상위상위폴더 이름 첫 3글자가 작업자 이름이랑 매칭되는지 확인 상상상위
                for j in range(len(files)):
                    if files[j].split('.')[0] == cur_exp_name:
                        j2 = int(j + df_sudang.iloc[i]['프레임수'] * 2/4)
                        j3 = int(j + df_sudang.iloc[i]['프레임수'] * 3/4)
                        try:
                            os.mkdir(dst + '\\' + cur_exp_name)
                        except:
                            pass
                        os.mkdir(dst + '\\' + cur_exp_name +'\\' + cam_num)
                        os.mkdir(dst + '\\' + cur_exp_name + '\\' + cam_num + "_annotations_v001")
                        shutil.copy2(path +'\\' + files[j], dst + '\\' + cur_exp_name +'\\' + cam_num + '\\' + files[j])
                        shutil.copy2(path + '\\' + files[j2], dst + '\\' + cur_exp_name +'\\' + cam_num + '\\' + files[j2])
                        shutil.copy2(path + '\\' + files[j3], dst + '\\' + cur_exp_name +'\\' + cam_num + '\\' + files[j3])
                        shutil.copy2('\\'.join(path.split('\\')[0:-1]) +'\\' + os.path.basename(path)+"_annotations_v001" + '\\' + files[j].split('.')[0] + "_v001.xml" ,
                                     dst + '\\' + cur_exp_name + '\\' + cam_num + "_annotations_v001" + '\\' + files[j].split('.')[0] + "_v001.xml")
                        shutil.copy2('\\'.join(path.split('\\')[0:-1]) +'\\' + os.path.basename(path)+"_annotations_v001" + '\\' + files[j2].split('.')[0] + "_v001.xml" ,
                                     dst+ '\\' + cur_exp_name + '\\' + cam_num + "_annotations_v001"  + '\\' + files[j2].split('.')[0] + "_v001.xml")
                        shutil.copy2('\\'.join(path.split('\\')[0:-1]) +'\\' + os.path.basename(path)+"_annotations_v001" + '\\' + files[j3].split('.')[0] + "_v001.xml" ,
                                     dst+ '\\' + cur_exp_name + '\\' + cam_num + "_annotations_v001"  + '\\' + files[j3].split('.')[0] + "_v001.xml")
                        suc = 1
                        BREAK = True
                        break
            else:
                pass
        if suc == 0:
            print('fail getting files!!!')
            print(df_sudang.iloc[i]['시험명'])
                # print(df_sudang.iloc[i]['시험명'])
                # print(path.split('\\')[-2][0:3] , len(path.split('\\')[-3]) )

def MakeModifyXML():
    for (path, dirs, files) in os.walk("C:\\Users\\jcy37\\Desktop\\과제\\전측방\\수당수령증_자동화\\수당수령이미지"):
        for file in files:
            if file.split('.')[-1] == 'xml':
                shutil.copy2(path + '\\' + file, path + '\\' + file.split('.')[0] + '_1.xml')


if __name__ == "__main__":
    main()