import cv2
import numpy as np
img = cv2.imread("C:\\Users\\jcy37\\PycharmProjects\\utils\\test.bmp")

# cv2.imshow('origin', img)
new_img = np.empty((5839+300,3885,3), dtype=np.uint8)
for i in range(150):
    new_img[i] = img[i]
for i in range(150):
    new_img[i+150] = img[150-i]
new_img[300:] = img

dst1 = cv2.resize(new_img, (777, 1228), interpolation=cv2.INTER_AREA)
cv2.imshow('resize', dst1)
print(img[0].shape)
print(type(img))
print(img.dtype)
# cv2.waitKey()
cv2.imwrite("newwedding.jpeg", new_img )