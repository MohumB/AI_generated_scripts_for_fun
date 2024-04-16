import os
import zipfile
import math
from PIL import Image
from collections import Counter

# Path to the zip file containing images
zip_file_path = 'flower_images.zip'

# Output PNG file path
output_png_path = 'tiled_image.png'

# Create a list to store extracted image paths
extracted_image_paths = []

# Extract images from the zip file
with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    for file_info in zip_ref.infolist():
        if file_info.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            extracted_image_path = zip_ref.extract(file_info)
            extracted_image_paths.append(extracted_image_path)

# Determine the most common image size
image_sizes = [Image.open(img_path).size for img_path in extracted_image_paths]
most_common_size = Counter(image_sizes).most_common(1)[0][0]

# Resize all images to the most common size
resized_image_paths = []
for img_path in extracted_image_paths:
    img = Image.open(img_path)
    if img.size != most_common_size:
        img = img.resize(most_common_size)
        resized_img_path = img_path.replace('.', '_resized.')
        img.save(resized_img_path)
        resized_image_paths.append(resized_img_path)
    else:
        resized_image_paths.append(img_path)

# Determine the dimensions of the tiled image
num_images = len(resized_image_paths)
tiles_per_row = math.ceil(math.sqrt(num_images))  # Number of images per row/column
tiles_per_column = math.ceil(num_images / tiles_per_row)
image_width, image_height = most_common_size
tiled_width = image_width * tiles_per_row
tiled_height = image_height * tiles_per_column  # Adjust the height based on the number of rows

# Create a new blank image (PNG)
tiled_image = Image.new('RGB', (tiled_width, tiled_height))

# Paste the resized images in a grid
for i, image_path in enumerate(resized_image_paths):
    img = Image.open(image_path)
    row = i // tiles_per_row
    col = i % tiles_per_row
    tiled_image.paste(img, (col * image_width, row * image_height))

# Save the tiled image as PNG
tiled_image.save(output_png_path, format='PNG')

print(f"Tiled PNG image saved to {output_png_path}")