import numpy as np


data =  np.array([[-0.037899380894, -0.032803202898, 0.99874300338],
       [-0.99870764917, 0.035111975735, -0.036744804429],
       [-0.033862492826, -0.99884488237, -0.034091531793]])

print(np.round(data, 3))
data2 = np.array([[0.13856241935], [-0.77479417726], [-1.2499001112]])
print(data)
print(data2)
print(data.T)

result = data.T @ data2 * -1

print("result:", result)