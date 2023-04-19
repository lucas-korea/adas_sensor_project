import PySpin
from time import time
serial_1 = "21159646" #편광 카메라
serial_2 = '22623682'

system = PySpin.System.GetInstance()

cam_list = system.GetCameras()

cam_1 = cam_list.GetBySerial(serial_1)
cam_2 = cam_list.GetBySerial(serial_2)

cam_1.Init()
cam_2.Init()
print("init")

cam_1.LineSelector.SetValue(PySpin.LineSelector_Line2)
cam_1.V3_3Enable.SetValue(True)

cam_2.TriggerMode.SetValue(PySpin.TriggerMode_Off)
cam_2.TriggerSource.SetValue(PySpin.TriggerSource_Line3)
cam_2.TriggerOverlap.SetValue(PySpin.TriggerOverlap_ReadOut)
cam_2.TriggerMode.SetValue(PySpin.TriggerMode_On)
print("setting...")

cam_1.AcquisitionMode.SetValue(PySpin.AcquisitionMode_SingleFrame)
cam_2.AcquisitionMode.SetValue(PySpin.AcquisitionMode_SingleFrame)

cam_2.BeginAcquisition()
cam_1.BeginAcquisition()
print("begin...")

image_1 = cam_1.GetNextImage()
image_2 = cam_2.GetNextImage()
print("get image....")

image_1.Save('cam_1_{}.png'.format(time()))
image_2.Save('cam_2_{}.png'.format(time()))

image_1.Release()
image_2.Release()

cam_1.EndAcquisition()
cam_2.EndAcquisition()