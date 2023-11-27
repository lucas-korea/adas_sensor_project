import os
import gmplot
import csv
# '케이스별 ofest.xlsx' 파일을 읽어 각 케이스별 offest을 get
# yymmdd_hhmmss_K/gps 폴더안에 있는 csv 파일을 읽어, 위경도 값이 offset을 더하여 yymmdd_hhmmss_K/gps_new 폴더에 파일 생성
# yymmdd_hhmmss.html, yymmdd_hhmmss_new.html 각각 생성하여 비교검증

LAST_editing = 1
if LAST_editing:
    f = open('F:\\230918_GPS_img_F\\offset_list.csv', "r", encoding='utf-8-sig')
    reader = csv.reader(f)
    offest_list = []
    for row in reader:
        offest_list.append(row) #[yymmdd_hhmmdd_K, lat_offset, long_offset]
    # offest_list = offest_list[0:]
    case_path = 'F:\\230918_GPS_img_F'
    folders = [file for file in os.listdir(case_path) if file.endswith('_K')]
    # print('floers:', folders)
    cnt = 0
    original_row = []
    for folder in folders:
        print('folder:', folder)
        gps_csv_files = [file for file in os.listdir(case_path + '\\' + folder + '\\gps') if file.endswith('csv')]
        os.makedirs(case_path + '\\'  + folder + '\\gps_new', exist_ok=True)
        # print('gps_csv_files : ', gps_csv_files)
        latitude_new_list = []
        longitude_new_list = []
        latitude_old_list = []
        longitude_old_list = []
        if offest_list[cnt][0] == folder and not offest_list[cnt][1] == '불용':
            lat_offset = offest_list[cnt][1] # up
            lon_offset = offest_list[cnt][2] # right
        elif offest_list[cnt][1] == '불용':
            print(offest_list[cnt][0], "불용")
            cnt += 1
            continue
        else:
            print(offest_list[cnt][0], offest_list[cnt][1], offest_list[cnt][2])
            print("error!!!!!")
            break
        #기존 gps 파일에서 데이터 추출 및 offset을 더한다
        for csv_file in gps_csv_files:
            f = open(case_path + '\\' + folder + '\\gps\\' + csv_file, "r")
            reader = csv.reader(f)
            for row in reader:
                original_row.append(row)
                latitude_new_list.append(float(row[1]) + float(lat_offset))
                longitude_new_list.append(float(row[2]) + float(lon_offset))
                latitude_old_list.append(float(row[1]))
                longitude_old_list.append(float(row[2]))

        #gps_new 에 csv 만들기
        for new_i in range(len(gps_csv_files)):
            new_CSV = open(case_path + '\\' + folder + '\\gps_new\\' + '_'.join(gps_csv_files[new_i].split('_')[0:3]) +'_{0:03d}'.format(new_i+1)  + '.csv',
                       'w', encoding='utf-8', newline='')
            wr = csv.writer(new_CSV)
            wr.writerow([original_row[cnt][0], latitude_new_list[new_i], longitude_new_list[new_i], original_row[cnt][3], original_row[cnt][4], original_row[cnt][5], original_row[cnt][6], original_row[cnt][7]])
            new_CSV.close()

        #지도그리기
        gmap_new = gmplot.GoogleMapPlotter(latitude_new_list[0], longitude_new_list[0], zoom=18, apikey='AIzaSyAqrO_DZ2Dfx8VGhKLQ4uHVA7wVtTSVazg')
        gmap_new.heatmap(latitude_new_list[0:1], longitude_new_list[0:1], radius=15, opacity=1)
        gmap_new.heatmap(latitude_new_list[1:], longitude_new_list[1:], radius=5, )
        gmap_new.draw(case_path + '\\' + folder +'\\' + '_'.join(folder.split('_')[0:2]) + '_new.html')

        gmap_old = gmplot.GoogleMapPlotter(latitude_old_list[0], longitude_old_list[0], zoom=18,apikey='AIzaSyAqrO_DZ2Dfx8VGhKLQ4uHVA7wVtTSVazg')
        gmap_old.heatmap(latitude_old_list[0:1], longitude_old_list[0:1], radius=15, opacity=1)
        gmap_old.heatmap(latitude_old_list[1:], longitude_old_list[1:], radius=5, )
        gmap_old.draw(case_path + '\\' + folder + '\\' + '_'.join(folder.split('_')[0:2]) + '_old.html')
        f.close()
        cnt += 1

else:
    #################################################작업용##############################################################################
    folders = os.listdir('F:\\230823 GPS 수정')
    print('floers:', folders)
    for folder in folders:
        folder ='230823_185542_K'
        gps_csv_files = os.listdir('F:\\230823 GPS 수정\\' + folder + '\\gps_new')
        # os.makedirs('F:\\230823 GPS 수정\\' + folder + '\\gps_new', exist_ok=True)
        print('gps_csv_files : ', gps_csv_files)
        latitude_list = []
        longitude_list = []
        lat_offset = 0.00000 # up
        lon_offset = 0.00000 # right
        for csv_file in gps_csv_files:
            f = open('F:\\230823 GPS 수정\\' + folder + '\\gps_new\\' + csv_file, "r")
            reader = csv.reader(f)
            for row in reader:
                latitude_list.append(float(row[1]) + lat_offset)
                longitude_list.append(float(row[2]) + lon_offset)
        print(latitude_list, longitude_list)
        gmap = gmplot.GoogleMapPlotter(latitude_list[0],longitude_list[0], zoom=18, apikey='AIzaSyAqrO_DZ2Dfx8VGhKLQ4uHVA7wVtTSVazg')
        # heatmap plot heating Type
        # points on the Google map
        gmap.heatmap(latitude_list[0:1], longitude_list[0:1], radius=15, opacity=1)
        gmap.heatmap(latitude_list[1:], longitude_list[1:],radius=5, )
        # Pass the absolute path
        gmap.draw('F:\\230823 GPS 수정\\' + folder +'\\' + '_'.join(folder.split('_')[0:2]) + '_new.html')
        exit(1)