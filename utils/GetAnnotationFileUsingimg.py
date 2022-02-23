import os, shutil
from PIL import Image

def RemoveNoAnnotationImgfile():
    pass

def ConvertJpgPng():
    frontPATH = 'D:\\NIA4차 대비 실도로 주행 sample PNGPCD 3case'
    frontFileList = [file for file in os.listdir(frontPATH) if file.endswith('png')]
    for file in frontFileList:
        if file.split('.')[1] == 'png':
            im = Image.open(frontPATH + '\\' + file).convert('RGB')
            im.save(frontPATH + '\\' + file.split('.')[0] + '_2.jpg', 'jpeg')

def GetAnnotationFile():
    PATH = 'F:\\heptacam 인식율평가 데이터셋'
    ImgPathStruct = [[],[]]
    for path, dirs, files in os.walk(PATH):
        if len(files) > 10 and (files[0].split('.')[-1] == 'jpg' or files[0].split('.')[-1] == 'png'):
            os.makedirs(path + '_annotations_v001', exist_ok=True)
            for file in files:
                ImgPathStruct[0].append(file.split('.')[0])
                ImgPathStruct[1].append(path)
    print(len(ImgPathStruct[0]))
    for path, dirs, files in os.walk('D:\\GT 생성 업무\\객체생성-검수\\검수완'):
        if path.split('\\')[-1][-6:] == 'v001_1':
            print(path)
            for file in files:
                file_name = '_'.join(file.split('_')[:-2])
                if file_name in ImgPathStruct[0]:
                    if os.path.isfile(ImgPathStruct[1][ImgPathStruct[0].index(file_name)] + '_annotations_v001' + '\\' + file[:-6] + '.xml'):
                        print('file already!!!',ImgPathStruct[1][ImgPathStruct[0].index(file_name)] + '_annotations_v001' + '\\' + file[:-6] + '.xml' )
                    shutil.copy2(path + '\\' + file , ImgPathStruct[1][ImgPathStruct[0].index(file_name)] + '_annotations_v001' + '\\' + file[:-6] + '.xml')
                    del ImgPathStruct[1][ImgPathStruct[0].index(file_name)]
                    del ImgPathStruct[0][ImgPathStruct[0].index(file_name)]


def RenameXml():
    PATH = 'F:\\H2bus 인식율평가 데이터셋'
    for path, dirs, files in os.walk(PATH):
        if len(files) > 10 and files[0].split('.')[-1] == 'xml':
            for file in files:
                os.rename(path + '\\' +file , path + '\\' +file[:-6] + '.xml')
def RenameImgXmlinCase():
    PATH = "D:\\GT 생성 업무\\객체생성-검수\\검수완\\1\\배은이0120"
    for path, dirs, files in os.walk(PATH):
        if len(files) > 10 and (files[0].split('.')[-1] == 'xml' or files[0].split('.')[-1] == 'jpg' or files[0].split('.')[-1] == 'png'):
            for file in files:
                os.rename(path + '\\' + file, path + '\\' + 'bee0120_' + file)

def RemoveNoAnnotation():
    PATH = 'F:\\heptacam 인식율평가 데이터셋'
    cnt = 0
    exception = ["F:\\H2bus 인식율평가 데이터셋\\자전로\\주간\\자전로주간측방\\버스_주간_자전로_측방_정제후_320", "F:\\H2bus 인식율평가 데이터셋\\자전로\\야간\\자전로야간측방\\버스_야간_자전로_측방_정제후_200"]
    for path, dirs, files in os.walk(PATH):
        if path in exception:
            pass
        elif len(files) > 10 and (files[0].split('.')[-1] == 'jpg' or files[0].split('.')[-1] == 'png'):
            for file in files:
                if not os.path.isfile('\\'.join(path.split('\\')[:-1])+'\\'+path.split('\\')[-1]+'_annotations_v001' + '\\' + file[:-4] + '_v001.xml'):
                    cnt += 1
                    shutil.move(path + '\\' + file, "F:\\heptacam 인식율평가 데이터셋_휴지통\\" + file)
    print(cnt)

def GetNmae():
    PATH = 'F:\\H2bus 인식율평가 데이터셋'
    FileList = []
    for path, dirs, files in os.walk(PATH):
        if len(files) > 10 and files[0].split('.')[-1] == 'jpg':
            for file in files:
                if file in FileList:
                    print(path,'\\', file)
                else: FileList.append(file)
    print(len(FileList))

if __name__ == "__main__":
    ConvertJpgPng()