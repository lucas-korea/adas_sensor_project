import shutil
import os

def findNearNum(exList, values):
    answer = [0 for _ in range(2)]  # answer 리스트 0으로 초기화
    minValue = min(exList, key=lambda x: abs(x - values))
    # exList = exList.tolist()
    minIndex = exList.index(minValue)
    answer[0] = minIndex
    answer[1] = minValue
    return answer

Frame_TimeStamp_file = [file for file in os.listdir('E:\\20231011thermalcalibration\\20231011_114446') if file.startswith('Frame_TimeStamp')]
with open('E:\\20231011thermalcalibration\\20231011_114446' + '\\' +Frame_TimeStamp_file[0]) as f:
    Frame_TimeStamp_list = f.readlines()
    Frame_TimeStamps = []
    for i in Frame_TimeStamp_list:
        Frame_TimeStamps.append(int(i.split('\t')[-1].replace(' ','').replace('\n','')))
print(Frame_TimeStamps)

thermal_timestamp_file  = [file for file in os.listdir('E:\\20231011thermalcalibration\\20231011_114446') if file.startswith('thermal_timestamp')]
with open('E:\\20231011thermalcalibration\\20231011_114446' + '\\' +thermal_timestamp_file[0]) as f:
    thermal_TimeStamp_list = f.readlines()
    thermal_TimeStamps = []
    for i in thermal_TimeStamp_list:
        thermal_TimeStamps.append(int(i.split('\t')[-1].replace(' ','').replace('\n','')))
print(thermal_TimeStamps)

Frame_target_list = [file for file in os.listdir('E:\\20231011thermalcalibration\\extrinsic\\color') if file.startswith('4_20231011_114446')]

for i in Frame_target_list:
    frame_num = int(i.split('_')[-1].split('.')[0])
    print(Frame_TimeStamps[frame_num])
    shutil.copy2('E:\\20231011thermalcalibration\\20231011_114446' +'\\' + 'thermal_20231011_114446_'+
                 str(findNearNum(thermal_TimeStamps, Frame_TimeStamps[frame_num]+330)[0])+'.png'
                 ,'E:\\20231011thermalcalibration\\extrinsic\\thermal'+'\\' + 'thermal_20231011_114446_'+
                 str(findNearNum(thermal_TimeStamps, Frame_TimeStamps[frame_num]+330)[0])+'.png')
