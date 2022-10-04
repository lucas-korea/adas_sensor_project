import os
import numpy as np
from tkinter import filedialog
from tkinter import messagebox
from scipy.spatial import ConvexHull
from numpy import *
import pandas as pd
import iou

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





def polygon_clip(subjectPolygon, clipPolygon):
    """ Clip a polygon with another polygon.
    Ref: https://rosettacode.org/wiki/Sutherland-Hodgman_polygon_clipping#Python
    Args:
      subjectPolygon: a list of (x,y) 2d points, any polygon.
      clipPolygon: a list of (x,y) 2d points, has to be *convex*
    Note:
      **points have to be counter-clockwise ordered**
    Return:
      a list of (x,y) vertex point for the intersection polygon.
    """

    def inside(p):
        return (cp2[0] - cp1[0]) * (p[1] - cp1[1]) > (cp2[1] - cp1[1]) * (p[0] - cp1[0])

    def computeIntersection():
        dc = [cp1[0] - cp2[0], cp1[1] - cp2[1]]
        dp = [s[0] - e[0], s[1] - e[1]]
        n1 = cp1[0] * cp2[1] - cp1[1] * cp2[0]
        n2 = s[0] * e[1] - s[1] * e[0]
        n3 = 1.0 / (dc[0] * dp[1] - dc[1] * dp[0])
        return [(n1 * dp[0] - n2 * dc[0]) * n3, (n1 * dp[1] - n2 * dc[1]) * n3]

    outputList = subjectPolygon
    cp1 = clipPolygon[-1]

    for clipVertex in clipPolygon:
        cp2 = clipVertex
        inputList = outputList
        outputList = []
        s = inputList[-1]

        for subjectVertex in inputList:
            e = subjectVertex
            if inside(e):
                if not inside(s):
                    outputList.append(computeIntersection())
                outputList.append(e)
            elif inside(s):
                outputList.append(computeIntersection())
            s = e
        cp1 = cp2
        if len(outputList) == 0:
            return None
    return (outputList)


def poly_area(x, y):
    """ Ref: http://stackoverflow.com/questions/24467972/calculate-area-of-polygon-given-x-y-coordinates """
    return 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))


def convex_hull_intersection(p1, p2):
    """ Compute area of two convex hull's intersection area.
        p1,p2 are a list of (x,y) tuples of hull vertices.
        return a list of (x,y) for the intersection and its volume
    """
    inter_p = polygon_clip(p1, p2)
    if inter_p is not None:
        hull_inter = ConvexHull(inter_p)
        return inter_p, hull_inter.volume
    else:
        return None, 0.0


def box3d_vol(corners):
    ''' corners: (8,3) no assumption on axis direction '''
    a = np.sqrt(np.sum((corners[0, :] - corners[1, :]) ** 2))
    b = np.sqrt(np.sum((corners[1, :] - corners[2, :]) ** 2))
    c = np.sqrt(np.sum((corners[0, :] - corners[4, :]) ** 2))
    return a * b * c


def is_clockwise(p):
    x = p[:, 0]
    y = p[:, 1]
    return np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)) > 0


def box3d_iou(corners1, corners2):
    ''' Compute 3D bounding box IoU.
    Input:
        corners1: numpy array (8,3), assume up direction is negative Y
        corners2: numpy array (8,3), assume up direction is negative Y
    Output:
        iou: 3D bounding box IoU
        iou_2d: bird's eye view 2D bounding box IoU
    todo (kent): add more description on corner points' orders.
    '''
    # corner points are in counter clockwise order
    rect1 = [(corners1[i, 0], corners1[i, 2]) for i in range(3, -1, -1)]
    rect2 = [(corners2[i, 0], corners2[i, 2]) for i in range(3, -1, -1)]

    area1 = poly_area(np.array(rect1)[:, 0], np.array(rect1)[:, 1])
    area2 = poly_area(np.array(rect2)[:, 0], np.array(rect2)[:, 1])

    inter, inter_area = convex_hull_intersection(rect1, rect2)
    iou_2d = inter_area / (area1 + area2 - inter_area)
    ymax = min(corners1[0, 1], corners2[0, 1])
    ymin = max(corners1[4, 1], corners2[4, 1])

    inter_vol = inter_area * max(0.0, ymax - ymin)

    vol1 = box3d_vol(corners1)
    vol2 = box3d_vol(corners2)
    iou = inter_vol / (vol1 + vol2 - inter_vol)
    return iou, iou_2d


