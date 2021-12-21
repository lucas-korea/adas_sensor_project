import os
import shutil
import pandas as pd
import math
from PIL import Image


# 작업자별 할당및통계와 김선임님 Counting 프로그램 결과물을 이용해 생성작업 수당 계산
# 할당및 통계에서는 케이스 이름과 그에 해당하는 이미지 속성만 추출
# 김선임님 Counting 프로그램의 경우, 전체 합산 결과와 각 케이스별 개발 결과는 오차가 있으므로 참고
def CalculateCreatePay():
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


#file_source로부터, dst에 대회용 파일구조를 build. 연월일_시분초 이름을 가지고 있어야 하며, 이미지,xml이름을 기준으로 폴더, 파일을 생성(이동)한다
def build_contest_filetree():
    file_source = "C:\\Users\\jcy37\\Desktop\\컨테스트 파일\\학습용데이터\\컨테스트_학습용_주간_xml"
    dst =         "C:\\Users\\jcy37\\Desktop\\컨테스트 파일\\학습용데이터\\컨테스트_학습용_주간_img_파일구조완성"
    dst = dst + '\\'
    cnt = 0
    for (path, dir, files) in os.walk(file_source):
        print(path)
        print(len(os.listdir(path)))
        for file in files:
            print(cnt)
            cnt = cnt + 1
            if file.split('.')[1] == 'jpg--' or file.split('.')[1] == 'png--':
                if file[1] == '_':
                    try:
                        shutil.move(path + '\\' + file, dst + file.split('_')[1] + '_' + file.split('_')[2] + '\\' + file[0] + '\\' + file)
                    except FileNotFoundError:
                        os.makedirs(dst + file.split('_')[1] + '_' + file.split('_')[2] + '\\' + file[0])
                        shutil.move(path + '\\' + file , dst + file.split('_')[1] + '_' + file.split('_')[2] + '\\' + file[0] + '\\' + file)
                else:
                    print('wrong file')
                    print(file)
            # if file.split('.')[1] == 'png':
            #     im = Image.open(path + '\\' + file).convert('RGB')
            #     im.save(path + '\\' + file.split('.')[0] + '.jpg', 'jpeg')
            elif file[-10:] == "v001_1.xml":
                if file[1] == '_':
                    try:
                        shutil.move(path + '\\' + file , dst + file.split('_')[1] + '_' + file.split('_')[2] + '\\' + file[0] + '_annotations_v001_1' + '\\' + file)
                    except FileNotFoundError:
                        os.makedirs(dst + file.split('_')[1] + '_' + file.split('_')[2] + '\\' + file[0] + '_annotations_v001_1')
                        shutil.move(path + '\\' + file , dst + file.split('_')[1] + '_' + file.split('_')[2] + '\\' + file[0] + '_annotations_v001_1' + '\\' + file)
                else:
                    print('wrong file')
                    print(file)

#file_source내의 png파일을 jpg로 바꾸기. 동일 폴더 내에 생성. png를 삭제할지, 말지는 알아서.
def png2jpg():
    file_source = "C:\\Users\\jcy37\\Desktop\\과제\\전측방\\수당수령증_자동화\\수당수령이미지_파일명검수버전"
    cnt = 0
    for (path, dir, files) in os.walk(file_source):
        print(path)
        print(len(os.listdir(path)))
        for file in files:
            print(cnt)
            cnt = cnt + 1
            if file.split('.')[1] == 'png':
                try:
                    im = Image.open(path + '\\' + file).convert('RGB')
                    im.save(path + '\\' + file.split('.')[0] + '.jpg', 'jpeg')
                    os.remove(path + '\\' + file)
                except OSError as e:
                    print(e)
                    print(path + '\\' + file)
                    f = open("오류파일2.txt", 'a')
                    f.write(str(e))
                    f.write(path + '\\' + file)
                    f.write('\n')
                    f.close()

# 상위폴더 이름이 yyyymmdd_hhmmss 와 같은 형태(길이기준)일 때, 하위 폴더 (1, 1_annotations_v001 등) 들은 각각 같은 파일 수를 가지고 있는지 확인
# 하지만 두 쌍의 img-xml 밖에 체크 못하는 구조, (a,b,c,d)
def checking_same_imgxml_number():
    file_source = "C:\\Users\\jcy37\\Desktop\\컨테스트 파일\\학습용데이터\\컨테스트_학습용_주간_img_파일구조완성"
    for (path, dirs, files) in os.walk(file_source):
        if len(path.split('\\')[-1]) == 15:
            a = len(os.listdir(path + '\\' + dirs[0]))
            b = len(os.listdir(path + '\\' + dirs[1]))
            try:
                c = len(os.listdir(path + '\\' + dirs[2]))
                d = len(os.listdir(path + '\\' + dirs[3]))
                if c != d:
                    print(path)
                    print(dirs[2], dirs[3])
            except:
                pass
            if a != b:
                print(path)
                print(dirs[0], dirs[1])

#file_source에서, 내가 원하는 특징의(ex.파일확장자) 파일의 개수 counting
def CountImageThatIwant():
    file_source = "C:\\Users\\jcy37\\Desktop\\컨테스트 파일\\학습용데이터\\컨테스트_학습용_통합_img_파일구조완성"
    cnt = 0
    with open("testdatalist.txt", 'a') as f:
        for (path, dirs, files) in os.walk(file_source):
            for file in files:
                if file.split('.')[-1] == 'png':
                    print(cnt)
                    cnt = cnt + 1
                    f.write(file)
                    f.write('\n')

def GettCorrespondingXml(): #file_source에서, jpg 파일을 찾아, 그에 대응되는 xml 파일을 dst(혹은 특정 루트) 에서부터 파일을 가져오는 코드
    file_source = "C:\\Users\\jcy37\\Desktop\\컨테스트 파일\\학습용데이터\\컨테스트_학습용_통합_img_파일구조완성"
    # dst = "C:\\Users\\jcy37\\Desktop\\컨테스트 파일\\학습용데이터\\컨테스트_학습용_통합_xml_파일구조완성"
    # dst = dst + '\\'
    cnt = 0
    for (path, dirs, files) in os.walk(file_source):
        for file in files:
            if file.split('.')[-1] == 'jpg':
                print(cnt)
                cnt = cnt + 1
                try:
                    shutil.move("C:\\Users\\jcy37\\Desktop\\컨테스트 파일\\학습용데이터\\컨테스트_학습용_통합_xml" + '\\' + file.split('.')[0] + '_v001_1.xml',
                                 path + '\\' + file.split('.')[0] + '_v001_1.xml')
                except:
                    print(path, file)
if __name__ == "__main__":
    CountInspection2()