import os
import sys
import struct
from matplotlib import pyplot as plt
import gc
import numpy as np


# fig, ax = plt.subplots(figsize=(15, 8))
# plt.grid(True)
# plt.xlabel('x')
# plt.ylabel('y')
# plt.title('Interactive Plot')
#
# ax.set(xlim=[-10, 10], ylim=[-10, 10])
# ax.set_aspect('auto', adjustable='box')
#
# xdata = [0]
# ydata = [0]
# line, = ax.plot(xdata, ydata)

xyz_lim = 10
fig = plt.figure()
# plt.style.use(['dark_background'])
ax = fig.add_subplot(111, projection='3d')
plt.cla()
ax.grid(True)
xdata = [0,1,2]
ydata = [0,1,2]
zdata = [0,1,2]
scatter = ax.plot(xdata,xdata,xdata, 'b.', alpha = 1)

# ax.set_xlim(-xyz_lim, xyz_lim)
# ax.set_ylim(-xyz_lim, xyz_lim)
# ax.set_zlim(-xyz_lim, xyz_lim)

# plt.axis('off')
plt.pause(0.001)
gc.collect()

def add_point(event):
    if event.inaxes != ax:
        return

    # button 1: 마우스 좌클릭
    if event.button == 11:
        x = event.xdata
        y = event.ydata
        print(event.xdata,event.ydata,event.zdata)
        xdata.append(x)
        ydata.append(y)

        scatter.set_data(xdata, ydata)
        plt.draw()

    # button 3: 마우스 우클릭 시 기존 입력값 삭제
    if event.button == 33:
        print(xdata)
        xdata.pop(0)
        ydata.pop(0)
        scatter.set_data(xdata, ydata)
        plt.draw()

    # 마우스 중간버튼 클릭 시 종료하기
    # if event.button == 2:
    #     plt.disconnect(cid)
    #     plt.close()

def key_press(event):
    sys.stdout.flush()
    if event.key == 'a':
        for i in range(len(xdata)):
            xdata[i] = xdata[i] - 1
    if event.key == 'd':
        for i in range(len(xdata)):
            xdata[i] = xdata[i] + 1
    if event.key == 'w':
        for i in range(len(xdata)):
            ydata[i] = ydata[i] - 1
    if event.key == 'x':
        for i in range(len(xdata)):
            ydata[i] = ydata[i] + 1
    if event.key == 'v':
        for i in range(len(xdata)):
            zdata[i] = zdata[i] - 1
    if event.key == 'r':
        for i in range(len(xdata)):
            zdata[i] = zdata[i] + 1

    plt.cla()
    ax.plot(xdata,ydata,zdata, 'b.', alpha = 1)
    plt.draw()

cid = plt.connect('button_press_event', add_point)
cid2 = plt.connect('key_press_event', key_press)
plt.show()