# ----------------------------------
# Helper functions for evaluation
# ----------------------------------

def get_3d_box(box_size, heading_angle, center):
    ''' Calculate 3D bounding box corners from its parameterization.
    Input:
        box_size: tuple of (length,wide,height)
        heading_angle: rad scalar, clockwise from pos x axis
        center: tuple of (x,y,z)
    Output:
        corners_3d: numpy array of shape (8,3) for 3D box cornders
    '''

    def roty(t):
        c = np.cos(t)
        s = np.sin(t)
        return np.array([[c, 0, s],
                         [0, 1, 0],
                         [-s, 0, c]])

    R = roty(heading_angle)
    l, w, h = box_size
    x_corners = [l / 2, l / 2, -l / 2, -l / 2, l / 2, l / 2, -l / 2, -l / 2];
    y_corners = [h / 2, h / 2, h / 2, h / 2, -h / 2, -h / 2, -h / 2, -h / 2];
    z_corners = [w / 2, -w / 2, -w / 2, w / 2, w / 2, -w / 2, -w / 2, w / 2];
    corners_3d = np.dot(R, np.vstack([x_corners, y_corners, z_corners]))
    corners_3d[0, :] = corners_3d[0, :] + center[0];
    corners_3d[1, :] = corners_3d[1, :] + center[1];
    corners_3d[2, :] = corners_3d[2, :] + center[2];
    corners_3d = np.transpose(corners_3d)
    return corners_3d

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

def bubble_sort(result):
    pass

if __name__ == '__main__':
    # output_path = select_folder("평가 결과가 모여져 있는 폴더")
    # GT_path = select_folder("GT 폴더")
    GT_path = "C:\\Users\\jcy37\\Desktop\\과제\\3D High resolution 라이다\\라이다 평가 Tool sw 개발\\sunny[seoul robotics]\\south_to_west\\label"
    output_path = "C:\\Users\\jcy37\\Desktop\\과제\\3D High resolution 라이다\\라이다 평가 Tool sw 개발\\sunny[seoul robotics]\\output\\objects"
    IOU_path = "C:\\Users\\jcy37\\Desktop\\과제\\3D High resolution 라이다\\라이다 평가 Tool sw 개발\\sunny[seoul robotics]\\evaluation\\iou"

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
        else:
            for j in range(len(result["IOU"][i])):
                GT_obj = result['GT'][i][j]
                output_obj = result['output'][i][j]
                corners_3d_ground = get_3d_box((GT_obj[4], GT_obj[6], GT_obj[5]), GT_obj[7],(GT_obj[1],GT_obj[3], GT_obj[2]))
                corners_3d_predict = get_3d_box((output_obj[4], output_obj[6], output_obj[5]), output_obj[7],(output_obj[1], output_obj[3], output_obj[2] ))
                IoU_3D, flag_detected = iou.evaluate_IoU(GT_obj, output_obj, 0.5)
                # (IOU_3d, IOU_2d) = box3d_iou(corners_3d_predict,corners_3d_ground)  # 3d IoU/ 2d IoU of BEV(bird eye's view)
                my_IOU_unit.append('{0:0.3f}'.format(IoU_3D))
                if result["IOU"][i][j] == '':
                    IOU_gap_unit.append('{0:0.3f}'.format(abs(IoU_3D - 0)))
                else:
                    IOU_gap_unit.append('{0:0.3f}'.format(abs(IoU_3D - float(result["IOU"][i][j]))))

        result['my_IOU'][i] = my_IOU_unit
        result['IOU_gap'][i] = IOU_gap_unit
    # result.to_csv("test2.csv")
