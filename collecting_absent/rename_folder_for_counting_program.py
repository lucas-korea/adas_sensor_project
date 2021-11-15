import os, glob

PATH = "D:\\GT 생성 업무\\정제생"
path_ = PATH + "\\"
folder_name = "정제생"
def main():
    List = os.listdir(PATH)
    with open("D:\\GT 생성 업무\\" + "test.txt", 'w') as f:
        for i in List:
            if os.path.isdir(path_ + i):
                f.write('.\\' + folder_name + '\\' + i + ' ' + i[:3] + '\n')

def main2():
    for (path, dir, files) in os.walk(PATH):
        if len(dir) == 2:
            if dir[1][-4:] == 'v001':
                print(dir)
                os.rename(path + '\\' + dir[0], path + '\\1')
                os.rename(path + '\\' + dir[1], path + '\\1_annotations_v001')

if __name__ == "__main__":
    main()