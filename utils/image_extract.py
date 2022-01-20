import cv2
import os
import shutil

def GetImgFromVideo():
    # 영상의 의미지를 연속적으로 캡쳐할 수 있게 하는 class
    path_dir = 'D:\\H2BUS_3차년도_DB_정제중(20211018)\\20210205_수소버스_도로주행영상(전후좌우)\\1번_전방'
    count = 0
    file_list = os.listdir(path_dir)
    print(file_list)
    for file in file_list:
        print(file)
        vidcap = cv2.VideoCapture(path_dir + '\\' + file)
        count = 0
        while (vidcap.isOpened()):
            ret, image = vidcap.read()
            # 캡쳐된 이미지를 저장하는 함수
            if (count % 30 == 0):
                try:
                    cv2.imwrite("D:\\20210205_1th_image\\" + file[:-4] + "%d.jpg" % count, image)
                    print('Saved frame%d.jpg' % count)
                except Exception as e:
                    print(e)
                    print("D:\\20210205_1th_image\\" + file[:-4] + "%d.jpg")
                    break
            count += 1
        vidcap.release()
    print("finish")

def GetImgFromImgs():
    Root = "G:\\211018~19 세종 버스실험"
    Dirs = []
    for item in os.listdir(Root):
        if os.path.isdir(Root + '\\' + item):
            Dirs.append(item)

    for Dir in Dirs:
        for path, dirs, files in os.walk(Root + '\\' + Dir):
            if path.split('\\')[-2] in Dirs:
                try:
                    os.mkdir(Root + '\\' + Dir + '_sampling')
                    os.mkdir(Root + '\\' + Dir + '_sampling' + '\\' + path.split('\\')[-1])
                    for i in range(len(files)):
                        if i % 30 == 0:
                            shutil.copy2(path + '\\' + files[i], Root + '\\' + Dir + '_sampling' + '\\' + path.split('\\')[-1] + '\\' + files[i])
                except:
                    os.mkdir(Root + '\\' + Dir + '_sampling' + '\\' + path.split('\\')[-1])
                    for i in range(len(files)):
                        if i % 30 == 0:
                            shutil.copy2(path + '\\' + files[i], Root + '\\' + Dir + '_sampling' + '\\' + path.split('\\')[-1] + '\\' + files[i])

def getimg30():
    PATH = "Z:\\side_cam_night\\20220114_132018\\5"
    cnt = 0
    for file in os.listdir(PATH):
        if cnt % 3 == 0:
            shutil.move(PATH + '\\' + file, 'Z:\\side_cam_night\\20220114_132018\\5_sampling\\' + file)
        cnt = cnt + 1

if __name__ == "__main__":
    getimg30()
