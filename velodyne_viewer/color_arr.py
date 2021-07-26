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

def intensity_color(point_cloud):
    color_arr_intensity = np.zeros((len(point_cloud), 3))
    for j in range(len(point_cloud)):
        val = point_cloud[j, 3]
        if val < 64:
            color_arr_intensity[j, 0] = 0
            color_arr_intensity[j, 1] = val / 64
            color_arr_intensity[j, 2] = 1
        elif val >= 64 and val < 127:
            color_arr_intensity[j, 0] = 0
            color_arr_intensity[j, 1] = 1
            color_arr_intensity[j, 2] = 1 - (val - 64) / 63
        elif val >= 127 and val < 191:
            color_arr_intensity[j, 0] = (val - 127) / 63
            color_arr_intensity[j, 1] = 1
            color_arr_intensity[j, 2] = 0
        else:
            color_arr_intensity[j, 0] = 1
            color_arr_intensity[j, 1] = 1 - (val - 191) / 63
            color_arr_intensity[j, 2] = 0
    return color_arr_intensity

def distance_color(point_cloud_dist, max_dist=200): #velodyne puck max = 200meter
    color_arr_distance = np.zeros((len(point_cloud_dist), 3))
    dist_arr = point_cloud_dist
    queter_dist = max_dist / 4
    for j in range(len(dist_arr)):
        val = dist_arr[j]
        if val < max_dist:
            color_arr_distance[j, :] = val / max_dist
        else:
            color_arr_distance[j, :] = 1



        # if val < queter_dist:
        #     color_arr_distance[j, 0] = 0
        #     color_arr_distance[j, 1] = val / queter_dist
        #     color_arr_distance[j, 2] = 1
        # elif val >= queter_dist and val < queter_dist * 2:
        #     color_arr_distance[j, 0] = 0
        #     color_arr_distance[j, 1] = 1
        #     color_arr_distance[j, 2] = 1 - (val - queter_dist) / queter_dist
        # elif val >= queter_dist * 2 and val < queter_dist * 3:
        #     color_arr_distance[j, 0] = (val - queter_dist * 2) / queter_dist
        #     color_arr_distance[j, 1] = 1
        #     color_arr_distance[j, 2] = 0
        # elif val >= queter_dist * 3 and val <= max_dist:
        #     color_arr_distance[j, 0] = 1
        #     color_arr_distance[j, 1] = 1 - (val - queter_dist * 3) / queter_dist
        #     color_arr_distance[j, 2] = 0
        # else:
        #     color_arr_distance[j, 0] = 1
        #     color_arr_distance[j, 1] = 0
        #     color_arr_distance[j, 2] = 0
    return color_arr_distance