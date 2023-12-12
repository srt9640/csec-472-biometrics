from PIL import Image
import os, re
from typing import Tuple, Dict
from tqdm import tqdm

WHITESPACE_ROWS = 32
WIDTH = 512
HEIGHT = 512
HEIGHT_ADJUSTED = HEIGHT - WHITESPACE_ROWS
TOTAL_PIXEL_COUNT = WIDTH * HEIGHT
TOTAL_PIXEL_COUNT_ADJUSTED = WIDTH * HEIGHT_ADJUSTED

DEFAULT_ALLOWED_DELTA = 80 # This is the threshold value for acceptance. 0 is the most strict.
DEFAULT_DELTA_LOWER_BOUND = -1
DEFAULT_DELTA_STEP = -5

DEFAULT_IMAGE_INDEX_END = 2000
DEFAULT_IMAGE_INDEX_START = 0
DEFAULT_IMAGE_DIRECTORY = "C:\\Users\\lukas\\Documents\\Fall2023\\CSEC472\\Lab4\\images\\"


def pixelAverage(image: str) -> float:
    """Call this through the evaluate function

    Args:
        image (str): path to image

    Returns:
        float: pixel average value
    """
    with Image.open(image) as openImage:
        pixelValueSum = 0
        for x in range(WIDTH):
            for y in range(HEIGHT_ADJUSTED):
                pixelCoordinates = (x, y)
                pixelValueSum += openImage.getpixel(pixelCoordinates)
        return pixelValueSum/TOTAL_PIXEL_COUNT_ADJUSTED
    
    
def evaluate(targetImage:str, referenceImage:str, allowedDelta:int, deltaLowerBound:int, deltaStep:int) -> Dict:
    """
    Iterates through a range of delta values defined by allowedDelta as the start, deltaLowerBound as the stop, and a negative deltaStep value to iterate through the range
    
    to check only one delta value, set deltaStep = -1*allowedDelta.

    Args:
        targetImage (str): Image being tested
        referenceImage (str): Image tested against
        allowedDelta (int): maximum allowed difference between the values for each image. 0 is the most strict. EER seems to be about 25.
        deltaLowerBound (int): minimum difference value to be tested
        deltaStep (int): step for iteration through the range of delta values

    Returns:
        Dictionary: a dictionary of results in the format {(int)delta:(bool)result}
    """
    results = dict()
    targetImagePixelAverage = pixelAverage(targetImage) 
    referenceImagePixelAverage = pixelAverage(referenceImage)
    for delta in range(allowedDelta, deltaLowerBound, deltaStep):
        upperBound = referenceImagePixelAverage + delta
        lowerBound = referenceImagePixelAverage - delta
        inBounds = False

        if (lowerBound <= targetImagePixelAverage) and (targetImagePixelAverage <= upperBound):
            inBounds = True

        results[delta] = inBounds

    return results

def getImagePaths(testImageIndex:str, failImageIndex:str, imageDirectory:str) -> Tuple[str, str, str]:
    """_summary_

    Args:
        testImageIndex (str): Image number for the intended test pair
        failImageIndex (str): Image number for FAR testing (false positive)
        imageDirectory (str): Path to image directory

    Returns:
        Tuple[str, str, str]: (path to target image, path to reference image, path to FAR testing image)
    """
    imagePaths = {"target":"", "reference":"", "failImage":""}
    prefix = {"target":"f", "reference":"s"}
    fileExtension = ".png"
    for fileName in os.listdir(imageDirectory):
        if re.match(f'{prefix["target"]}{testImageIndex}_\\d\\d{fileExtension}', fileName):
            imagePaths["target"] = f'{imageDirectory}{fileName}'
            imagePaths["reference"] = f'{imageDirectory}{prefix["reference"]}{fileName[1:]}'
        if re.match(f'{prefix["target"]}{failImageIndex}_\\d\\d{fileExtension}', fileName):
            imagePaths["failImage"] = f'{imageDirectory}{fileName}'
    return imagePaths

def run(allowedDelta:int=DEFAULT_ALLOWED_DELTA, deltaLowerBound:int=DEFAULT_DELTA_LOWER_BOUND, \
            deltaStep:int=DEFAULT_DELTA_STEP, imageDirectory:str=DEFAULT_IMAGE_DIRECTORY, \
            imageIndexStart:int=DEFAULT_IMAGE_INDEX_START, imageIndexEnd:int=DEFAULT_IMAGE_INDEX_END) -> None:
    metrics = {}

    for i in tqdm(range(imageIndexStart,imageIndexEnd), leave=False):
        i += 1
        testIndex = f'{i:04d}'
        failIndex = '0013' if i == 1 else f'{i-1:04d}'
        imagePaths = getImagePaths(testIndex, failIndex, imageDirectory)

        # test for match with good pair
        results = evaluate(imagePaths["target"], imagePaths["reference"], allowedDelta, deltaLowerBound, deltaStep)
        for delta in results.keys():
            if delta not in metrics.keys():
                metrics[delta] = {"Accept":0, "Reject":0, "FRR":0, "FAR":0, "TotalTested":0}
            if results[delta]:
                metrics[delta]["Accept"] += 1
            else:
                metrics[delta]["Reject"] += 1
                metrics[delta]["FRR"] += 1
            metrics[delta]["TotalTested"] += 1

        #test for match with intentionally bad pair
        results = evaluate(imagePaths["target"], imagePaths["failImage"], allowedDelta, deltaLowerBound, deltaStep)
        for delta in results.keys():        
            if results[delta]:
                metrics[delta]["Accept"] += 1
                metrics[delta]["FAR"] += 1
            else:
                metrics[delta]["Reject"] += 1
            metrics[delta]["TotalTested"] += 1
    
    count = 0
    FARTotal = 0
    FRRTotal = 0
    for delta in metrics.keys():
        FARTotal += metrics[delta]["FAR"]
        FRRTotal += metrics[delta]["FRR"]
        count += 1
        print(f'Delta: {delta} {metrics[delta]} ERR {round((metrics[delta]["FRR"] + metrics[delta]["FAR"])/2)}')

    print(f'Average FRR: {round(FRRTotal/count)}\nAverage FAR: {round(FARTotal/count)}\nAverage EER: {round(((FARTotal/count)+(FRRTotal/count))/2)}')

if __name__ == '__main__':
    run()