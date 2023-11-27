import os

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp2d

def linear_interpolation_color_image(image, new_shape):
    """
    Perform linear interpolation on a color image to resize it.

    Parameters:
    - image: 3D numpy array representing the original color image (height, width, channels).
    - new_shape: Tuple (new_height, new_width) representing the desired new shape.

    Returns:
    - 3D numpy array representing the resized color image.
    """
    height, width, channels = image.shape
    new_height, new_width = new_shape

    resized_image = np.zeros((new_height, new_width, channels), dtype=image.dtype)

    for c in range(channels):
        # Create a function for linear interpolation for each color channel
        interpolator = interp2d(np.arange(width), np.arange(height), image[:, :, c], kind='linear')

        # Generate new coordinates for the resized image
        new_x = np.linspace(0, width - 1, new_width)
        new_y = np.linspace(0, height - 1, new_height)

        # Perform the interpolation for each color channel
        resized_image[:, :, c] = interpolator(new_x, new_y)

    return resized_image

# Example usage:
# Load an example color image (you can replace this with your own image)
file_list = os.listdir('E:\\15000set\\polar_drive_image_all_angle')
cnt = 0
for file in file_list:
    print(file, cnt)
    cnt +=1
    original_color_image = plt.imread('E:\\15000set\\polar_drive_image_all_angle\\' + file)

    # Set the new shape for the resized image
    new_shape = (512*4, 612*4)

    # Perform linear interpolation for the color image
    resized_color_image = linear_interpolation_color_image(original_color_image, new_shape)

    # Display the original and resized color images

    plt.imsave('E:\\15000set\\polar_drive_image_all_angle_interpolation\\' + file, resized_color_image)
