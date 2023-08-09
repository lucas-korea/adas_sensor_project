import  os,sys
from PIL import Image
# import numpy as np

def getBinaryData(filename):
    binaryValues = []
    file = open(filename, "rb")
    data = file.read(2048*2448)  # read byte by byte
    cnt =0
    return binaryValues

def createGreyScaleImageSpecificWith(dataSet,outputfilename,width=0):
    width = 2448
    height = 2048

    image = Image.new('L', (width,height))

    image.putdata(dataSet)

    imagename = outputfilename+".bmp"
    image = image.rotate(180)
    image.save(imagename)
    image.show()
    print (imagename+" Greyscale image created")



if __name__=="__main__":
    root_path = 'E:\\편광 야외 촬영 데이터20230802'
    list1 = os.listdir(root_path)
    list_polar = [i for i in list1 if i.endswith('232000061.tmp')]
    list_GRB   = [j for j in list1 if j.endswith('22623682.tmp') ]

    for file in list_polar:
        file_full_path= root_path + '\\' + file
        base_name=os.path.splitext(os.path.basename(file_full_path))[0]
        outputFilename=os.path.join(root_path + "\\polar",base_name)

        file = open(file_full_path, "rb")
        size = os.path.getsize(file_full_path)
        image_number = int(size / 2448/ 2048)

        for i in range(int(size / 2448/ 2048)):
            data = file.read(2448*2048)  # read byte by byte
            if i % 10 == 0:
                print(i, "/", image_number)
                createGreyScaleImageSpecificWith(data, outputFilename+'_' + str(i))

        file.close()

