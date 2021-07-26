import numpy as np
import math
a = np.zeros(12) # 모든값이 0인 2x3 배열 생성.
# print(a[1])
# print(a)
angle = [-15, 1, -13, -3 ,-11, 5, -9, 7, -7, 9, -5, 11, -3, 13, -1, 15] * 2

# print(angle)

pos_intens = np.zeros((16, 24, 2))
# print(pos_intens)

angle = np.array([-15, 1, -13, -3 ,-11, 5, -9, 7, -7, 9, -5, 11, -3, 13, -1, 15])
angle_radian = angle / 180 * math.pi
angle_radian = np.transpose(np.array([angle_radian]))


Azimuth = np.ones(24)
distance = np.ones((16, 24))
Azimuth_pi = np.array(Azimuth * math.pi / 180)
Azimuth_pi2 = Azimuth * math.pi / 180
# print(angle_radian.shape, Azimuth_pi.shape, distance.shape)

x = distance * np.sin(Azimuth_pi) * np.cos(angle_radian)
y = distance * np.cos(Azimuth_pi) * np.cos(angle_radian)

print("distance\n", distance)
print("sin(Azimuth_radian)\n", np.sin(Azimuth_pi))
print("cos(angle_radian)\n", np.cos(angle_radian))
print(x)
#
# print(y)
# print((x+y).shape)
# npstack = np.stack([x,y,x], axis=-1)
# print(npstack.shape)
# print(npstack)
# print((npstack.reshape(-1, 3)).shape)
# print(npstack.reshape(-1, 3))
# npstack = npstack.reshape(-1, 3)
#
# arr = np.empty((1, 3), dtype=float)
# arr = np.append(arr, npstack, axis=0)
# arr = np.delete(arr, 0, axis=0)
# print(arr.shape)
# print(arr)
# print("\n\n")
# print(arr[:][0])
#
# print(arr[:, 0])
# print(Azimuth_pi.dtype)
# print(type(Azimuth_pi2))
#
# l = [1,2,3]
# print (hex(id(l)))
# l = np.empty((1, 3), dtype=float)
# print (hex(id(l)))
import numpy as np
# import matplotlib.pyplot as plt
#
# plt.axis([0, 10, 0, 1])
#
#
#
# import numpy as np
# import matplotlib.pyplot as plt
# x=0
# plt.title("Real Time plot")
# plt.xlabel("x")
# plt.ylabel("sinx")
# for i in range(100):
#     x=x+0.04
#     y = np.sin(x)
#     plt.plot(x, y, 'o')
#     plt.pause(0.0000001)

# plt.show()


# distance = np.array([[1, 2, 3], [4, 5, 6]])
# Azimuth = np.array([2, 3, 4])
# Azimuth2 = np.array([[2], [3]])
# print(distance * Azimuth)
# print(distance * Azimuth2)
# print(distance.shape, Azimuth.shape, Azimuth2.shape)

import sys
arr = np.array([[[3, 4, 5, 6], [3, 4, 5, 6], [3, 4, 5, 6], [3, 4, 5, 6], [3, 4, 5, 6]],
                [[0, 4, 5, 6], [0, 4, 5, 6], [0, 4, 5, 6], [0, 4, 5, 6], [0, 4, 5, 6]],
                [[3, 4, 5, 6], [3, 4, 5, 6], [3, 4, 5, 6], [3, 4, 5, 6], [3, 4, 5, 6]]], dtype=np.float64)
a, b, c = arr.shape
print(arr.shape, a*b*c)

print(sys.getsizeof(arr))
arr = np.array([[[3, 4, 5, 6], [3, 4, 5, 6], [3, 4, 5, 6], [3, 4, 5, 6], [3, 4, 5, 6]],
                [[0, 4, 5, 6], [0, 4, 5, 6], [0, 4, 5, 6], [0, 4, 5, 6], [0, 4, 5, 6]],
                [[0, 4, 5, 6], [0, 4, 5, 6], [0, 4, 5, 6], [0, 4, 5, 6], [0, 4, 5, 6]],
                [[3, 4, 5, 6], [3, 4, 5, 6], [3, 4, 5, 6], [3, 4, 5, 6], [3, 4, 5, 6]]], dtype=np.float64)
a, b, c = arr.shape
print(arr.shape, a*b*c)

print(sys.getsizeof(arr))
