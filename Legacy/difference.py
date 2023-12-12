from PIL import Image, ImageChops, ImageStat
import matplotlib.pyplot as plt
import  numpy as np
import pathlib

SCRIPT_PATH = str(pathlib.Path(__file__).parent.resolve())
DATA_DIR = SCRIPT_PATH + "\\data"

def load_image(image_path):
    return Image.open(image_path).convert('L')  # Convert to grayscale

def calculate_difference(image1, image2):
    margin = .25
    # Calculate raw difference
    diff = ImageChops.difference(image1, image2)

    # Convert to numpy array for processing
    np_diff = np.array(diff)

    # Apply margin of error
    np_diff[np.abs(np_diff) < margin] = 0
    print(np_diff)
    # Convert back to PIL Image
    return Image.fromarray(np_diff)
def generate_histogram(image):
    histogram = image.histogram()
    print(histogram)
    plt.hist(histogram, bins=512, range=(0, 256))
    plt.ylim(0,3)
    plt.title("Histogram of Image Difference")
    plt.show()
    return histogram

def hash_histogram(histogram):
    return hash(tuple(histogram))

print(DATA_DIR)
# Example Usage
image_path1 = DATA_DIR + "\\png_txt\\figs_0\\f0001_01.png"
image_path2 = DATA_DIR + "\\png_txt\\figs_0\\s0001_01.png"

img1 = load_image(image_path1)
img2 = load_image(image_path2)

diff_img = calculate_difference(img1, img2)
histogram = generate_histogram(diff_img)
histogram_hash = hash_histogram(histogram)

print("Hash of the Histogram:", histogram_hash)
