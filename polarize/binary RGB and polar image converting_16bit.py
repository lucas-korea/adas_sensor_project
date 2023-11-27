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

    RGB_image = np.zeros((int(height / 2), int(width / 2), 3), dtype=np.uint16)
    for i in range(int(height/2)):
        for j in range(int(width/2)):
            # print(gray_image[i*2][j*2])
            RGB_image[i][j][0] = gray_image[i*2][j*2]
            RGB_image[i][j][1] = gray_image[i*2+1][j*2]
            RGB_image[i][j][2] = gray_image[i*2+1][j*2+1]
    cv2.imwrite(imagename, RGB_image)
    RGB_image = cv2.resize(RGB_image, (int(width / 4), int(height / 4)))
    cv2.imshow('RGB_image', RGB_image)
    cv2.waitKey(1)
    print (imagename+" RGB color image created")

def createPolarSplitedColorImage(dataSet,path, basename, index,width=0):
    width = 2448
    height = 2048
    data = np.frombuffer(dataSet, dtype=np.uint16)
    image = data.reshape(height, width)
    # image = Image.new('I;16L', (width,height))
    # image.putdata(dataSet)


    imagename0 = path + '\\' + '0' '\\' + basename +'_' + index + "_0.png"
    imagename45 = path + '\\' + '45' '\\' + basename +'_' + index + "_45.png"
    imagename90 = path + '\\' + '90' '\\' + basename +'_' + index + "_90.png"
    imagename135 = path + '\\' + '135' '\\' + basename +'_' + index + "_135.png"
    imagenameAll = path + '\\' + 'All_angle' '\\' + basename +'_' + index + "_all.png"
    image = np.rot90(image, 2)
    # image = image.rotate(180)
    gray_image = np.array(image)

    image_0 = np.zeros((int(height / 4), int(width / 4), 3), dtype=np.uint16)
    image_45 = np.zeros((int(height / 4), int(width / 4), 3), dtype=np.uint16)
    image_135 = np.zeros((int(height / 4), int(width / 4), 3), dtype=np.uint16)
    image_90 = np.zeros((int(height / 4), int(width / 4), 3), dtype=np.uint16)

    for i in range(int(height / 4)):
        for j in range(int(width / 4)):
            image_0[i][j][0] = gray_image[i*4][j*4]
            image_0[i][j][1] = gray_image[i*4+2][j*4]
            image_0[i][j][2] = gray_image[i*4+2][j*4+2]

            image_45[i][j][0] = gray_image[i*4+1][j*4]
            image_45[i][j][1] = gray_image[i*4+2+1][j*4]
            image_45[i][j][2] = gray_image[i*4+2+1][j*4+2]

            image_135[i][j][0] = gray_image[i*4][j*4+1]
            image_135[i][j][1] = gray_image[i*4+2][j*4+1]
            image_135[i][j][2] = gray_image[i*4+2][j*4+2+1]

            image_90[i][j][0] = gray_image[i*4+1][j*4+1]
            image_90[i][j][1] = gray_image[i*4+2+1][j*4+1]
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
    print(image_all)
    cv2.waitKey()
    exit(10)


    print (path + '\\' + '0' '\\' + base_name +'_' + index + "_0.bmp" +" polar splited image created")

if __name__=="__main__":
    root_path = 'C:\\Users\\jcy37\\source\\repos\\Project2\\data'
    list1 = os.listdir(root_path)
    list_polar = [i for i in list1 if i.endswith('232000061.bin')]
    list_RGB   = [j for j in list1 if j.endswith('22623682.bin') ]

    print('#######################################')
    print('########### polar data ################')
    print('#######################################')
    cnt = 0
    for file in list_polar:
        print(cnt ,'/', len(list_polar), 'file')
        cnt += 1
        file_full_path= root_path + '\\' + file
        base_name=os.path.splitext(os.path.basename(file_full_path))[0]
        os.makedirs(root_path + "\\polar", exist_ok=True)
        os.makedirs(root_path + "\\polar\\0", exist_ok=True)
        os.makedirs(root_path + "\\polar\\45", exist_ok=True)
        os.makedirs(root_path + "\\polar\\90", exist_ok=True)
        os.makedirs(root_path + "\\polar\\135", exist_ok=True)
        os.makedirs(root_path + "\\polar\\All_angle", exist_ok=True)
        outputFilename=os.path.join(root_path + "\\polar",base_name)

        file = open(file_full_path, "rb")
        size = os.path.getsize(file_full_path)
        # 16bit 니까 2448*2048*2
        image_number = int(size / 2448/ 2048/2)
        for i in range(int(size / 2448/ 2048/2)):
            data = file.read(2448*2048*2)  # read byte by byte
            if i % 2 == 0:
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
        os.makedirs(root_path + "\\RGB", exist_ok=True)
        outputFilename=os.path.join(root_path + "\\RGB",base_name)

        file = open(file_full_path, "rb")
        size = os.path.getsize(file_full_path)
        image_number = int(size / 2448/ 2048/2)
        for i in range(int(size / 2448/ 2048/2)):
            data = file.read(2448*2048*2)  # read byte by byte
            if i % 2 == 0:
                print(i, "/", image_number, 'images')
                createRGBColorImage(data, outputFilename+'_' + str(i))
        file.close()