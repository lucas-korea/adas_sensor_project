import numpy as np
from PIL import Image

# Step 1: Read 16-bit binary data from a file
with open("C:\\Users\\jcy37\\source\\repos\\Project2\\data\\202301011_164940_21159646.bin", "rb") as file:
    binary_data = file.read(2048*2448)

# Step 2: Convert binary data to a NumPy array
data_array = np.frombuffer(binary_data, dtype=np.uint8)

# Step 3: Reshape the array to match image dimensions (e.g., width and height)
width = 2448  # Replace with your image's width
height = 2048  # Replace with your image's height
data_array = data_array.reshape((height, width))

# Step 4: Create a 16-bit image object
image = Image.fromarray(data_array)

# Step 5: Save the image or display it
image.save("output_image.png")  # Save the image to a file
image.show()  # Display the image (opens a viewer)
image.save('C:\\Users\\jcy37\\source\\repos\\Project2\\data\\202301011_164940_21159646.png')
# Optionally, you can convert the image to another format (e.g., TIFF) for better compatibility with 16-bit data.
# image.save("output_image.tiff", format="TIFF")