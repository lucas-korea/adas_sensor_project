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

def rename_images_xml_create_folder():
    PATH = "D:\\GT 생성 업무\\객체생성-검수\\생성완"
    for (path, dir, files) in os.walk(PATH):
        if len(dir) == 2:
            if dir[1][-4:] == 'v001':
                # print(dir)
                # print(path)
                print(os.listdir(path + "\\" + dir[0])[0][0:2])
                cam_num = os.listdir(path + "\\" + dir[0])[0][0]
                if os.listdir(path + "\\" + dir[0])[0][1] == '_':
                    os.rename(path + '\\' + dir[0], path + '\\' + cam_num)
                    os.rename(path + '\\' + dir[1], path + '\\' + cam_num + '_annotations_v001')
                else:
                    os.rename(path + '\\' + dir[0], path + '\\4')
                    os.rename(path + '\\' + dir[1], path + '\\4_annotations_v001')
    print("====================================================================")
    for (path, dir, files) in os.walk(PATH):
        if len(dir) == 2:
            if dir[1][-4:] == 'v001':
                pass
                # print(dir)

def rename_images_xml_modify_folder():
    PATH = "D:\\GT 생성 업무\\객체생성-검수\\검수완"
    for (path, dir, files) in os.walk(PATH):
        if len(dir) == 3:
            if dir[1][-4:] == 'v001':
                print(dir)
                print(path)
                print(os.listdir(path + "\\" + dir[0])[0][0:2])
                cam_num = os.listdir(path + "\\" + dir[0])[0][0]
                if os.listdir(path + "\\" + dir[0])[0][1] == '_':
                    os.rename(path + '\\' + dir[0], path + '\\' + cam_num)
                    os.rename(path + '\\' + dir[1], path + '\\' + cam_num + '_annotations_v001')
                    os.rename(path + '\\' + dir[2], path + '\\' + cam_num + '_annotations_v001_1')
                else:
                    os.rename(path + '\\' + dir[0], path + '\\4')
                    os.rename(path + '\\' + dir[1], path + '\\4_annotations_v001')
                    os.rename(path + '\\' + dir[2], path + '\\4_annotations_v001_1')
    print("====================================================================")
    for (path, dir, files) in os.walk(PATH):
        if len(dir) == 3:
            if dir[1][-4:] == 'v001':
                pass
                # print(dir)

if __name__ == "__main__":
    make_txt_for_objectCounting()