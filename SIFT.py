import cv2
from tqdm import tqdm
from pixelAverage import getImagePaths

MARGIN = 0.7

def fingerprint(testImage, referenceImage, ratio=MARGIN):
    sample = cv2.imread(referenceImage)
    score = 0
    #for file in [file for file in os.listdir(path_to_images)]:
    fingerprint_image = cv2.imread(testImage)
    sift = cv2.SIFT_create()
    keypoints_1, descriptions_1 = sift.detectAndCompute(sample, None)
    keypoints_2, descriptions_2 = sift.detectAndCompute(fingerprint_image, None)
    matches = cv2.FlannBasedMatcher({'algorithm': 1, 'trees': 10}, {}).knnMatch(descriptions_1, descriptions_2, k=2)
    match_points = []
    for p, q in matches:
        if p.distance < ratio * q.distance:
            match_points.append(p)
    keypoints = 0
    if len(keypoints_1) < len(keypoints_2):
        keypoints = len(keypoints_1)
    else:
        keypoints = len(keypoints_2)
    if(len(match_points)/keypoints * 100 > score):
        score = len(match_points)/keypoints * 100

    return score

def evaluate(targetImage:str, referenceImage:str, ThresholdMax, ThresholdMin, ThresholdStep, ratio):
    results = dict()
    score = fingerprint(targetImage,referenceImage, ratio)
    for delta in range(ThresholdMax, ThresholdMin, ThresholdStep):
        inBounds = False
        for scale in range(ThresholdMax, ThresholdMin, ThresholdStep):
            currentThreshold = scale*0.01
            if score >= currentThreshold:
                inBounds = True
        results[delta] = inBounds

    return results

def run(imageDirectory, imageIndexStart, imageIndexEnd, ThresholdMax, ThresholdMin, ThresholdStep, ratio):

    results = dict()

    for i in tqdm(range(imageIndexStart,imageIndexEnd), leave=False, disable=False):

        testIndex = f'{i+1:04d}'
        failIndex = '0013' if i+1 == 1 else f'{i:04d}'
        imagePaths = getImagePaths(testIndex, failIndex, imageDirectory)

        intendedAcceptScore = fingerprint(imagePaths["target"],imagePaths["reference"], ratio)
        intendedFailScore = fingerprint(imagePaths["target"],imagePaths["failImage"], ratio)
        
        for scale in range(ThresholdMax, ThresholdMin, ThresholdStep):
            currentThreshold = scale*0.01
            if currentThreshold not in results.keys():
                results[currentThreshold] = {"Accept":0, "Reject":0, "FRR":0, "FAR":0, "TotalTested":0, "None":0}
            
            results[currentThreshold]["TotalTested"] += 2

            if intendedAcceptScore >= currentThreshold:
                results[currentThreshold]["Accept"] += 1
            else:
                results[currentThreshold]["Reject"] += 1
                results[currentThreshold]["FRR"] += 1
            
            if intendedFailScore >= currentThreshold:
                results[currentThreshold]["Accept"] += 1
                results[currentThreshold]["FAR"] += 1
            else:
                results[currentThreshold]["Reject"] += 1
    
    return results

def main():
    #Loop through whatever directory you have all the original images in
    imageIndexStart = 0
    imageIndexEnd = 2000
    path = 'C:\\Users\\lukas\\Documents\\Fall2023\\CSEC472\\Lab4\\images\\' #Path for original photos
    ThresholdStep = -5
    ThresholdMax = 80 # 30 seems to be optimal for the ratio = 0.7
    ThresholdMin = -1
    ratio = 0.7

    results = run(path, imageIndexStart, imageIndexEnd, ThresholdMax, ThresholdMin, ThresholdStep, ratio)

    count = 0
    FARTotal = 0
    FRRTotal = 0
    for threshold in results.keys():
        count += 1
        FRRTotal += results[threshold]["FRR"]
        FARTotal += results[threshold]["FAR"]
        print(f'Threshold: {round(threshold * 100)} {results[threshold]} EER {round((results[threshold]["FAR"] + results[threshold]["FRR"]) / 2)}')

    print(f'Average FRR: {round(FRRTotal/count)}\nAverage FAR: {round(FARTotal/count)}\nAverage EER: {round(((FARTotal/count)+(FRRTotal/count))/2)}')


if __name__ == '__main__':
    main()