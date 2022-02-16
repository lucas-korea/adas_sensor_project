import sys
import cv2
import numpy as np

l = 2448
h = 2048

img = cv2.imread('C:\\232.bmp')
print(img.shape)
image90 = np.zeros((int(h/2), int(l/2), 3), dtype=np.uint8)*255
image45 = np.zeros((int(h/2), int(l/2), 3), dtype=np.uint8)*255
image135 = np.zeros((int(h/2), int(l/2), 3), dtype=np.uint8)*255
image0 = np.zeros((int(h/2), int(l/2), 3), dtype=np.uint8)*255
img[0,0] = (255,0,0)
img[0,1] = (0,255,0)
img[1,1] = (0,0,255)
img[1,0] = (255,255,255)
# for i in range(int(h/2)):
#     for j in range(int(l/2)):
#         image90[i,j] = img[i * 2,j * 2]
#         image45[i, j] = img[i * 2, j * 2 + 1]
#         image135[i, j] = img[i * 2 + 1, j * 2]
#         image0[i, j] = img[i * 2 + 1, j * 2 + 1]
for i in range(0, int(h/2),2):
    for j in range(0, int(l/2),2):
        image90[i, j] = img[i * 2,j * 2]
        image90[i + 1, j] = img[i * 2 + 1, j * 2]
        image90[i, j + 1] = img[i * 2, j * 2 + 1]
        image90[i + 1, j + 1] = img[i * 2 + 1, j * 2 + 1]
        image45[i, j] = img[i * 2, j * 2 + 2]
        image45[i + 1, j] = img[i * 2 + 1, j * 2 + 2]
        image45[i, j + 1] = img[i * 2, j * 2 + 2 + 1]
        image45[i + 1, j + 1] = img[i * 2 + 1, j * 2 + 2 + 1]
        image135[i, j] = img[i * 2 + 2, j * 2]
        image135[i + 1, j] = img[i * 2 + 2 + 1, j * 2]
        image135[i, j + 1] = img[i * 2 + 2, j * 2 + 1]
        image135[i + 1, j + 1] = img[i * 2 + 2 + 1, j * 2 + 1]
        image0[i, j] = img[i * 2 + 2, j * 2 + 2]
        image0[i + 1, j] = img[i * 2 + 2 + 1, j * 2 + 2]
        image0[i, j + 1] = img[i * 2 + 2, j * 2 + 2 + 1]
        image0[i + 1, j + 1] = img[i * 2 + 2 + 1, j * 2 + 2 + 1]
# if img is None:
#     print("이미지 로드가 실패 했습니다.")
#     sys.exit()

print(img[1820,1020])
# img[0,0] = [255, 0 , 0]
cv2.imshow('image', img)
cv2.imshow('image90', image90)
cv2.imshow('image45', image45)
cv2.imshow('image135', image135)
cv2.imshow('image0', image0)
cv2.waitKey()

cv2.destroyWindow()