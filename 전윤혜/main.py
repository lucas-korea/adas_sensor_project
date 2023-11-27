import os
import cv2
from tkinter import filedialog
from tkinter import messagebox
import numpy as np

def select_folder(str_):
    folder = filedialog.askdirectory(initialdir=os.getcwd(),
                                        title=str_)
    if folder == '':
        print("폴더을 추가 하세요")
        messagebox.showwarning("경고", "폴더을 추가 하세요")  # 파일 선택 안했을 때 메세지 출력
        exit(1)
    return "\\".join(folder.split("/"))

def select_file(str_):
    files = filedialog.askopenfilenames(initialdir=os.getcwd(),
                                        title=str_,
                                        filetypes=(("*.txt", "*txt"), ("*.xls", "*xls"), ("*.csv", "*csv")))
    if files == '':
        print("파일을 추가 하세요")
        messagebox.showwarning("경고", "파일을 추가 하세요")  # 파일 선택 안했을 때 메세지 출력
        exit(1)
    dir_path = ("\\".join(list(files)[0].split("/")[: -1]))  # path 추출
    files = ("\\".join(list(files)[0].split("/"))) #path\\파일명 추출
    return files, dir_path

def read_all_wave_images():
    # path = select_folder("파장대별 이미지가 포함되어 있는 폴더를 선택하세요")
    path = 'C:\\Users\\jcy37\\Desktop\\katech\\yoonhae_programe_develop\\sample\\sample1_pedestrian_maneking'
    img_file_list = os.listdir(path)
    img_data_list = []
    for i in range(len(img_file_list)):
        img_data_list.append(cv2.imread(path + '\\' + img_file_list[i]))
    return path, img_file_list,img_data_list # 폴더, 파일 이름, 파일 데이터 return

def crop_ROI(img_file_list, img_data_list):
    # ROI_txt_file, _ = select_file('원하는 검출영역 ROI가 적혀진 txt 파일을 선택하세요, 본 경로에 ROI crop 폴더가 생성됩니다')
    ROI_txt_file = 'C:\\Users\\jcy37\\Desktop\\katech\\yoonhae_programe_develop\\sample1_ROI.txt'
    os.makedirs(ROI_txt_file.split('.')[0], exist_ok=True) # ROI crop된 폴더 만들기
    with open(ROI_txt_file, 'r', encoding='utf-8') as f:
        line = ''
        target_list = []
        target_name = ''
        while(1): # 끝까지 한 라인씩 읽기
            try:
                line = f.readline()
                if line[0] == ' ':
                    x = int(line.split('=')[1].split(',')[0].replace('(', '').replace(')', '').replace(' ', '').replace(
                        '\n', ''))
                    y = int(line.split('=')[1].split(',')[1].replace('(', '').replace(')', '').replace(' ', '').replace(
                        '\n', ''))
                    w = int(line.split('=')[1].split(',')[2].replace('(', '').replace(')', '').replace(' ', '').replace(
                        '\n', ''))
                    h = int(line.split('=')[1].split(',')[3].replace('(', '').replace(')', '').replace(' ', '').replace(
                        '\n', ''))
                    for i in range(len(img_data_list)):

                        cv2.imwrite(ROI_txt_file.split('.')[0]+'\\' + img_file_list[i].split('\\')[-1].split('.')[0] + '_' + target_name+'.bmp',
                                    img_data_list[i][y : y+h , x : x+w])
                # 마지막 줄 읽으면 종료
                elif line == '-------------------------------------------\n' or '':
                    print("ROI_txt_file read done")
                    break
                else:
                    # 타겟 이름 추출
                    target_name = line.replace('\n', '')
                    target_list.append(target_name)
            except Exception as e:
                print(e)
                break
    ## ROI crop 폴더 return
    return ROI_txt_file.split('.')[0], target_list

