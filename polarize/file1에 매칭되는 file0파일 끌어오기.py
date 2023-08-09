import os
import shutil


# rgb_list = [file for file in os.listdir('Y:\\PolarRealRoadDataBMP\\선별 데이터\\raw') if file in '22623682']
# polar_list = [file for file in os.listdir('Y:\\PolarRealRoadDataBMP\\선별 데이터\\raw') if file in '21159646']

root_list = os.listdir('Y:\\PolarRealRoadDataBMP\\NIA 편광 샘플 데이터 어노테이션용\\RGB이미지')
print(root_list)

for file in root_list:
    start = '_'.join(file.split('_')[0:2])
    end = file.split('_')[-1].split('.')[0]
    print(start, end)
    print(file)
    target_file = [file for file in os.listdir('Y:\\PolarRealRoadDataBMP\\selected data\\DOLP_polar') if file.startswith(start) and file.endswith(end+'_DOLP.bmp') ][0]
    print(target_file)
    shutil.copy2("Y:\\PolarRealRoadDataBMP\\selected data\\DOLP_polar\\" + target_file,"Y:\\PolarRealRoadDataBMP\\NIA 편광 샘플 데이터 어노테이션용\\편광이미지 DOLP")