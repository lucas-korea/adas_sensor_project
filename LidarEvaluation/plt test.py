import matplotlib.pyplot as plt

sub_plots = plt.subplots(2, 1)

fig = sub_plots[0]
graph = sub_plots[1]

print(fig, sub_plots)

fig = plt.figure()
ax = fig.add_subplot(121, projection='3d')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax2 = fig.add_subplot(122)
xyz_lim = 15
print(ax)
print(fig)
ax.cla()