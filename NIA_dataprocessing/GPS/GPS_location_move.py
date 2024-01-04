import os
import gmplot
import csv

root_path  = 'C:\\Users\\jcy37\\Downloads\\230918_GPS_img_F'
folders = [file for file in os.listdir(root_path) if file.endswith('_K')]

for i in range(len(folders)):
    i = 0
    print(folders[i])
    path = root_path + '\\' + folders[i] + '\\GPS'
    files = [file for file in os.listdir(path) if file.endswith('csv')]
    latitude_list = []
    longitude_list = []
    for file in files:
        with open(path + '\\' + file, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                latitude_list.append(float(row[1]))
                longitude_list.append(float(row[2]))
    for j in range(len(latitude_list)):
        latitude_list[j]  += -0.000# up
        longitude_list[j] += -0.000 # right
    gmap4 = gmplot.GoogleMapPlotter(latitude_list[0],longitude_list[0], zoom=18, apikey='AIzaSyAqrO_DZ2Dfx8VGhKLQ4uHVA7wVtTSVazg')
    # heatmap plot heating Type
    # points on the Google map
    gmap4.heatmap(latitude_list[0:1], longitude_list[0:1], radius=15, opacity=1)
    gmap4.heatmap(latitude_list[1:], longitude_list[1:],radius=5, )
    # Pass the absolute path
    gmap4.draw(path + '\\' + files[0].split('.')[0] + '_new.html')
    exit(1)
# for i in range(len(files)):
#     i = 23
#     print(files[i])
#     f = open(path + '\\' + files[i], "r")
#     reader = csv.reader(f)
#     latitude_list = []
#     longitude_list = []
#     for row in reader:
#         # print(row)
#         latitude_list.append(float(row[0]))
#         longitude_list.append(float(row[1]))
#
#     # print(latitude_list)
#     # print(longitude_list)
#     for j in range(len(latitude_list)):
#         latitude_list[j] +=  0.00033  # up
#         longitude_list[j] += 0.00150 # right
#     gmap4 = gmplot.GoogleMapPlotter(latitude_list[0],longitude_list[0], zoom=18, apikey='AIzaSyAqrO_DZ2Dfx8VGhKLQ4uHVA7wVtTSVazg')
#     # heatmap plot heating Type
#     # points on the Google map
#     gmap4.heatmap(latitude_list[0:1], longitude_list[0:1], radius=15, opacity=1)
#     gmap4.heatmap(latitude_list[1:], longitude_list[1:],radius=5, )
#     # Pass the absolute path
#     gmap4.draw('C:\\Users\\jcy37\\Documents\\카카오톡 받은 파일\\gps_bin_gather\\230823_map\\' + files[i].split('.')[0] + '_new.html')
#     exit(1)