import os, glob

PATH = "D:\\GT 생성 업무\\객체생성-검수\\생성완"
path_ = PATH + "\\"
folder_name = "생성완"
def make_txt_for_objectCounting():
    List = os.listdir(PATH)
    with open("D:\\GT 생성 업무\\객체생성-검수\\" + "test.txt", 'w') as f:
        for i in List:
            if os.path.isdir(path_ + i):
                f.write('.\\' + folder_name + '\\' + i + ' ' + i[:3] + '\n')

def rename_images_xml_folder():
    for (path, dir, files) in os.walk(PATH):
        if len(dir) == 2:
            if dir[1][-4:] == 'v001':
                print(dir)
                os.rename(path + '\\' + dir[0], path + '\\1')
                os.rename(path + '\\' + dir[1], path + '\\1_annotations_v001')
    print("====================================================================")
    for (path, dir, files) in os.walk(PATH):
        if len(dir) == 2:
            if dir[1][-4:] == 'v001':
                print(dir)

if __name__ == "__main__":
    rename_images_xml_folder()