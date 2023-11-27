import os
import csv
import natsort

files = [file for file in os.listdir('E:\\20231108_polardata\\정제된 데이터') if file.endswith('png') or file.endswith('bmp')]

files = natsort.natsorted(files)
print(files)
f = open('E:\\20231108_polardata\\정제된 데이터\\file_list.csv', 'w')
wr = csv.writer(f)

wr.writerow(['file_name',' good image number'])
for file in files:
    wr.writerow([file])
f.close()