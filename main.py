''' Imports for...
- os:       OS commands
- cv2:      OpenCV import for image manipulation
- pathlib:  Obtain path directories
'''

import os, cv2, pathlib



''' Initialization of all variables
'''

# Obtain true path for script and data directory
SCRIPT_PATH = str(pathlib.Path(__file__).parent.resolve())
DATA_DIR = SCRIPT_PATH + "\\data"

# Training data numbers
TRAIN_MAX = 1499
TEST_MAX = 2000

# Optional resizing of image
# sample = cv2.resize(sample, None, fx=2.5, fy=2.5)

#Best match score
best_score = 0

# Initialize filename (string)
filename = None

# Initialize image
image = None

kp1, kp2, mp = None, None, None



''' Start of functions
'''

def iterate(analysis_choice):
    # Loop through all data files for images
    for subdir, dirs, files in os.walk(DATA_DIR):
        for file in files:
            if file[0] == 'f':
                # Split data into [name, file_format]
                data = file.split('.')

                if data[1] == 'png':
                    if (int(file[1:5]) <= TRAIN_MAX):
                        print(file)
                    elif (int(file[1:5]) <= TEST_MAX):
                        print('here')


def main():
    # Numbers in analysis_choice list will correlate to which methods to be applied.
    analysis_choice = [0]
    iterate(analysis_choice)

main()



'''
# Input for image
# sample = cv2.imread("")

for file in [file for file in os.listdir()]:
    fingerprint_image = cv2.imread("" + file)

    
# Show image and delete window shortly after
cv2.imshow("Sample", sample)
cv2.waitKey(0)
cv2.destroyAllWindows
'''

