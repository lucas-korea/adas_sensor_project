import os, glob

path = "D:\\GT 생성 업무\\정제성성 완료 파일 모음"
path_ = path + "\\"
folder_name = "정제생성 완료 파일 모음"
def main():
    List = os.listdir(path)
    with open(path_ + "test.txt", 'w') as f:
        for i in List:
            if os.path.isdir(path_ + i):
                f.write('.\\' + folder_name + '\\' + i + ' ' + i[:3] + '\n')
if __name__ == "__main__":
    for (path, dir, files) in os.walk(path):
        if len(dir) == 2:
            if dir[1][-4:] == 'v001':
                print(dir)
                os.rename(path + '\\' + dir[0], path + '\\1')
                os.rename(path + '\\' + dir[1], path + '\\1_annotations_v001')