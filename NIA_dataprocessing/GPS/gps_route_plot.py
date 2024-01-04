import os
import gmplot
import csv

files = os.listdir('F:\\20230828_gps_test\\csv')
for i in range(len(files)):
    f = open('F:\\20230828_gps_test\\csv\\' + files[i], "r")
    reader = csv.reader(f)
    latitude_list = []
    longitude_list = []
    for row in reader:
        # print(row)
        latitude_list.append(float(row[0]))
        longitude_list.append(float(row[1]))

    # print(latitude_list)
    # print(longitude_list)

    gmap4 = gmplot.GoogleMapPlotter(latitude_list[0],longitude_list[0], zoom=15, apikey='AIzaSyAqrO_DZ2Dfx8VGhKLQ4uHVA7wVtTSVazg')
    # heatmap plot heating Type
    # points on the Google map
    gmap4.heatmap(latitude_list[0:1], longitude_list[0:1], radius=15, opacity=1)
    gmap4.heatmap(latitude_list[1:], longitude_list[1:],radius=5, )
    # Pass the absolute path
    gmap4.draw('F:\\20230828_gps_test\\html\\' + files[i].split('.')[0] + '.html')