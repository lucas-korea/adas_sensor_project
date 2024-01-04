import os
import csv
list = [file for file in os.listdir('C:\\Users\\jcy37\\Downloads\\230918_GPS_img_F') if file.endswith('_K')]
print(list)
#
new_CSV = open('C:\\Users\\jcy37\\Downloads\\230918_GPS_img_F\\offset_list.csv','w', encoding='utf-8', newline='')
wr = csv.writer(new_CSV)
for case in list:
    wr.writerow([case])
new_CSV.close()