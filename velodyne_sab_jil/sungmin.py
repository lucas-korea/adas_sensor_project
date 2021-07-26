#!/usr/bin/env python
import socket
import math
import vtk
from numpy import random
import os
import sys
import numpy as np

test = 1
def cal_lidar_pos(Azimuth_, distance_, angle_):
    Azimuth_pi = Azimuth_ * math.pi / 180
    angle_pi = angle_ * math.pi / 180
    x_ = distance_ * math.sin(Azimuth_pi) * math.cos(angle_pi)
    y_ = distance_ * math.cos(Azimuth_pi) * math.cos(angle_pi)
    z_ = distance_ * math.sin(angle_pi)
    return(x_, y_, z_)

class VtkPointCloud:

    def __init__(self, zMin=-10.0, zMax=10.0, maxNumPoints=1e6):
        self.maxNumPoints = maxNumPoints
        self.vtkPolyData = vtk.vtkPolyData()
        self.clearPoints()
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(self.vtkPolyData)
        mapper.SetColorModeToDefault()
        mapper.SetScalarRange(zMin, zMax)
        mapper.SetScalarVisibility(1)
        self.vtkActor = vtk.vtkActor()
        self.vtkActor.SetMapper(mapper)

    def addPoint(self, point):
        if self.vtkPoints.GetNumberOfPoints() < self.maxNumPoints:
            pointId = self.vtkPoints.InsertNextPoint(point[:])
            self.vtkDepth.InsertNextValue(point[2])
            self.vtkCells.InsertNextCell(1)
            self.vtkCells.InsertCellPoint(pointId)
        else:
            r = random.randint(0, self.maxNumPoints)
            self.vtkPoints.SetPoint(r, point[:])
        self.vtkCells.Modified()
        self.vtkPoints.Modified()
        self.vtkDepth.Modified()

    def clearPoints(self):

        self.vtkPoints = vtk.vtkPoints()
        self.vtkCells = vtk.vtkCellArray()
        self.vtkDepth = vtk.vtkDoubleArray()
        self.vtkDepth.SetName('DepthArray')
        self.vtkPolyData.SetPoints(self.vtkPoints)
        self.vtkPolyData.SetVerts(self.vtkCells)
        self.vtkPolyData.GetPointData().SetScalars(self.vtkDepth)
        self.vtkPolyData.GetPointData().SetActiveScalars('DepthArray')

    def removePoints(self):

        self.vtkPolyData.GetPointData().Reset()
        self.vtkPolyData.GetPointData().Update()
        # self.vtkPoints.GetNumberOfPoints()
        print("test")


IP_ADDRESS = "192.168.1.77"
PORT_NO = 2368
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSocket.bind((IP_ADDRESS, PORT_NO))
vertical_angle = [-15, 1, -13, -3, -11, 5, -9, 7, -7, 9, -5, 11, -3, 13, -1, 15]

class AddPointCloudTimerCallback():
    def __init__(self, renderer, iterations):
        self.iterations = iterations
        self.renderer = renderer

    def load_data(self, point_cloud_path):
        # 0: left and right (-5:5); 1: near and further (10:-30); 2: up and down (-1:3)
        # 0: left < right
        # 1: near < further
        # 2: up < down
        # x_thresh = [-5, 5]
        # y_thresh = [-30, 10]
        # z_thresh = [-1, 3]

        # x_thresh = [-1.1, 1.8]
        # y_thresh = [-2.5, -1.5]
        # z_thresh = [-0.4, 2.1]

        x_thresh = [-1.1, 2.1]
        y_thresh = [1.5, 4.5]
        z_thresh = [-0.4, 2.1]

        file_path = os.path.join(point_cloud_path)
        # file_path = os.path.join(point_cloud_path, 'frame('+str(img_num)+').csv')
        point_list = []
        all_point_list = []
        with open(file_path) as f:
            f.readline()
            while True:
                data = f.readline()
                if not data:
                    break
                if data != '\n':
                    point_coords = np.float64(data.strip().split(',')[:3])
                    all_point_list.append(point_coords)
                    # if (point_coords[0] > x_thresh[0]) and (point_coords[0] < x_thresh[1]) and \
                    #        (point_coords[1] > y_thresh[0]) and (point_coords[1] < y_thresh[1]) and \
                    #        (point_coords[2] > z_thresh[0]) and (point_coords[2] < z_thresh[1]):
                    point_list.append(point_coords)
        point_list = np.array(point_list)
        all_point_list = np.array(all_point_list)
        thresh = [x_thresh, y_thresh, z_thresh]
        return point_list, all_point_list, thresh

    def execute(self, iren, event):
        # iren.DestroyTimer(self.timerId)
        pointCloud = VtkPointCloud()
        self.renderer.AddActor(pointCloud.vtkActor)
        pointCloud.clearPoints()

        if self.iterations == 0:
            pointCloud.removePoints()
            self.iterations = 30

        # 영역 별 파싱 필요
        # print("again {}". format(self.iterations))
        for w in range(50):
            array = serverSocket.recv(1206)
            add = 0
            for block in range(12):
                Azimuth = (array[3 + add] * 256 + array[2 + add]) / 100
                print("data block :", block, "$$Azimuth :", Azimuth)
                add += 4
                for double_ in range(2):
                    for channel in range(16):
                        angle = vertical_angle[channel]
                        distance = round((array[5 + add] * 256 + array[4 + add]) * 0.002, 3)
                        intensity = array[6 + add]
                        # print("$$channel {} angle{} $$distance : {} $$intensity : {}".format(channel, vertical_angle[channel], distance, intensity))
                        x, y, z = cal_lidar_pos(Azimuth, distance, angle)
                        # pointCloud.addPoint([x, y, z])

        # for i in range(1, 5000):
        #     #    print(i)
        #     point = 20 * (random.rand(3) - 0.5)
        #     # print(point)
        #     point_coords = point
        #     pointCloud.addPoint(point_coords)

        iren.GetRenderWindow().Render()
        pointCloud.clearPoints()

        self.iterations -= 1


if __name__ == "__main__":
    # Renderer
    renderer = vtk.vtkRenderer()
    renderer.SetBackground(.2, .3, .4)
    renderer.ResetCamera()

    # Render Window
    renderWindow = vtk.vtkRenderWindow()

    renderWindow.AddRenderer(renderer)

    # Interactor
    renderWindowInteractor = vtk.vtkRenderWindowInteractor()
    renderWindowInteractor.SetRenderWindow(renderWindow)
    renderWindowInteractor.Initialize()

    # Initialize a timer for the animation
    addPointCloudTimerCallback = AddPointCloudTimerCallback(renderer, 30)
    renderWindowInteractor.AddObserver('TimerEvent', addPointCloudTimerCallback.execute)
    timerId = renderWindowInteractor.CreateRepeatingTimer(10)
    addPointCloudTimerCallback.timerId = timerId

    # Begin Interaction
    renderWindow.Render()
    renderWindowInteractor.Start()