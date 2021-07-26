from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.set_xlim(-40, 40)
ax.set_ylim(-40, 40)
ax.set_zlim(-40, 40)
# ax.set_xticks([-10, -5, 0, 5, 10])
# ax.set_yticks([-10, -5, 0, 5, 10])
# ax.set_zticks([-10, -5, 0, 5, 10])

ax.scatter(1,1,20, alpha=1)
plt.tight_layout()
plt.show()