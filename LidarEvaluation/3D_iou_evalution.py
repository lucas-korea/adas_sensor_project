import os
import numpy as np
from tkinter import filedialog
from tkinter import messagebox
from scipy.spatial import ConvexHull
from numpy import *
import pandas as pd
import iou
import warnings
warnings.filterwarnings(action='ignore') # pandas append함수 concat으로 쓰라는 warning 무시
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


# row 생략 없이 출력
pd.set_option('display.max_rows', None)
# col 생략 없이 출력
pd.set_option('display.max_columns', None)

# 3D IoU caculate code for 3D object detection
# Kent 2018/12

def select_folder(str_=''):
    folder = filedialog.askdirectory(initialdir=os.getcwd(),
                                        title=str_)
    if folder == '':
        print("폴더을 추가 하세요")
        messagebox.showwarning("경고", "폴더을 추가 하세요")  # 파일 선택 안했을 때 메세지 출력
        exit(1)
    return "\\".join(folder.split("/"))

def make_output_df(output_path_):
    output_files_ = os.listdir(output_path_)
    output_result = pd.DataFrame({"filename" : [],
              "output" : []})
    for i in range(len(output_files_)):
        with open(output_path + '\\' + output_files_[i], 'r') as f:
            file_length = len(f.readlines())
        with open(output_path + '\\' + output_files_[i], 'r') as f:
            output_datas = []
            for u in range(file_length):
                output_data = f.readline()
                output_data_splited = output_data.split(';')
                for j in range(8):
                    output_data_splited[j] = double(output_data_splited[j])
                output_datas.append(output_data_splited)
        output_result.loc[i] = output_files_[i].split('.')[0], output_datas
    return output_result

def make_GT_df(GT_path_):
    GT_files_ = os.listdir(GT_path_)
    GT_result = pd.DataFrame({"filename" : [],
              "GT" : []})
    for i in range(len(GT_files_)):
        with open(GT_path + '\\' + GT_files_[i], 'r') as f:
            file_length = len(f.readlines())
        with open(GT_path + '\\' + GT_files_[i], 'r') as f:
            GT_datas = []
            for line_num in range(file_length):
                GT_data = f.readline()
                GT_data_splited = GT_data.split(';')
                for j in range(8):
                    GT_data_splited[j] = double(GT_data_splited[j])
                GT_datas.append(GT_data_splited)
        GT_result.loc[i] = GT_files_[i].split('.')[0], GT_datas
    return GT_result

def make_IOU_df(IOU_path_):
    IOU_files_ = os.listdir(IOU_path_)
    IOU_result = pd.DataFrame({"filename" : [],
                               "IOU" : []})
    for i in range(len(IOU_files_)):
        IOU_data = pd.read_csv(IOU_path_ + '\\' + IOU_files_[i])
        IOU_datas = []
        for k in range(IOU_data.shape[0]):
            IOU_datas.append(IOU_data.iloc[k, 0].split('\t')[k + 1])
        IOU_result.loc[i] = IOU_files_[i].split('.')[0], IOU_datas
    return IOU_result

def get_class_from_str(input):
    print(input.split(',')[8].replace('\\n', '').replace('\'', '').replace(']', ''))

def sort_matchin_GT_output(matching_df):
    origin_df = matching_df.copy()
    FN = 0
    FP = 0
    matched_row = -1
    matched_col = -2
    matched_key = -3
    # print(matching_df)
    for i in range(origin_df.shape[0]): # 행개수(gt개수) 만큼 반복
        Nlarge_i = 1
        while(matching_df.shape[1] > Nlarge_i - 1 ):
            matched_row = matching_df.astype(float).apply(lambda row: row.nlargest(Nlarge_i),axis=1).index[0] # 기준 GT
            matched_col = matching_df.astype(float).apply(lambda row: row.nlargest(Nlarge_i).index.values[Nlarge_i-1],axis=1).loc[matching_df.astype(float).apply(lambda row: row.nlargest(Nlarge_i),axis=1).index[0]]
            # 기준 GT에 대해 가장 큰 iou를 가진 output
            matched_key = matching_df[matching_df.astype(float).apply(lambda row: row.nlargest(Nlarge_i).index.values[Nlarge_i-1],axis=1)
                  .loc[matching_df.astype(float).apply(lambda row: row.nlargest(Nlarge_i),axis=1).index[0]]].astype(float).idxmax()# 기준 GT에 대해 가장 큰 iou를 가진 output 기준 가장 큰 iou를 가진 GT

            if matched_row == matched_key and get_class_from_str(matched_row) == get_class_from_str(matched_col): break # 가장 큰 iou가 잘 매칭되면 끝
            Nlarge_i += 1
        if matched_row == matched_key: # 서로 잘 매칭 됐으면 매칭된 거 삭제하기
            if matching_df[matched_col][matched_row] < 0.5: # 매칭 됐는데도 불구하고 기준 iou보다 낮으면 fail.
                FP += 1; FN += 1
            matching_df.drop([matched_row], inplace=True)
            matching_df.drop([matched_col], axis='columns', inplace=True)
        elif matching_df.shape[1] == 0: # GT는 아직 남아있는데, output이 없는 경우 FN에 남는 GT만큼 추가시키고, GT 모두 삭제
            FN += matching_df.shape[0]
            matching_df.drop(matching_df.index.values, inplace=True)
            break
        else: # 탐색을 다 했는데도 매칭이 안됐으면 GT에 매칭되는게 없는것으로 판정, GT를 삭제하고 FN 카운트
            matching_df.drop([matched_row], inplace=True)
            FN += 1
    FP += matching_df.shape[1] # 남은 output은 FP로 판정
    TP = origin_df.shape[0] - FN # 본래 GT에서 FN을 빼면 TP
    print("FN {}, FP {}, TP {}".format(FN, FP, TP))

    return ()



