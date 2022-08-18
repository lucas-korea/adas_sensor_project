import os
import numpy as np
import pandas as pd
import csv
from datetime import datetime
import matplotlib.pyplot as plt
import pickle

start = 1
simple = 0
if simple:
 pass
elif start:
    df = pd.read_excel('2021-08-12~2022-08-12.xlsx', sheet_name='가계부 내역')
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
        print(i, '/', len(df))
        if df.loc[i]['타입'] == '지출' and df.loc[i]['내용'] != "(학)한동대학교(갈" and df.loc[i]['내용'] != "감사의기적교회"\
                and df.loc[i]['대분류'] != "주거/통신" and df.loc[i]['대분류'] != "경조사" and df.loc[i]['대분류'] != "의료/건강":
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

current_month = '2022_8'
# month_list.remove('2022_2')
# month_list.remove('2021_6')
# # month_list.remove('2021_3')
# # month_list.remove('2021_2')
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
plt.yticks(np.arange(0, 3000000, 100000))
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