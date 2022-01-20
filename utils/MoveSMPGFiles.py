import os
import shutil

if __name__ == '__main__':

    PATH = "F:\\H2BUS_3차년도_DB\\20210607_에이아이매틱스_영상DB\\210524_수소버스_천안_SMPG\\210524_Front\\210524_SMPG"
    srcPATH = "D:\\GT 생성 업무\\객체생성-검수\\정제완료4002장_2차"
    dstPATH = "D:\\GT 생성 업무\\객체생성-검수\\정제완료_SMPG데이터만"
    fileList = []
    for path, dirs, files in os.walk(PATH):
        print(path)
        if path.split('\\')[-2] == "210524_SMPG":
            for i in range(len(files)):
                fileList.append(files[i])
    print(fileList)
    print(len(fileList))
    cnt = 0
    for file in os.listdir(srcPATH):
        if file in fileList:
            cnt = cnt + 1
            print(file)
            shutil.move(srcPATH + '\\' + file, dstPATH + '\\' + file)
    print(cnt)