import os
import pandas as pd
import shutil
path  = "E:\\polar_acquisition_data"
if __name__ == '__main__':
    file_21159646_list = [file for file in os.listdir(path) if file[9 : 24]=="192350_21159646" and file.endswith('jpg')]
    file_22623682_list = [file for file in os.listdir(path) if file[9 : 24]=="192350_22623682" and file.endswith('jpg')]
    csv_list = [file for file in os.listdir(path) if
                          file[17: 23] == "192350" and file.endswith('origin.csv')]
    # for file in file_21159646_list:
    #     os.rename(path+ '\\' + file, path+ '\\' + '_'.join(file.split('_')[0:-1]) + '_' + str('{:06d}'.format(int(file.split('_')[-1].split('.')[0]))) + '.jpg')
    #     print(file)
    # for file in file_22623682_list:
    #     os.rename(path+ '\\' + file, path+ '\\' + "20230329_192350_22623682_" + '{:06d}'.format(int(file.split('_')[-2])) + '.jpg')
    #     print("20230329_192350_22623682_" + '{:06d}'.format(int(file.split('_')[-2])) + '.jpg')

    # for file in file_21159646_list:
    #     os.rename(path+ '\\' + file, path+ '\\' + "20230329_192350_21159646_" + '{:06d}'.format(int(file.split('_')[-2])) + '.jpg')
    #     print("20230329_192350_21159646_" + '{:06d}'.format(int(file.split('_')[-2])) + '.jpg')


    data = pd.read_csv(path + '\\' + csv_list[0])
    data.reset_index(inplace=True)
    data['gap'] = -1
    for i in range(len(data)-1):
        data.loc[i, 'gap'] = (data.loc[i+1]['SystemTimeInNanoseconds'] - data.loc[i]['SystemTimeInNanoseconds']) / 1000000000

    # print(data[data["SerialNumber"] == 22623682].reset_index(drop=True))
    # print(data[data["SerialNumber"] == 21159646].reset_index(drop=True))
    # data_index=data.reset_index(inplace=True)
    # print(data_index[data["SerialNumber"] == 22623682])

    df_21159646 = data[data["SerialNumber"] == 21159646].reset_index(drop=True).drop(columns='FrameID')
    df_22623682 = data[data["SerialNumber"] == 22623682].reset_index(drop=True).drop(columns='FrameID')

    match_cnt = 0
    YMD_HMS = '20230329_192350'
    for i in range(1, len(df_21159646)):
        if 0.02 < float(df_21159646.loc[i,'gap']) < 0.04:
            match_index = df_21159646.loc[i,'index']
            if(df_22623682[df_22623682['index'] == match_index-3]['gap'].values[0] < 0.01):
                match_index_21159646 = df_21159646[df_21159646['index'] == match_index].index.values[0]
                match_index_22623682 = df_22623682[df_22623682['index'] == match_index - 3].index.values[0]
                shutil.copy2(path + '\\' + YMD_HMS + '_21159646_' + '{:06d}'.format(match_index_21159646) + '.jpg',
                             path + '\\match\\' + YMD_HMS + '_21159646_' + '{:06d}'.format(match_cnt) + '.jpg')
                shutil.copy2(path + '\\' + YMD_HMS + '_22623682_' + '{:06d}'.format(match_index_22623682) + '.jpg',
                             path + '\\match\\' + YMD_HMS + '_22623682_' + '{:06d}'.format(match_cnt) + '.jpg')
                match_cnt += 1
        print(i)