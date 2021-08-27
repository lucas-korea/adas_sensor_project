import os
import shutil

path_dir = "E:\\20210826_005023\\20210826_005023\\PCDPNGfiles_matched"
move_dir = "E:\\20210826_005023\\20210826_005023\\PCDPNGfiles"
file_list = [file for file in os.listdir(path_dir) if file.endswith(".png")]
print(len(file_list))
png_i = 0
for file_name in file_list:
    if png_i % 10 == 5 or png_i % 10 == 0 or 1:
        print(png_i)
        shutil.move(path_dir + '\\' + file_name, move_dir + '\\' + file_name)
    png_i = png_i + 1