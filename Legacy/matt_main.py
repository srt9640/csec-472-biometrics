from PIL import Image, ImageFilter, ImageOps
import numpy as np
import matplotlib.pyplot as plt
import pathlib

def load_and_preprocess_image(image_path):
    # Load image with PIL and convert to grayscale
    img = Image.open(image_path).convert('L')

    # Apply a binary threshold
    img_bin = img.point(lambda p: p > 128 and 255)
    img_bin = ImageOps.invert(img_bin)

    return img_bin

def extract_minutiae(image):
    # Applying morphological operations using PIL is not as straightforward as in OpenCV.
    # PIL lacks some of the advanced image processing capabilities, specifically for minutiae extraction.
    # However, you can perform basic operations like edge detection as a placeholder.
    edges = image.filter(ImageFilter.FIND_EDGES)

    return edges

def visualize_results(original, extracted):
    plt.subplot(1, 2, 1)
    plt.imshow(original, cmap='gray')
    plt.title('Original Image')
    plt.axis('off')

    plt.subplot(1, 2, 2)
    plt.imshow(extracted, cmap='gray')
    plt.title('Extracted Minutiae')
    plt.axis('off')

    plt.show()

SCRIPT_PATH = str(pathlib.Path(__file__).parent.resolve())
DATA_DIR = SCRIPT_PATH + "\\data"

# Example usage
image_path = DATA_DIR + "\\png_txt\\figs_0\\f0001_01.png"
img = load_and_preprocess_image(image_path)
minutiae = extract_minutiae(img)

visualize_results(img, minutiae)
