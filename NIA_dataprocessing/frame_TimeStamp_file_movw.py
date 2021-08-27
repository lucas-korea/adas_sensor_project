import os
import shutil

def search(dirname):
    file_path_list = []
    for (path, dir, files) in os.walk(dirname):
        file_path_list.append([path + '\\' + file for file in files if file.startswith("Frame_TimeStamp_")])
    return [v for v in file_path_list if v]

search_result = search("D:\\210828_testdata_sw5\\short")
print(search_result)
print(len(search_result))
# search_result = []
for i in range(len(search_result)):
    print(search_result[i][0])
    shutil.copy2(search_result[i][0], "D:\\210828_testdata_sw5")
# sample_list = [v for v in search("D:\\210828_testdata_sw5\\short") if v]
# print(sample_list)
# print(len(sample_list))