def matching_GT_output(result_frame):
    matching_df = pd.DataFrame()
    for j in range(len(result_frame['GT'])):
        matching_df = matching_df.append(pd.Series(dtype="object", name=str(result_frame['GT'][j])))
    for i in range(len(result_frame['output'])):
        matching_df.insert(i, str(result_frame['output'][i]), '')
    matching_df2 = matching_df.copy()
    for GT_i in range(len(result_frame['GT'])):
        for output_i in range(len(result_frame['output'])):
            matching_df2.iloc[GT_i][str(result_frame['output'][output_i])] = iou.evaluate_IoU(result_frame['GT'][GT_i], result_frame['output'][output_i], 0.5)[0]
    sort_matchin_GT_output(matching_df2)
    return matching_df2


if __name__ == '__main__':
    # output_path = select_folder("평가 결과가 모여져 있는 폴더")
    # GT_path = select_folder("GT 폴더")
    GT_path = "C:\\Users\\jcy37\\Downloads\\label"
    output_path = "C:\\Users\\jcy37\\Downloads\\objects"
    IOU_path = "C:\\Users\\jcy37\\Downloads\\iou"

    output_files = os.listdir(output_path)
    result = pd.merge(make_GT_df(GT_path_=GT_path), make_output_df(output_path_=output_path), on="filename", how="outer")
    result = pd.merge(result, make_IOU_df(IOU_path_=IOU_path),  on="filename", how="outer")
    result["my_IOU"] = None
    result["IOU_gap"] = None
    for i in range(len(result)):
        my_IOU_unit = []
        IOU_gap_unit = []
        if type(result["IOU"][i]) is float: # GT만 있고 output은 없는 경우
            pass
        elif type(result["GT"][i]) is float: # output만 있고 GT는 없는 경우
            pass
        else:
            matching_GT_output(result.loc[i])
            for j in range(len(result["IOU"][i])):
                GT_obj = result['GT'][i][j]
                output_obj = result['output'][i][j]
                IoU_3D, flag_detected = iou.evaluate_IoU(GT_obj, output_obj, 0.5)
                my_IOU_unit.append('{0:0.3f}'.format(IoU_3D))
                if result["IOU"][i][j] == '':
                    IOU_gap_unit.append('{0:0.3f}'.format(abs(IoU_3D - 0)))
                else:
                    IOU_gap_unit.append('{0:0.3f}'.format(abs(IoU_3D - float(result["IOU"][i][j]))))

        result['my_IOU'][i] = my_IOU_unit
        result['IOU_gap'][i] = IOU_gap_unit
    # result.to_csv("test.csv")



###################################
# matched_row = matching_df.astype(float).idxmax(axis=1).index.values[0]  # 기준 GT
# matched_col = matching_df.astype(float).idxmax(axis=1).values[0]  # 기준 GT에 대해 가장 큰 iou를 가진 output
# matched_key = matching_df[matched_col].astype(float).idxmax()  # 기준 GT에 대해 가장 큰 iou를 가진 output 기준 가장 큰 iou를 가진 GT
#
# matching_df[matching_df.columns.values[0]].iloc[1] = 0.3
# matching_df[matching_df.columns.values[0]].iloc[2] = 0.2
#
# matching_df[matching_df.columns.values[1]].iloc[0] = 0.3
# matching_df[matching_df.columns.values[1]].iloc[2] = 0.1
# matching_df[matching_df.columns.values[2]].iloc[0] = 0.4
# matching_df[matching_df.columns.values[2]].iloc[1] = 0.1