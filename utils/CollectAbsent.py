import pandas as pd
import os
import csv

def CollectAbsent():
    dir_path = "C:\\Users\\jcy37\\Downloads"
    file_list = os.listdir(dir_path)
    file_list = [file for file in file_list if file.startswith("hrm_4400_007_20211104")]
    if len(file_list) < 20:
        print("file list error !!!!")
        exit(1)
    list =[ ]
    for file in file_list:
        data = pd.read_excel(dir_path + '\\' + file)
        data = data.rename(columns=data.iloc[2])
        data_origin = data
        data = data.drop([0, 1, 2])
        AI_member = data['부서'] == "AI센서연구센터"
        month = (data['기간'].mode().values[0][1][4:6])
        date = (data['기간'].mode().values[0][1][6:8])
        member = data[AI_member]["성명"].values
        reason = data[AI_member]['부재구분'].values
        location = data[AI_member]['출장지'].values
        if len(data_origin) > 20:
            list.append([month, date, member, reason, location])
    df = pd.DataFrame(list)
    df.columns = ["month", "date", "member", "reason", "location"]
    df = df.sort_values(by=["date"], axis=0)
    f = open("test1.csv", 'w', newline='', encoding='utf-8-sig')
    wr = csv.writer(f)
    wr.writerow(["month", "date", "member", "reason", "location"])
    for i in range(len(df)):
        for j in range(len(df.iloc[i]['member'])):
            if j == 0:
                df.iloc[i]['reason'][j] = df.iloc[i]['reason'][j].replace('\n', '')
                wr.writerow([df.iloc[i]['month'], df.iloc[i]['date'], df.iloc[i]['member'][j], df.iloc[i]['reason'][j], df.iloc[i]['location'][j]])
            else:
                df.iloc[i]['reason'][j] = df.iloc[i]['reason'][j].replace('\n', '')
                wr.writerow(['', '', df.iloc[i]['member'][j], df.iloc[i]['reason'][j], df.iloc[i]['location'][j]])
    f.close()

if __name__ == "__main__":
    CollectAbsent()