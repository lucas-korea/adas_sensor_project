import numpy as np
import cv2
import sys
import math

np.set_printoptions(threshold=sys.maxsize)
pred_data = np.load("C:\\Users\\jcy37\\Documents\\SuperResolution\\20220913_429-UNet-from-32-to-128_prediction.npy") * 100
origin_data  = np.load("C:\\Users\\jcy37\\Documents\\SuperResolution\\20220913_429.npy")
#data = np.load("C:\\Users\\jcy37\\Documents\\SuperResolution\\ouster_range_image.npy")

# np.save('C:\\Users\\jcy37\\Documents\\SuperResolution\\20220913_4000.npy', data[:4000])
# np.save('C:\\Users\\jcy37\\Documents\\SuperResolution\\20220913_1000.npy', data[4000:])

frame_num = 410
max_range = 80
min_range = 2
HorizonResol = 360 / (1024)

pred_data_img = np.zeros((pred_data[0].shape[0], pred_data[0].shape[1]), dtype=np.uint8)
pred_data_var_img = np.zeros((origin_data[0].shape[0], origin_data[0].shape[1]), dtype=np.uint8)
origin_data_img = np.zeros((origin_data[0].shape[0], origin_data[0].shape[1]), dtype=np.uint8)

for col in range(pred_data[0].shape[1]):
    for row in range(pred_data[0].shape[0]):
        real_col = col
        real_col = col - (row % 4) *4
        if real_col < 0:
            real_col += 1024
        pred_data_img[row][real_col] = pred_data[frame_num][row][col][0]
        pred_data_var_img[row][real_col] = pred_data[frame_num][row][col][1]*10

        origin_data_img[row][real_col] = origin_data[frame_num][row][col][0]
        if origin_data_img[row][real_col] > max_range or origin_data_img[row][real_col] < min_range:
            origin_data_img[row][real_col] = 0
        origin_data_img = origin_data_img

pred_data_img = cv2.applyColorMap(pred_data_img, cv2.COLORMAP_JET)
cv2.imshow("pred_data_img", pred_data_img)
pred_data_var_img = cv2.applyColorMap(pred_data_var_img, cv2.COLORMAP_JET)
cv2.imshow("pred_data_var_img", pred_data_var_img)
origin_data_img = cv2.applyColorMap(origin_data_img, cv2.COLORMAP_JET)
cv2.imshow("origin_data", origin_data_img)

cv2.waitKey(0)

print(pred_data.shape)
print(origin_data.shape)

