import pandas as pd
import os

def collecting_absent():
    dir_path = "C:\\Users\\jcy37\\Downloads"
    file_list = os.listdir(dir_path)
    file_list = [file for file in file_list if file.startswith("hrm_4400_007_20211207")]
    list =[ ]
    for file in file_list:
        data = pd.read_excel(dir_path + '\\' + file)
        data = data.rename(columns=data.iloc[2])
        data_origin = data
        data = data.drop([0, 1, 2])
        # print(data['기간'].mode().values[0][1][4:6], "월",
        #       data['기간'].mode().values[0][1][6:8], "일", end="")
        AI_member = data['부서'] == "AI센서연구센터"
        month = (data['기간'].mode().values[0][1][4:6])
        date = (data['기간'].mode().values[0][1][6:8])
        member = data[AI_member]["성명"].values
        reason = data[AI_member]['부재구분'].values
        location = data[AI_member]['출장지'].values
        if len(data_origin) > 20:
            list.append([month, date, member, reason, location])
    list = pd.DataFrame(list)
    list.columns = ["month", "date", "member", "reason", "location"]
    list = list.sort_values(by=["date"], axis=0)
    # print (sorted(list, key=lambda time: time[0]))
    print(list)
    list.to_excel("부재자현황.xlsx")
    new_data = pd.DataFrame

if __name__ == "__main__":
    collecting_absent()