## 각 crop된 파일들의 median 밸류를 출력하고 median_value.txt 파일로 저장
def get_median_value_each_wavelength(ROI_crop_folder):
    crop_data_list = [file for file in os.listdir(ROI_crop_folder) if file.endswith('bmp')]
    with open(ROI_crop_folder + '\\' + "median_value.txt", 'w') as f:
        for i in range(len(crop_data_list)):
            crop_data = cv2.imread(ROI_crop_folder + '\\' + crop_data_list[i])
            print(crop_data_list[i], ' median value :' ,np.median(crop_data))
            f.write(crop_data_list[i])
            f.write('\t')
            f.write(str(np.median(crop_data)))
            f.write('\n')

def RQ_3_1(path, ROI_crop_folder, target_list):
    texture_info_image_list = os.listdir(ROI_crop_folder)
    median_list = []
    median_sum = 0
    median_rootsqaure = 0
    for i in range(len(target_list)): #target은 피부, 티셔츠같은 재질을 의미
        print(target_list[i])
        wavelength_files = [file for file in texture_info_image_list if file.endswith(target_list[i] + '.bmp')]
        wavelength_files_iamge = []
        for file in wavelength_files:
            img_1064 = cv2.imread(ROI_crop_folder + '\\' + wavelength_files[0])
            median_list.append(np.median(img_1064))
            wavelength_files_iamge.append(img_1064)
            img_1150 = cv2.imread(ROI_crop_folder + '\\' + wavelength_files[1])
            median_list.append(np.median(img_1150))
            wavelength_files_iamge.append(img_1150)
            img_1152 = cv2.imread(ROI_crop_folder + '\\' + wavelength_files[2])
            median_list.append(np.median(img_1152))
            wavelength_files_iamge.append(img_1152)
            img_1200 = cv2.imread(ROI_crop_folder + '\\' + wavelength_files[3])
            median_list.append(np.median(img_1200))
            wavelength_files_iamge.append(img_1200)
            img_1250 = cv2.imread(ROI_crop_folder + '\\' + wavelength_files[4])
            median_list.append(np.median(img_1250))
            wavelength_files_iamge.append(img_1250)
            img_1300 = cv2.imread(ROI_crop_folder + '\\' + wavelength_files[5])
            median_list.append(np.median(img_1300))
            wavelength_files_iamge.append(img_1300)
            img_1310 = cv2.imread(ROI_crop_folder + '\\' + wavelength_files[6])
            median_list.append(np.median(img_1310))
            wavelength_files_iamge.append(img_1310)
            img_1330 = cv2.imread(ROI_crop_folder + '\\' + wavelength_files[7])
            median_list.append(np.median(img_1330))
            wavelength_files_iamge.append(img_1330)
            img_1350 = cv2.imread(ROI_crop_folder + '\\' + wavelength_files[8])
            median_list.append(np.median(img_1350))
            wavelength_files_iamge.append(img_1350)
            img_1400 = cv2.imread(ROI_crop_folder + '\\' + wavelength_files[9])
            median_list.append(np.median(img_1400))
            wavelength_files_iamge.append(img_1400)
            img_1450 = cv2.imread(ROI_crop_folder + '\\' + wavelength_files[10])
            median_list.append(np.median(img_1450))
            wavelength_files_iamge.append(img_1450)
            img_1490 = cv2.imread(ROI_crop_folder + '\\' + wavelength_files[11])
            median_list.append(np.median(img_1490))
            wavelength_files_iamge.append(img_1490)
            img_1510 = cv2.imread(ROI_crop_folder + '\\' + wavelength_files[12])
            median_list.append(np.median(img_1510))
            wavelength_files_iamge.append(img_1510)
            img_1530 = cv2.imread(ROI_crop_folder + '\\' + wavelength_files[13])
            median_list.append(np.median(img_1530))
            wavelength_files_iamge.append(img_1530)
            img_1550 = cv2.imread(ROI_crop_folder + '\\' + wavelength_files[14])
            median_list.append(np.median(img_1550))
            wavelength_files_iamge.append(img_1550)
            img_1570 = cv2.imread(ROI_crop_folder + '\\' + wavelength_files[15])
            median_list.append(np.median(img_1570))
            wavelength_files_iamge.append(img_1570)
            img_1590 = cv2.imread(ROI_crop_folder + '\\' + wavelength_files[16])
            median_list.append(np.median(img_1590))
            wavelength_files_iamge.append(img_1590)
            img_1610 = cv2.imread(ROI_crop_folder + '\\' + wavelength_files[17])
            median_list.append(np.median(img_1610))
            wavelength_files_iamge.append(img_1610)
            img_1650 = cv2.imread(ROI_crop_folder + '\\' + wavelength_files[18])
            median_list.append(np.median(img_1650))
            wavelength_files_iamge.append(img_1650)
            img_980  = cv2.imread(ROI_crop_folder + '\\' + wavelength_files[19])
            median_list.append(np.median(img_980))
            wavelength_files_iamge.append(img_980)
            median_sum = np.sum(median_list)
            median_rootsqaure = np.sqrt(np.sum(np.asarray(median_list) * np.asarray(median_list))) #스칼라곱
        SHAPE = img_1064.shape #다른 파장도 shape은 어차피 같음
        # print(SHAPE)
        new_image = np.zeros(SHAPE, dtype=np.float64)
        for row in range(SHAPE[0]):
            for col in range(SHAPE[1]):
                # print(img_1064[row][col])
                # print(img_1064[row][col]**2)
                # print(img_1064[row][col] * img_1064[row][col])
                # exit(1)
                root_square = np.sqrt(img_1064[row][col] ** 2 +
                                                                               img_1150[row][col] ** 2 +
                                                                               img_1152[row][col] ** 2 +
                                                                               img_1200[row][col] ** 2 +
                                                                               img_1250[row][col] ** 2 +
                                                                               img_1300[row][col] ** 2 +
                                                                               img_1310[row][col] ** 2 +
                                                                               img_1330[row][col] ** 2 +
                                                                               img_1350[row][col] ** 2 +
                                                                               img_1400[row][col] ** 2 +
                                                                               img_1450[row][col] ** 2 +
                                                                               img_1490[row][col] ** 2 +
                                                                               img_1510[row][col] ** 2 +
                                                                               img_1530[row][col] ** 2 +
                                                                               img_1550[row][col] ** 2 +
                                                                               img_1570[row][col] ** 2 +
                                                                               img_1590[row][col] ** 2 +
                                                                               img_1610[row][col] ** 2 +
                                                                               img_1650[row][col] ** 2 +
                                                                               img_980[row][col] ** 2)
                new_image[row][col] = median_sum / median_rootsqaure / root_square
                if root_square[0] == 0: #본 이미지에서의 값이 0이면 결과에 상관없이 파장대별 평균값 이미지에서도 0
                    new_image[row][col] = 0
                if new_image[row][col][0] < 1:
                    print(new_image[row][col])
                # print(row, col)
                # print(new_image[row][col])
                # if (np.isnan(new_image[row][col])):
                #     print(row, col)
        new_image = cv2.resize(new_image, (0, 0), fx=8, fy=8, interpolation=cv2.INTER_NEAREST)  # 스케일 팩터 이용
        # cv2.imshow(target_list[i],new_image)
        print(new_image.max())
        print(new_image.min())
        # for i in range(len(new_image)):
        #     print(len(new_image))
        #     print(new_image.shape)
        #     print(new_image[:,:,0].shape)
        #     if new_image[0] < 1:
        #         print(i)
        # print(new_image)
        new_image = new_image / new_image.max()  # normalizes data in range 0 - 255

        new_image = 255 * new_image
        img = new_image.astype(np.uint8)
        cv2.imshow(target_list[i], img)
        cv2.waitKey()
        print(wavelength_files)
if __name__ == "__main__":
    path, img_file_list,img_data_list = read_all_wave_images()
    ROI_crop_folder, target_list =  crop_ROI(img_file_list, img_data_list)
    get_median_value_each_wavelength(ROI_crop_folder)
    RQ_3_1(path, ROI_crop_folder, target_list)
