import PySpin
import time
serial_1 = "21159646"

system = PySpin.System.GetInstance()
print('get instance ....')

cam_list = system.GetCameras()

for i, cam in enumerate(cam_list):
    nodemap_tldevice = cam.GetTLDeviceNodeMap()
    cam.Init()
    nodemap = cam.GetNodeMap()
    node_acquisition_mode = PySpin.CEnumerationPtr(nodemap.GetNode('AcquisitionMode'))
    node_acquisition_mode_continuous = node_acquisition_mode.GetEntryByName('Continuous')
    acquisition_mode_continuous = node_acquisition_mode_continuous.GetValue()
    node_acquisition_mode.SetIntValue(acquisition_mode_continuous)
    cam.BeginAcquisition()
    processor = PySpin.ImageProcessor()
    processor.SetColorProcessing(PySpin.HQ_LINEAR)
    time1 = time.time_ns()
    for j in range(225):
        image_result = cam.GetNextImage()
        image_converted = processor.Convert(image_result, PySpin.PixelFormat_BayerRGPolarized8)
        # image_converted.Save("test_{}.jpg".format(j))
        # image_result.Release()
    print(float(time.time_ns()-time1)/1000000000)

    cam.EndAcquisition()
# cam_1 = cam_list.GetBySerial(serial_1)
# print(cam_1)
# cam_1.Init()
# print('init ....')
#
# nodemap = cam_1.GetNodeMap()
# nodemap_tldevice = cam_1.GetTLDeviceNodeMap()
# node_acquisition_mode = PySpin.CEnumerationPtr(nodemap.GetNode('AcquisitionMode'))
# node_acquisition_mode_continuous = node_acquisition_mode.GetEntryByName('Continuous')
#
# # Retrieve integer value from entry node
# acquisition_mode_continuous = node_acquisition_mode_continuous.GetValue()
#
# # Set integer value from entry node as new value of enumeration node
# node_acquisition_mode.SetIntValue(acquisition_mode_continuous)
#
#
#
# cam_1.LineSelector.SetValue(PySpin.LineSelector_Line2)
# cam_1.V3_3Enable.SetValue(True)
#
# cam_1.AcquisitionMode.SetValue(PySpin.AcquisitionMode_SingleFrame)
#
# cam_1.BeginAcquisition()
#
# processor = PySpin.ImageProcessor()
# processor.SetColorProcessing(PySpin.HQ_LINEAR)
# for i in range(10):
#     try:
#         print(i)
#         image_result = cam_1.GetNextImage()
#         print("GetNextImage")
#         if image_result.IsIncomplete():
#             print('Image incomplete with image status %d ...' % image_result.GetImageStatus())
#         else:
#             width = image_result.GetWidth()
#             height = image_result.GetHeight()
#             print('Grabbed Image %d, width = %d, height = %d' % (i, width, height))
#             image_converted = processor.Convert(image_result, PySpin.PixelFormat_Mono8)
#
#             # Create a unique filename
#             filename = 'Acquisition-%s-%d.jpg' % (serial_1, i)
#
#
#             image_converted.Save(filename)
#             print('Image saved at %s' % filename)
#             image_result.Release()
#             print('')
#     except PySpin.SpinnakerException as ex:
#         print('Error: %s' % ex)

# cam_1.EndAcquisition()