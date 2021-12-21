import pandas as pd
import os

# 내가 작성했던 엑셀파일(미첨부(내부문서)_온라인 작업자별_할당및통계)을 이용해 검수자별 작업 이미지 수를 계산
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

def CountInspection2():
    PATH = "D:\\GT 생성 업무\\객체생성-검수\\검수완"
    ShinSungRae_frame = []
    SungSunYoung_frame = []
    KimMinSer_frame = []
    SungMiAe_frame = []
    ShinSungRae_obj = []
    SungSunYoung_obj = []
    KimMinSer_obj = []
    SungMiAe_obj = []
    ShinSungRae_line = []
    SungSunYoung_line = []
    KimMinSer_line = []
    SungMiAe_line = []
    for (path, dirs, files) in os.walk(PATH):
        up_folder = path.split('\\')[-1]
        if up_folder in ['1','2','3','4'] and path.split('\\')[-2] == '검수완':
            data = pd.read_csv(path + '\\' + 'total_obj.csv', encoding='euc-kr', sep='\t')
            for i in range(len(data)):
                if len(data.iloc[i].values[0].split(',')[1]) < 3:
                    print(data.iloc[i].values[0].split(',')[1])
                    pass
                elif up_folder == '1':
                    KimMinSer_frame.append(int(data.iloc[i].values[0].split(',')[2]))
                    KimMinSer_obj.append(int(data.iloc[i].values[0].split(',')[3]))
                elif up_folder == '2':
                    SungMiAe_frame.append(int(data.iloc[i].values[0].split(',')[2]))
                    SungMiAe_obj.append(int(data.iloc[i].values[0].split(',')[3]))
                elif up_folder == '3':
                    SungSunYoung_frame.append(int(data.iloc[i].values[0].split(',')[2]))
                    SungSunYoung_obj.append(int(data.iloc[i].values[0].split(',')[3]))
                elif up_folder == '4':
                    ShinSungRae_frame.append(int(data.iloc[i].values[0].split(',')[2]))
                    ShinSungRae_obj.append(int(data.iloc[i].values[0].split(',')[3]))
            data = pd.read_csv(path + '\\' + 'total_line.csv', encoding='euc-kr', sep='\t')
            for i in range(len(data)-1):
                i = i + 1
                if data.iloc[i].values[0].split(',')[1] != '':
                    pass
                elif up_folder == '1':
                    KimMinSer_line.append(int(data.iloc[i].values[0].split(',')[3]))
                elif up_folder == '2':
                    SungMiAe_line.append(int(data.iloc[i].values[0].split(',')[3]))
                elif up_folder == '3':
                    SungSunYoung_line.append(int(data.iloc[i].values[0].split(',')[3]))
                elif up_folder == '4':
                    ShinSungRae_line.append(int(data.iloc[i].values[0].split(',')[3]))
    print("SungMiAe - frame : ", str(sum(SungMiAe_frame)), "obj : ", str(sum(SungMiAe_obj) + sum(SungMiAe_line)))
    print("SungSunYoung - frame : ", str(sum(SungSunYoung_frame)), "obj : ", str(sum(SungSunYoung_obj) + sum(SungSunYoung_line)))
    print("ShinSungRae - frame : " , str(sum(ShinSungRae_frame)) , "obj : " ,str(sum(ShinSungRae_obj) + sum(ShinSungRae_line)))
    print("KimMinSer - frame : ", str(sum(KimMinSer_frame)), "obj : ", str(sum(KimMinSer_obj) + sum(KimMinSer_line)))

if __name__ == "__main__":
    CountInspection2()