import numpy as np
import cv2
import os
from tkinter import filedialog
from tkinter import messagebox
import time

def select_file_list():
    files = filedialog.askopenfilenames(initialdir=os.getcwd(),
                                        title="파일을 선택 해 주세요",
                                        filetypes=(("*.txt", "*txt"), ("*.xls", "*xls"), ("*.csv", "*csv")))
    if files == '':
        messagebox.showwarning("경고", "파일을 추가 하세요")  # 파일 선택 안했을 때 메세지 출력
        exit(1)
    file_list_dir_path = ("\\".join(list(files)[0].split("/")[0: -1]))  # lidar 데이터 목록 위치 추출
    return files, file_list_dir_path

def main():
    files, file_list_dir_path = select_file_list()
    print(file_list_dir_path, '\n', files[0])
    with open(list(files)[0], 'r', encoding='utf8') as thermal_f:
        print(list(files)[0])
        thermal_file_list = thermal_f.readlines()
    time1 = time.time()
    file_num = 0
    for file_name in thermal_file_list:
        file_name = file_name.replace("\n", "")
        print("now converting : ", file_name)
        total_frame = os.path.getsize(file_name)/(480 * 640 * 4)

        with open(file_name, "rb") as f:
            frame = 0
            while(1):
                try:
                    print(file_num + 1, '/', len(thermal_file_list), '\t', frame, "/", total_frame, "frame\t",
                          format((total_frame - frame) * (time.time() - time1) / 60, '.2f'), "min left",
                          "   now converting : ", file_name)
                    data = f.read(480 * 640 * 4) # 한 프레임의 크기(바이트) 만큼 읽기
                    if frame % 10 == 0:
                        image = np.zeros((480, 640), dtype=np.uint8) # 추출한 파일의 형태 잡기
                        cnt = 0
                        for col in range(480):
                            for row in range(640):
                                image[col, row] = data[cnt*4] #픽셀by픽셀 데이터 집어넣기
                                cnt +=1
                        cv2.imwrite('\\'.join(file_name.split('\\')[:-1]) + '\\' + file_name.split('\\')[-1].split('.')[0]
                                    + '_' + str(frame) + '.png' , image)
                    frame += 1
                except Exception as e:
                    print("error : ", e)
                    print("file finish")
                    break
        file_num = file_num + 1

if __name__ == '__main__':
    main()