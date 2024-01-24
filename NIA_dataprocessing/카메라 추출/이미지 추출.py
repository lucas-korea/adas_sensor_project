import numpy as np
import cv2
import os

path1 = 'E:\\20231011 thermalcalibration\\20231011_112915'   #검색할 최상위 폴더 경로 작성

for(path,dir,files) in os.walk(path1): #path1의 하위 폴더들을 전부 검색
    os.chdir(path)
    file_list = os.listdir(path)
    file_list_py = [file for file in file_list if (file.startswith('1_') or file.startswith('2_') or file.startswith('3_') or file.startswith('4_'))
                    and file.endswith('.bin') and "H_Lidar" not in file] ## 파일명 끝이 .bin과 H_Lidar를 제외한 경우

    width = 1920  # 폭 높이 채널 설정
    height = 1080
    channel = 2

    for file in file_list_py:
        filepath=file
        with open(filepath, 'rb') as f:
            print("filepath: " , path+'\\'+filepath)
            total_frame = os.path.getsize(path + '\\' + file) / (width*height*channel)
            #디렉토리 내 파일 생성 후 파일 내에 png 파일 생성
            try:
                if not os.path.exists(filepath[:-4]):
                    os.makedirs(name=filepath[:-4])
            except OSError:
                    print ('Error: Creating directory. ' +  filepath[:-4])
            # 데이터 읽고 프레임 변환, 1by1
            for frame in range(int(total_frame)):
                content = f.read(width*height*channel)
                if frame % 30 == 0:
                    x = np.frombuffer(content, dtype=np.uint8)
                    im = x.reshape(height, width, 2)
                    rgb = cv2.cvtColor(im, cv2.COLOR_YUV2BGR_UYVY)   #YUV에서 RGB로
                    cv2.imshow("rgb",  rgb)
                    cv2.waitKey(1)
                    cv2.imwrite(filepath[:-4] + "/frame%d.png" % frame, rgb)
print("완료")
cv2.waitKey()
cv2.destroyAllWindows()