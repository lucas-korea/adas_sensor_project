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
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
import math
import gc
# row 생략 없이 출력
pd.set_option('display.max_rows', None)
# col 생략 없이 출력
pd.set_option('display.max_columns', None)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
xyz_lim = 10


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
        output_result.loc[i] = os.path.basename(output_files_[i]), output_datas
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
        GT_result.loc[i] = os.path.basename(GT_files_[i]), GT_datas
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
    return input.split(',')[8].replace('\\n', '').replace('\'', '').replace(']', '')

def sort_matchin_GT_output(matching_df):
    origin_df = matching_df.copy()
    FN = 0
    FP = 0
    new_my_iou = []
    for i in range(origin_df.shape[0]): # 행개수(gt개수) 만큼 반복
        matched_row = -1
        matched_col = -2
        matched_key = -3
        Nlarge_i = 1
        while(matching_df.shape[1] > Nlarge_i - 1 ):
            matched_row = matching_df.astype(float).apply(lambda row: row.nlargest(Nlarge_i),axis=1).index[0] # 기준 GT
            matched_col = matching_df.astype(float).apply(lambda row: row.nlargest(Nlarge_i).index.values[Nlarge_i-1],axis=1).loc[matching_df.astype(float).apply(lambda row: row.nlargest(Nlarge_i),axis=1).index[0]]
            # 기준 GT에 대해 가장 큰 iou를 가진 output
            matched_key = matching_df[matching_df.astype(float).apply(lambda row: row.nlargest(Nlarge_i).index.values[Nlarge_i-1],axis=1)
                  .loc[matching_df.astype(float).apply(lambda row: row.nlargest(Nlarge_i),axis=1).index[0]]].astype(float).idxmax()# 기준 GT에 대해 가장 큰 iou를 가진 output 기준 가장 큰 iou를 가진 GT

            if matched_row == matched_key and get_class_from_str(matched_row) == get_class_from_str(matched_col):
                break # 가장 큰 iou가 잘 매칭되면 끝
            Nlarge_i += 1
        if matched_row == matched_key: # 서로 잘 매칭 됐으면 매칭된 거 삭제하기
            if matching_df[matched_col][matched_row] < 0.5: # 매칭 됐는데도 불구하고 기준 iou보다 낮으면 fail.
                FP += 1; FN += 1
            new_my_iou.append(matching_df[matched_col][matched_row])
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
    # print("FN {}, FP {}, TP {}".format(FN, FP, TP))
    return new_my_iou, TP, FP, FN

# string화 된 obj 정보를 다시 list화
def str2list(bbox_data):
    bbox_data = bbox_data.replace('[', '').replace(']', '').replace('\\n', '').replace('\'', '').replace(' ', '').split(',')
    return float(bbox_data[0]), float(bbox_data[1]), float(bbox_data[2]), float(bbox_data[3]), \
           float(bbox_data[4]), float(bbox_data[5]), float(bbox_data[6]), float(bbox_data[7]), bbox_data[8]

# GT, output annotation 정보를 취합한 dataframe으로 부터, iou+class 기반 매칭.
def matching_GT_output(result_frame):
    matching_df = pd.DataFrame()
    for j in range(len(result_frame['GT'])):
        if not chekc_isin_ROI(result_frame['GT'][j]):
            continue
        matching_df = matching_df.append(pd.Series(dtype="object", name=str(result_frame['GT'][j])))
    cnt = 0
    for i in range(len(result_frame['output'])):
        if not chekc_isin_ROI(result_frame['output'][i]):
            cnt += 1
            continue
        matching_df.insert(i - cnt, str(result_frame['output'][i]), '')# 열을 insert할 때는 index 인자를 넣어야 하는데, for문의 iterator로는 continue 문의 상황을 반영하지 못하므로 cnt를 감하여 보정.
    matching_df2 = matching_df.copy()
    for GT_i in range(matching_df2.shape[0]):
        for output_i in range(matching_df2.shape[1]):
            matching_df2.iloc[GT_i][matching_df2.columns.values[output_i]]\
                = iou.evaluate_IoU(str2list(matching_df2.index[GT_i]),str2list(matching_df2.columns.values[output_i]), 0.5)[0]
    draw_3d_Bbox(matching_df2)  # 정보 취합된 dataframe으로부터 시각화
    return sort_matchin_GT_output(matching_df2)

