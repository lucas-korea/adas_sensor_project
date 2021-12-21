import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
CaseListForTest = ['윤가영1112','노수진1112','배은이1112','정성미1112','박윤미1116','정다운1118','배은이1118',"강인선1118"
    ,"권미애1122","박윤미1122","윤가영1122","이민희1122","노수진1129","권미애1129","박윤미1129","윤가영1129","정다운1130",
        "강인선1130","권미애1206","성미애1207",",정다운1207","윤가영1207","박윤미1209","노수진1209","윤가영1210",
        "박윤미1210","성미애1210", "정다운1025","성선영1026",'윤가영1026']

# PATH안에 있는 *sub.csv(Counting 프로그램 결과파일) 을 이용해, 이미지 별 결과를 활용할 수 있는 코드
def GetAvgOfImages():
    PATH = "H:\\직박"
    a = []
    num = 0
    fifty_over = 0
    ten_under = 0
    print(len(os.listdir(PATH)))
    for file in os.listdir(PATH):
        print(num)
        num = num + 1
        if file[-7:] == 'sub.csv':
            print(file)
            data = pd.read_csv(PATH + '\\' + file)
            data = data.loc[:, ["case name" , "Num_of_Obj"]]
            for i in range(len(data)):
                # print(data.iloc[i]["Num_of_Obj"])
                if data.iloc[i]["case name"] != 'total':
                    a.append(data.iloc[i]['Num_of_Obj'])
                    if (data.iloc[i]['Num_of_Obj'] > 50):
                        fifty_over = fifty_over + 1
                    elif data.iloc[i]['Num_of_Obj'] < 10:
                        ten_under = ten_under + 1
                else:
                    pass

    x = range(len(a))
    print(len(x),' images ')
    print("Avg = ", sum(a)/len(a))
    print("fifty_over = ", fifty_over , 'images')
    print("ten_under = ", ten_under , 'images')
    plt.scatter(x, a)
    plt.show()


# CaseListForTest에 해당하는 case들의 *sub_csv결과를 이용하여 분석
def GetAvgOfImages2():
    a = []
    num = 0
    fifty_over = 0
    ten_under = 0
    PATH = "D:\\GT 생성 업무\\객체생성-검수\\생성완"
    for (path, dir, files) in os.walk(PATH):
        if path[-1] == '_':
            for file in files:
                if file[-7:] == "sub.csv" and file[0:7] in CaseListForTest:
                    print(path + '\\' + file)
                    data = pd.read_csv(path + '\\' + file ,encoding='euc-kr', sep='\t')
                    for i in range(len(data)):
                        if data.iloc[i].values[0].split(',')[0] != 'total' and data.iloc[i].values[0].split(',')[0][:-1] != 'subtotal':
                            a.append(int(data.iloc[i].values[0].split(',')[1]))
                            if (int(data.iloc[i].values[0].split(',')[1]) > 50):
                                fifty_over = fifty_over + 1
                            elif int(data.iloc[i].values[0].split(',')[1]) < 10:
                                ten_under = ten_under + 1
                        else:
                            print(data.iloc[i].values[0].split(',')[0])
    a = np.asarray(a)
    print(fifty_over, ten_under, np.average(a), len(a))



if __name__ == "__main__":
    pass
