import os
import numpy as np
from tkinter import filedialog
from tkinter import messagebox
from scipy.spatial import ConvexHull
from numpy import *
import pandas as pd
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
              "result" : []})
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
        output_result.loc[i] = [output_files_[i], output_datas]
    return output_result

def make_GT_df(GT_path_):
    GT_files_ = os.listdir(GT_path_)
    GT_result = pd.DataFrame({"filename" : [],
              "result" : []})
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
        GT_result.loc[i] = [GT_files_[i], GT_datas]
    return GT_result

if __name__ == '__main__':
    # output_path = select_folder("평가 결과가 모여져 있는 폴더")
    # GT_path = select_folder("GT 폴더")
    GT_path = "C:\\Users\\jcy37\\Desktop\\과제\\3D High resolution 라이다\\라이다 평가 Tool sw 개발\\sunny[seoul robotics]\\south_to_west\\label"
    output_path = "C:\\Users\\jcy37\\Desktop\\과제\\3D High resolution 라이다\\라이다 평가 Tool sw 개발\\sunny[seoul robotics]\\output\\objects"
    file_length = 0

    output_files = os.listdir(output_path)
    result_merge = pd.merge(make_GT_df(GT_path_=GT_path), make_output_df( output_path_=output_path), on="filename", how="outer")

    # for i in range(len(result_merge)):
    #     for output_obj in result_merge.loc[i]["result_x"]:
    #         for GT_obj in result_merge.loc[i]




    #     corners_3d_ground = get_3d_box((result['GT'][i][q][4], result['GT'][i][q][5], result['GT'][i][q][6]), result['GT'][i][q][7],
    #                                    (result['GT'][i][q][1], result['GT'][i][q][2], result['GT'][i][q][3]))
    #     corners_3d_predict = get_3d_box((result['output'][i][q][4], result['output'][i][q][5], result['output'][i][q][6]), result['output'][i][q][7],
    #                                     (result['output'][i][q][1], result['output'][i][q][2], result['output'][i][q][3]))
    #     (IOU_3d, IOU_2d) = box3d_iou(corners_3d_predict, corners_3d_ground) # 3d IoU/ 2d IoU of BEV(bird eye's view)
    #     print("IOU3d:\n", IOU_3d)
    IOU_path = "C:\\Users\\jcy37\\Desktop\\과제\\3D High resolution 라이다\\라이다 평가 Tool sw 개발\\sunny[seoul robotics]\\evaluation\\iou"
    IOU_data = pd.read_csv(IOU_path + '\\' + output_files[67].split('.')[0] + '.csv')
    # print(IOU_data)
    for k in range(IOU_data.shape[0]):
        # print(IOU_data.iloc[k,0].replace(" ", ""))
        print(IOU_data.iloc[k,0].split('\t')[k+1])


        # print(IOU_data.iloc[0])
        # exit(1)
        # print('\n')
        # with open( + '.csv', 'r') as f:
        #     rdr = csv.reader(f)
            # for line in rdr:
            #     print(line[0].split('\t'))
            # exit(1)
            # # IOU_data = f.read()
            # # print(IOU_data)