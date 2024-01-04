import os
import shutil

frontList = ['20220217_143317', '20220217_143346','20220217_143429']
matchList = ['20220217_143317_match_list.txt','20220217_143346_match_list.txt','20220217_143429_match_list.txt']
sideList = ['143318', '143347','143430']
frontPATH = 'D:\\NIA4차 대비 실도로 주행 sample PNGPCD 3case'
sidePATH = 'E:\\NIA4_saple_220217_f,s\\side\\sideimg'

for i in range(3):
    imgList = []

    with open(frontPATH + '\\' + matchList[i], 'r') as f:
        while(1):
            try:
                imgList.append(int(f.readline().split('\t')[1]))
            except:
                break
    sideFileList = [file for file in os.listdir(sidePATH) if file.endswith('jpg') and file.split('_')[2] == sideList[i]]
    cnt = 0
    for imgNum in imgList:
        target = [file for file in sideFileList if file.split('_')[2] == sideList[i] and int(file.split('_')[3].split('.')[0]) == imgNum]
        print(target)
        for abcd in target:
            print(abcd)
            print(frontList[i] +'_' + str(cnt) + '_' + str(int(abcd[0])+3) + '.jpg')
            shutil.copy2(sidePATH + '\\' + abcd , frontPATH + '\\' + frontList[i] +'_' + '{0:06d}'.format(cnt) + '_' + str(int(abcd[0])+3) + '.jpg')
        cnt += 1
