import os, shutil

def RemoveNoAnnotationImgfile():
    pass

def dd():
    file = 1
    Image= 1
    path = 1
    if file.split('.')[1] == 'png':
        im = Image.open(path + '\\' + file).convert('RGB')
        im.save(path + '\\' + file.split('.')[0] + '.jpg', 'jpeg')

def GetAnnotationFile():
    PATH = 'F:\\H2bus 인식율평가 데이터셋'
    ImgPathStruct = [[],[]]
    for path, dirs, files in os.walk(PATH):
        if len(files) > 10 and files[0].split('.')[-1] == 'jpg':
            os.makedirs(path + '_annotations_v001_1', exist_ok=True)
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
                    shutil.copy2(path + '\\' + file , ImgPathStruct[1][ImgPathStruct[0].index(file_name)] + '_annotations_v001_1' + '\\' + file)
                    del ImgPathStruct[1][ImgPathStruct[0].index(file_name)]
                    del ImgPathStruct[0][ImgPathStruct[0].index(file_name)]

if __name__ == "__main__":
    GetAnnotationFile()