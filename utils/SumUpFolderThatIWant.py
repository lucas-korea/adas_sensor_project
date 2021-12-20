import os
import shutil

LIST = ['윤가영1112','노수진1112','배은이1112','정성미1112','박윤미1116','정다운1118','배은이1118',"강인선1118"
    ,"권미애1122","박윤미1122","윤가영1122","이민희1122","노수진1129","권미애1129","박윤미1129","윤가영1129","정다운1130",
        "강인선1130","권미애1206","성미애1207","정다운1207","윤가영1207","박윤미1209","노수진1209","윤가영1210",
        "박윤미1210","성미애1210"]
# LIST = ["정다운1025","성선영1026",'윤가영1026']
# PATH = "D:\\GT 생성 업무\\객체생성-검수\\생성완"
PATH = "D:\\GT 생성 업무\\객체생성-검수\\검수완"
print(len(LIST))
cnt = 0
for (path, dir, files) in os.walk(PATH):
    if path.split('\\')[-1] == '와토시스':
        continue
    for dir_ in dir:
        if dir_ in LIST:
            LIST.remove(dir_)
            for (path2, dir2, files2) in os.walk(path + '\\' + dir_):
                # if len(path2.split('\\')[-1]) == 1:
                if path2.split('\\')[-1][-6:] == 'v001_1':
                    print(path2)
                    cnt = cnt + 1
                    for i in os.listdir(path2):
                        shutil.copy2(path2 + '\\' + i, 'D:\\GT 생성 업무\\객체생성-검수\\컨테스트_학습용_주간_xml')
                    print(len(os.listdir(path2)), 'th images moved')
                    print(len(os.listdir("D:\\GT 생성 업무\\객체생성-검수\\컨테스트_학습용_주간_xml")), "th images")
print(cnt)
print(LIST)