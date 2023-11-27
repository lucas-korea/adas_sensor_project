import os
import cv2

# Replace with the actual path to your image


path = 'E:\\max distance experiment\\20231108_polar_Experiment\\wet ground\\pothole\\polarize'
for (root, dirs, files) in os.walk(path):
    for file in files:
        if file.endswith('.png'):
            print(file)
            image_path = root + '\\' + file

            # Read the original image
            original_image = cv2.imread(image_path)

            if original_image is None:
                print("Error: Could not read the image.")
                exit()

            # Specify the rotation angle (in degrees)
            rotation_angle = 180

            # Rotate the image
            rows, cols, _ = original_image.shape
            rotation_matrix = cv2.getRotationMatrix2D((cols / 2, rows / 2), rotation_angle, 1)
            rotated_image = cv2.warpAffine(original_image, rotation_matrix, (cols, rows))

            # Specify the path to save the rotated image
            output_path = root

            # Create the output directory if it doesn't exist
            os.makedirs(output_path, exist_ok=True)

            # Save the rotated image
            output_image_path = os.path.join(output_path, file)
            cv2.imwrite(output_image_path, rotated_image)

            print(output_image_path)


