import  os,sys
from PIL import Image
import numpy as np
import cv2

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
    numpy_image = np.array(image)
    cv2.imshow('numpy_image', numpy_image)
    cv2.waitKey()
    imagename = outputfilename+".bmp"
    image = image.rotate(180)
    image.save(imagename)
    image.show()
    print (imagename+" Greyscale image created")

def createRGBColorImage(dataSet,outputfilename,width=0):
    width = 2448
    height = 2048

    image = Image.new('L', (width,height))
    image.putdata(dataSet)
    imagename = outputfilename+"_color.bmp"
    image = image.rotate(180)
    gray_image = np.array(image)

    RGB_image = np.zeros((int(height / 2), int(width / 2), 3), dtype=np.uint8)
    for i in range(int(height/2)):
        for j in range(int(width/2)):
            # print(gray_image[i*2][j*2])
            RGB_image[i][j][0] = gray_image[i*2][j*2]
            RGB_image[i][j][1] = (gray_image[i*2+1][j*2]/2 + gray_image[i*2][j*2+1]/2)
            RGB_image[i][j][2] = gray_image[i*2+1][j*2+1]
    cv2.imwrite(imagename, RGB_image)
    RGB_image = cv2.resize(RGB_image, (int(width / 4), int(height / 4)))
    cv2.imshow('RGB_image', RGB_image)
    cv2.waitKey(1)
    print (imagename+" RGB color image created")

def createPolarSplitedColorImage(dataSet,path, basename, index,width=0):
    width = 2448
    height = 2048
    image = Image.new('L', (width,height))
    image.putdata(dataSet)
    imagename0 = path + '\\' + '0' '\\' + basename +'_' + index + "_0.bmp"
    imagename45 = path + '\\' + '45' '\\' + basename +'_' + index + "_45.bmp"
    imagename90 = path + '\\' + '90' '\\' + basename +'_' + index + "_90.bmp"
    imagename135 = path + '\\' + '135' '\\' + basename +'_' + index + "_135.bmp"
    imagenameAll = path + '\\' + 'All_angle' '\\' + basename +'_' + index + "_all.bmp"
    image = image.rotate(180)
    gray_image = np.array(image)

    image_0 = np.zeros((int(height / 4), int(width / 4), 3), dtype=np.uint8)
    image_45 = np.zeros((int(height / 4), int(width / 4), 3), dtype=np.uint8)
    image_135 = np.zeros((int(height / 4), int(width / 4), 3), dtype=np.uint8)
    image_90 = np.zeros((int(height / 4), int(width / 4), 3), dtype=np.uint8)

    for i in range(int(height / 4)):
        for j in range(int(width / 4)):
            image_0[i][j][0] = gray_image[i*4][j*4]
            image_0[i][j][1] = (gray_image[i*4+2][j*4]/2 + gray_image[i*4][j*4+2]/2)
            image_0[i][j][2] = gray_image[i*4+2][j*4+2]

            image_45[i][j][0] = gray_image[i*4+1][j*4]
            image_45[i][j][1] = (gray_image[i*4+2+1][j*4]/2 + gray_image[i*4+1][j*4+2]/2)
            image_45[i][j][2] = gray_image[i*4+2+1][j*4+2]

            image_135[i][j][0] = gray_image[i*4][j*4+1]
            image_135[i][j][1] = (gray_image[i*4+2][j*4+1]/2 + gray_image[i*4][j*4+2+1]/2)
            image_135[i][j][2] = gray_image[i*4+2][j*4+2+1]

            image_90[i][j][0] = gray_image[i*4+1][j*4+1]
            image_90[i][j][1] = (gray_image[i*4+2+1][j*4+1]/2 + gray_image[i*4+1][j*4+2+1]/2)
            image_90[i][j][2] = gray_image[i*4+2+1][j*4+2+1]
    image0_45 = np.hstack((image_0,image_45))
    image135_90 = np.hstack((image_135, image_90))
    image_all = np.vstack((image0_45, image135_90))

    cv2.imwrite(imagename0, image_0)
    cv2.imwrite(imagename45, image_45)
    cv2.imwrite(imagename90, image_90)
    cv2.imwrite(imagename135, image_135)
    cv2.imwrite(imagenameAll, image_all)

    image_all = cv2.resize(image_all, (int(2448 / 4), int(2048 / 4)))
    cv2.imshow("image_all", image_all)
    cv2.waitKey(1)

    print (path + '\\' + '0' '\\' + base_name +'_' + index + "_0.bmp" +" polar splited image created")

if __name__=="__main__":
    root_path = 'E:\\polar_outsideDataAcquisition20230802'
    list1 = os.listdir(root_path)
    list_polar = [i for i in list1 if i.endswith('232000061.tmp')]
    list_RGB   = [j for j in list1 if j.endswith('22623682.tmp') ]

    print('#######################################')
    print('########### polar data ################')
    print('#######################################')
    cnt = 0
    for file in list_polar:
        print(cnt ,'/', len(list_polar), 'file')
        cnt += 1
        file_full_path= root_path + '\\' + file
        base_name=os.path.splitext(os.path.basename(file_full_path))[0]
        outputFilename=os.path.join(root_path + "\\polar",base_name)

        file = open(file_full_path, "rb")
        size = os.path.getsize(file_full_path)
        image_number = int(size / 2448/ 2048)

        for i in range(int(size / 2448/ 2048)):
            data = file.read(2448*2048)  # read byte by byte
            if i % 10 == 0:
                print(i, "/", image_number, 'images')
                createPolarSplitedColorImage(data, root_path + "\\polar", base_name, str(i))
        file.close()

    print('#######################################')
    print('###########  RGB data  ################')
    print('#######################################')
    cnt = 0
    for file in list_RGB:
        print(cnt ,'/', len(list_RGB), 'file')
        cnt += 1
        file_full_path= root_path + '\\' + file
        base_name=os.path.splitext(os.path.basename(file_full_path))[0]
        outputFilename=os.path.join(root_path + "\\RGB",base_name)

        file = open(file_full_path, "rb")
        size = os.path.getsize(file_full_path)
        image_number = int(size / 2448/ 2048)
        for i in range(int(size / 2448/ 2048)):
            data = file.read(2448*2048)  # read byte by byte
            if i % 10 == 0:
                print(i, "/", image_number, 'images')
                createRGBColorImage(data, outputFilename+'_' + str(i))
        file.close()