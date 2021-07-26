import numpy as np
import matplotlib.cm as cm
import parse

x = np.arange(16)
ys = [i+x+(i*x)**2 for i in range(16)]
colors = cm.rainbow(np.linspace(0, 1, len(ys)))
colors[0] =  [255/255, 0/255, 0/255, 1.0]
colors[2] =  [255/255, 64/255, 0/255, 1.0]
colors[4] =  [255/255, 127/255, 0/255, 1.0]
colors[6] =  [255/255, 191/255, 0/255, 1.0]
colors[8] =  [255/255, 255/255, 0/255, 1.0]
colors[10] =  [170/255, 255/255, 0/255, 1.0]
colors[12] =  [85/255, 255/255, 0/255, 1.0]
colors[14] =  [0/255, 255/255, 0/255, 1.0]
colors[1] =  [0/255, 255/255, 64/255, 1.0]
colors[3] =  [0/255, 255/255, 127/255, 1.0]
colors[5] = [0/255, 255/255, 191/255, 1.0]
colors[7] = [0/255, 255/255, 255/255, 1.0]
colors[9] = [0/255, 191/255, 255/255, 1.0]
colors[11] = [0/255, 127/255, 255/255, 1.0]
colors[13] = [0/255, 64/255, 255/255, 1.0]
colors[15] = [0/255, 0/255, 255/255, 1.0]
colors = colors.tolist()
colors = np.array(colors * 24 * (parse.COUNT_THRESH+1))