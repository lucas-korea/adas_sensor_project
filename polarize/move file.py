import os

import shutil

file_list = os.listdir("W:\\PolarRealRoadDataBMP\\extra\\polar factor")
AOLP_list = [file for file in file_list if file.endswith('_AOLP.bmp')]
for file in AOLP_list:
    print(file)
    shutil.copy2("W:\\PolarRealRoadDataBMP\\extra\\polar factor" + '\\' + file,
                "W:\\PolarRealRoadDataBMP\\extra\\AOLP\\" + file)
DOLP_list = [file for file in file_list if file.endswith('_DOLP.bmp')]
for file in DOLP_list:
    shutil.copy2("W:\\PolarRealRoadDataBMP\\extra\\polar factor" + '\\' + file,
                "W:\\PolarRealRoadDataBMP\\extra\\DOLP\\" + file)
AOLPDOLP_list = [file for file in file_list if file.endswith('DOLPplusAOLP.bmp')]
for file in AOLPDOLP_list:
    shutil.copy2("W:\\PolarRealRoadDataBMP\\extra\\polar factor" + '\\' + file,
                "W:\\PolarRealRoadDataBMP\\extra\\DOLP+AOLP\\"+ file)
glare_reduction_list = [file for file in file_list if file.endswith('Glare_reduction.bmp')]
for file in glare_reduction_list:
    shutil.copy2("W:\\PolarRealRoadDataBMP\\extra\\polar factor" + '\\' + file,
                "W:\\PolarRealRoadDataBMP\\extra\\glare reduction\\"+ file)