# 시각화
draw_cnt = 0
def draw_3d_Bbox(matching_df2):
    global draw_cnt
    draw_cnt += 1
    plt.cla()
    for GT in matching_df2.index:
        id, cx, cy, bz, l, w, h, yaw, cla = str2list(GT)
        x_corners = [l / 2 + cx, l / 2 + cx, -l / 2 + cx, -l / 2 + cx, l / 2 + cx, l / 2 + cx, -l / 2 + cx,
                     -l / 2 + cx]
        y_corners = [w / 2 + cy, w / 2 + cy, w / 2 + cy, w / 2 + cy, -w / 2 + cy, -w / 2 + cy, -w / 2 + cy,
                     -w / 2 + cy]
        z_corners = [h / 2 + bz + h/2, -h / 2 + bz + h/2, -h / 2 + bz + h/2, h / 2 + bz + h/2, h / 2 + bz + h/2, -h / 2 + bz + h/2, -h / 2 + bz + h/2,
                     h / 2 + bz + h/2]
        corners_3d = np.stack([x_corners,y_corners,z_corners], axis=1)
        bbox= [[corners_3d[0],corners_3d[1],corners_3d[2],corners_3d[3]],
               [corners_3d[4],corners_3d[5],corners_3d[6],corners_3d[7]],
               [corners_3d[0],corners_3d[1],corners_3d[5],corners_3d[4]],
               [corners_3d[2],corners_3d[3],corners_3d[7],corners_3d[6]],
               [corners_3d[1],corners_3d[2],corners_3d[6],corners_3d[5]],
               [corners_3d[4],corners_3d[7],corners_3d[3],corners_3d[0]]]
        ax.add_collection3d(Poly3DCollection(bbox, facecolors='red', linewidths=1, edgecolors='r', alpha=0.3))
    for output in matching_df2.columns.values:
        id, cx, cy, bz, l, w, h, yaw, cla = str2list(output)
        x_corners = [l / 2 + cx, l / 2 + cx, -l / 2 + cx, -l / 2 + cx, l / 2 + cx, l / 2 + cx, -l / 2 + cx,
                     -l / 2 + cx]
        y_corners = [w / 2 + cy, w / 2 + cy, w / 2 + cy, w / 2 + cy, -w / 2 + cy, -w / 2 + cy, -w / 2 + cy,
                     -w / 2 + cy]
        z_corners = [h / 2 + bz + h/2, -h / 2 + bz + h/2, -h / 2 + bz + h/2, h / 2 + bz + h/2, h / 2 + bz + h/2, -h / 2 + bz + h/2, -h / 2 + bz + h/2,
                     h / 2 + bz + h/2]
        corners_3d = np.stack([x_corners, y_corners, z_corners], axis=1)
        bbox = [[corners_3d[0], corners_3d[1], corners_3d[2], corners_3d[3]],
                [corners_3d[4], corners_3d[5], corners_3d[6], corners_3d[7]],
                [corners_3d[0], corners_3d[1], corners_3d[5], corners_3d[4]],
                [corners_3d[2], corners_3d[3], corners_3d[7], corners_3d[6]],
                [corners_3d[1], corners_3d[2], corners_3d[6], corners_3d[5]],
                [corners_3d[4], corners_3d[7], corners_3d[3], corners_3d[0]]]
        ax.add_collection3d(Poly3DCollection(bbox, facecolors='blue', linewidths=1, edgecolors='b', alpha=0.3))
    ax.set_xlim(-xyz_lim, xyz_lim)
    ax.set_ylim(-xyz_lim, xyz_lim)
    ax.set_zlim(-xyz_lim, xyz_lim)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.text(-10, 0, 7, "{} / {}".format(draw_cnt, file_len) )
    plt.pause(0.001)
    gc.collect()

