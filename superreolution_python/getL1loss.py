import numpy as np
print("data loading...")
origin_data = np.load("C:\\Users\\jcy37\\Documents\\SuperResolution\\20220913_429.npy")
print("load origin data done")
nomalize_parameter = 100
pred_data = np.load("C:\\Users\\jcy37\\Documents\\SuperResolution\\20220913_429-UNet-from-32-to-128_prediction.npy") * nomalize_parameter
print("load pred data done")


max_range = 80.0
min_range = 2.0
# 최대거리, 최소거리 삭제
condition_max = origin_data > max_range
condition_min = origin_data < min_range
origin_data[condition_max] = 0
origin_data[condition_min] = 0

# origin에는 있지만 pred에서는 사라져버린 remove 포인트 갯수
# ( ...which indcates the mean percentage of pixels deleted from the range images of each dataset)
LAMDA = 0.03
condition_remove = pred_data[:407,:,:,1:2] > pred_data[:407,:,:,0:1] * LAMDA
condition_remove = condition_remove.reshape(-1)
removed_point = np.count_nonzero(condition_remove)

print("data shape :" , origin_data.shape)
print("calculate L1 loss and removed point...")
L1_loss = sum(sum(sum(abs(origin_data[:407,:,:,0] - pred_data[:407,:,:,0]))))
print("# of removed point : ", removed_point )
print("removed percentage : {:.2f}% ".format(removed_point / (origin_data.shape[0] * origin_data.shape[1] * origin_data.shape[2]) * 100))
print("L1 loss mean : {:.2f}".format(L1_loss / (origin_data.shape[0] * origin_data.shape[1] * origin_data.shape[2])))