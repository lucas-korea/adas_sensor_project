import numpy as np

a = np.ones((5, 1)) * 5
x = np.ones((5, 4))
x = x*a
y = np.ones((5, 4)) *2
z = np.ones((5, 4)) *3

print(y)
print(np.stack([x, y, z], axis=-1).reshape(-1, 3))

