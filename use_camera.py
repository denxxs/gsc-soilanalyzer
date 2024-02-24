from PIL import Image
import numpy as np

def average_image_color(filename):
    img = Image.open(filename).convert('RGB')
    pixels = np.array(img)

    # Calculate the average RGB values
    average_color = pixels.mean(axis=(0, 1))
    rgb=list(average_color)

    r = (rgb[0])
    g = (rgb[1])
    b = (rgb[2]) 

    sum = r + g + b
     # Check if the total_sum is not zero to avoid division by zero
    if sum != 0:
        r = (r / sum) * 6
        g = (g / sum) * 6
        b = (b / sum) * 6
    else:
        # Handle the case where total_sum is zero
        r, g, b = 0, 0, 0  # or any other default valu1

    return r, g, b

# print(average_image_color("D:\Downloads\soil.jpg"))

