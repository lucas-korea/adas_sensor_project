import os
import random
import shutil

path = "G:\\정제완료5799장_전방"

os.mkdir("G:\\정제완료5799장_전방\\성미애")
os.mkdir("G:\\정제완료5799장_전방\\성선영")
os.mkdir("G:\\정제완료5799장_전방\\신성례")
os.mkdir("G:\\정제완료5799장_전방\\노수진")
os.mkdir("G:\\정제완료5799장_전방\\오연주")
os.mkdir("G:\\정제완료5799장_전방\\노화중")
os.mkdir("G:\\정제완료5799장_전방\\박윤미")
os.mkdir("G:\\정제완료5799장_전방\\정성미")
os.mkdir("G:\\정제완료5799장_전방\\이민희")
os.mkdir("G:\\정제완료5799장_전방\\김민서")
os.mkdir("G:\\정제완료5799장_전방\\심혜림")
os.mkdir("G:\\정제완료5799장_전방\\서경옥")
os.mkdir("G:\\정제완료5799장_전방\\노은영")
os.mkdir("G:\\정제완료5799장_전방\\권미애")


list = [_ for _ in os.listdir(path) if _.endswith('.jpg')]
random.shuffle(list)
print(list)
print(len(list))

작업자명단 = ['성미애','성선영','신성례','노수진','오연주','노화중','박윤미','정성미','이민희','김민서','심혜림','서경옥','노은영','권미애']
for i in range(len(list)):
    print(path + '\\' + str(list[i]))
    print(path + '\\' + 작업자명단[i % len(작업자명단)])
    shutil.copy2(path + '\\' + str(list[i]), path + '\\' + 작업자명단[i % len(작업자명단)])
