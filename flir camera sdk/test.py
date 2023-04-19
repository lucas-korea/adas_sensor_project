import os
import PySpin
import sys

NUM_IMAGES = 10  # number of images to grab

def acquire_images(cam, nodemap, nodemap_tldevice):

    try:
        result = True
        node_acquisition_mode = PySpin.CEnumerationPtr(nodemap.GetNode('AcquisitionMode'))
        node_acquisition_mode_continuous = node_acquisition_mode.GetEntryByName('Continuous')

        # Retrieve integer value from entry node
        acquisition_mode_continuous = node_acquisition_mode_continuous.GetValue()

        # Set integer value from entry node as new value of enumeration node
        node_acquisition_mode.SetIntValue(acquisition_mode_continuous)

        print('Acquisition mode set to continuous...')
        cam.BeginAcquisition()
        print('Acquiring images...')

        device_serial_number = ''
        node_device_serial_number = PySpin.CStringPtr(nodemap_tldevice.GetNode('DeviceSerialNumber'))
        if PySpin.IsAvailable(node_device_serial_number) and PySpin.IsReadable(node_device_serial_number):
            device_serial_number = node_device_serial_number.GetValue()
            print('Device serial number retrieved as %s...' % device_serial_number)

        processor = PySpin.ImageProcessor()
        processor.SetColorProcessing(PySpin.HQ_LINEAR)
        PySpin.BalanceRatioSelector_Red
        PySpin.Exposure
        for i in range(NUM_IMAGES):
            try:
                image_result = cam.GetNextImage()
                if image_result.IsIncomplete():
                    print('Image incomplete with image status %d ...' % image_result.GetImageStatus())
                else:
                    width = image_result.GetWidth()
                    height = image_result.GetHeight()
                    image_converted = processor.Convert(image_result, PySpin.PixelFormat_BayerRGPolarized8)
                    # Create a unique filename
                    if device_serial_number:
                        filename = 'Acquisition-%s-%d.jpg' % (device_serial_number, i)
                    else:  # if serial number is empty
                        filename = 'Acquisition-%d.jpg' % i

                    image_converted.Save(filename)
                    print('Image saved at %s' % filename)
                    image_result.Release()
            except PySpin.SpinnakerException as ex:
                print('Error: %s' % ex)
                return False
        cam.EndAcquisition()

    except PySpin.SpinnakerException as ex:
        print('Error: %s' % ex)
        return False

    return result


def run_single_camera(cam):
    nodemap_tldevice = cam.GetTLDeviceNodeMap()
    cam.Init()
    nodemap = cam.GetNodeMap()
    acquire_images(cam, nodemap, nodemap_tldevice)
    cam.DeInit()
    return True


def main():
    result = True
    # Retrieve singleton reference to system object
    system = PySpin.System.GetInstance()
    # Retrieve list of cameras from the system
    cam_list = system.GetCameras()
    print(cam_list)
    for i, cam in enumerate(cam_list):
        result &= run_single_camera(cam)
    cam_list.Clear()
    system.ReleaseInstance()
    return result

if __name__ == '__main__':
    main()
