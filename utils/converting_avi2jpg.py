import cv2

img = cv2.imread('C:\\Users\\jcy37\\PycharmProjects\\utils\\vehicle_30_side.jpg')

img_flip_lr = cv2.flip(img, 1)
cv2.imwrite('C:\\Users\\jcy37\\PycharmProjects\\utils\\vehicle_30_side_flip.jpg', img_flip_lr)