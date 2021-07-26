import numpy as np

A2 = np.array([[1,2,3],[4,5,6],[7,8,9]])

print(A2[A2>1])

bool_arr = A2[:,1] > 5
print(A2[:,1])
print(bool_arr)
print(bool_arr[1])


B2 = np.where(np.swapaxes([A2[:,1] > 2], 0, 1), 0, A2)
print(A2[:,1] > 2)
print(np.swapaxes([A2[:,1] > 2], 0, 1))
print(A2)
print(B2)