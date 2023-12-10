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

# Optional resizing of image
# sample = cv2.resize(sample, None, fx=2.5, fy=2.5)

#Best match score
best_score = 0

# Initialize filename (string)
filename = None

# Initialize image
image = None

kp1, kp2, mp = None, None, None

# Input for image
# sample = cv2.imread("")



''' Start of functions
'''

for subdir, dirs, files in os.walk(DATA_DIR):
    for file in files:
        print (file)

'''
for file in [file for file in os.listdir()]:
    fingerprint_image = cv2.imread("" + file)
'''
''' Test comments
cv2.imshow("Sample", sample)
cv2.waitKey(0)
cv2.destroyAllWindows
'''

