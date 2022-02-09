import os
import numpy as np
import pandas as pd
import csv
from datetime import datetime
import matplotlib.pyplot as plt
import pickle

start = 0
if start:
    df = pd.read_excel('C:\\Users\\정찬영\\Downloads\\2021-02-09~2022-02-09.xlsx', sheet_name='가계부 내역')
    print(df)
    df['year'] = df['날짜'].dt.year
    df['month'] = df['날짜'].dt.month
    df['day'] = df['날짜'].dt.day

    month_list = []
    for i in range(len(df)):
        case = str(df.loc[i].year) + '_' + str(df.loc[i].month)
        if case not in month_list:
            month_list.append(case)
    TOTAL = pd.DataFrame({})

    for i in range(len(month_list)):
        globals()['Case_{}'.format(month_list[i])] = [0 for _ in range(31)]
        # eval('Case_{}'.format(month_list[i]))[0] = 1
        # print(eval('Case_{}'.format(month_list[i])), i)
        # TOTAL.append('Case-{}'.format(i))

    for i in range(len(df)):
        if df.loc[i]['타입'] == '지출':
            for j in range(df.loc[i].day-1, 31):
                eval('Case_{}'.format(str(df.loc[i].year) + '_' + str(df.loc[i].month)))[j] -= df.loc[i]['금액']

    with open('월내역', 'wb') as f:
        pickle.dump(month_list, f, pickle.HIGHEST_PROTOCOL)
    for i in range(len(month_list)):
        with open('지출내역' + str(month_list[i]), 'wb') as f:
            pickle.dump(eval('Case_{}'.format(month_list[i])), f, pickle.HIGHEST_PROTOCOL)
else:
    with open('월내역', 'rb') as f:
        month_list = pickle.load(f)
    for i in range(len(month_list)):
        with open('지출내역' + str(month_list[i]), 'rb') as f:
            globals()['Case_{}'.format(month_list[i])] = pickle.load(f)
            print('Case_{}'.format(month_list[i]))

current_month = '2022_2'
month_list.remove('2022_2')
month_list.remove('2021_6')
month_list.remove('2021_3')
month_list.remove('2021_2')
AVG = [0 for _ in range(31)]
for i in range(len(month_list)):
    for j in range(31):
        AVG[j] += eval('Case_{}'.format(month_list[i]))[j] / len(month_list)

plt.figure(1)
for i in range(len(month_list)):
    plt.plot(np.arange(1, 32, 1), eval('Case_{}'.format(month_list[i])), label='Case_{}'.format(month_list[i]))
plt.ylabel('consume')
plt.xlabel('days')
plt.xticks(np.arange(0, 32, 1))
plt.yticks(np.arange(0, 2500000, 100000))
plt.grid()
plt.legend()

plt.figure(2)
plt.plot(np.arange(1, 32, 1),eval('Case_{}'.format(current_month)) , label='current_month')
plt.plot(np.arange(1, 32, 1),AVG, label='average')
plt.xticks(np.arange(0, 32, 1))
plt.yticks(np.arange(0, 2500000, 100000))
plt.grid()
plt.legend()
plt.ylabel('consume')
plt.xlabel('days')
plt.show()