VROI = [-22.5, +22.5] # 60분법 각도
HROI = [0, 360]
MINIMUM_SIZE_X = 0
MINIMUM_SIZE_Y = 0
VROI[0] = float(input("Minimun Vertical ROI [degree] :: "))
VROI[1] = float(input("Maximum Vertical ROI [degree] :: "))
HROI[0] = float(input("Minimun Horizontal ROI [degree] :: "))
HROI[1] = float(input("Maximum Horizontal ROI [degree] :: "))
MINIMUM_SIZE_X = float(input("MINIMUM_SIZE_X [meter] :: "))
MINIMUM_SIZE_Y = float(input("MINIMUM_SIZE_Y [meter] :: "))

# object가 ROI에 해당하는지, 최소 사이즈 이상인지 TorF 판단
def chekc_isin_ROI(obj):
    HAngle = math.atan(obj[2] / obj[1]) / math.pi * 180.0
    if obj[1] < 0: #2,3사분면
        HAngle += 180.0
    elif obj[2] < 0 and obj[1] > 0: # 4사분면
        HAngle += 360.0
    VAngle = math.atan(obj[3] / math.sqrt(obj[2]*obj[2] + obj[1]*obj[1]))/ math.pi * 180.0
    if HROI[0] <= HAngle <= HROI[1] and VROI[0] <= VAngle <= VROI[1] \
            and obj[4] > MINIMUM_SIZE_X and obj[5] > MINIMUM_SIZE_Y:
        return True
    print("False")
    return False


file_len = 0
if __name__ == '__main__':
    output_path = select_folder("평가 결과가 모여져 있는 폴더")
    GT_path = select_folder("GT 폴더")
    sum_TP_FP_FN = [0,0,0]
    # GT_path = "C:\\Users\\jcy37\\Desktop\\과제\\3D High resolution 라이다\\라이다 평가 Tool sw 개발\\2022_11_07_14_27_04_920\\2022_11_07_14_27_04_920\\label"
    # output_path = "C:\\Users\\jcy37\\Desktop\\과제\\3D High resolution 라이다\\라이다 평가 Tool sw 개발\\2022_11_07_14_27_04_920\\2022_11_07_14_27_04_920\\result"
    output_files = os.listdir(output_path)
    file_len = len(output_files)
    result = pd.merge(make_GT_df(GT_path_=GT_path), make_output_df(output_path_=output_path), on="filename", how="outer")
    result["my_IOU"] = None
    result["TP"] = None
    result["FP"] = None
    result["FN"] = None

    for i in range(len(result)):
        my_IOU_unit = []
        TP_unit = 0
        FP_unit = 0
        FN_unit = 0
        if type(result["output"][i]) is float and type(result["GT"][i]) is float: #GT, output 둘다 없는 경우
            pass
        if type(result["output"][i]) is float: # GT만 있고 output은 없는 경우
            sum_TP_FP_FN[1] += len(result["GT"][i])
        elif type(result["GT"][i]) is float: # output만 있고 GT는 없는 경우
            sum_TP_FP_FN[2] += len(result["output"][i])
        else:
            my_IOU_unit, TP_unit, FP_unit, FN_unit = matching_GT_output(result.loc[i])
            sum_TP_FP_FN[0] += TP_unit
            sum_TP_FP_FN[1] += FP_unit
            sum_TP_FP_FN[2] += FN_unit

        result['my_IOU'][i] = my_IOU_unit
        result['TP'][i] = TP_unit
        result['FP'][i] = FP_unit
        result['FN'][i] = FN_unit
    print("TP : {}, FP : {}, FN : {}".format(sum_TP_FP_FN[0] ,sum_TP_FP_FN[1] ,sum_TP_FP_FN[2]))
    result.to_csv("test.csv")
