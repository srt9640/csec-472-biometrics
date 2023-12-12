import cv2
from pixelAverage import getImagePaths
from tqdm import tqdm

DEFAULT_CORRELATION_RATIO = 1.0

def calculate_difference(targetImage, referenceImage, MarginMax, MarginMin, MarginStep, histBaseline=DEFAULT_CORRELATION_RATIO):
    results = dict()
    
    targetHist = generate_histogram(targetImage)
    referenceHist = generate_histogram(referenceImage)

    diffHist = cv2.compareHist(targetHist, referenceHist, cv2.HISTCMP_CORREL)

    for margin in range(MarginMax, MarginMin, MarginStep):
        margin *= 0.01
        upperBound = histBaseline + margin
        lowerBound = histBaseline - margin
        inBounds = False

        if (lowerBound <= diffHist) and (diffHist <= upperBound):
            inBounds = True

        results[round(margin*100)] = inBounds

    return results

def generate_histogram(image):
    image = cv2.imread(image)
    histogram = cv2.calcHist([image],[0], None, [256], [0, 256])
    return histogram

def run(imageIndexStart,imageIndexEnd, imageDirectory, MarginMax, MarginMin, MarginStep):
    metrics = dict()

    for i in tqdm(range(imageIndexStart,imageIndexEnd), leave=False):
        i += 1
        testIndex = f'{i:04d}'
        failIndex = '0013' if i == 1 else f'{i-1:04d}'
        imagePaths = getImagePaths(testIndex, failIndex, imageDirectory)

        # test for match with good pair
        results = calculate_difference(imagePaths["target"], imagePaths["reference"], MarginMax, MarginMin, MarginStep)
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
        results = calculate_difference(imagePaths["target"], imagePaths["failImage"], MarginMax, MarginMin, MarginStep)
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
        print(f'Delta: {round(delta)} {metrics[delta]} ERR {round((metrics[delta]["FRR"] + metrics[delta]["FAR"])/2)}')

    print(f'Average FRR: {round(FRRTotal/count)}\nAverage FAR: {round(FARTotal/count)}\nAverage EER: {round(((FARTotal/count)+(FRRTotal/count))/2)}')

def main():
    imageIndexStart = 0
    imageIndexEnd = 2000
    imageDirectory = 'C:\\Users\\lukas\\Documents\\Fall2023\\CSEC472\\Lab4\\images\\'
    MarginMax = 80
    MarginMin = -1
    MarginStep = -5
    
    run(imageIndexStart, imageIndexEnd, imageDirectory, MarginMax, MarginMin, MarginStep)

if __name__ == '__main__':
    main()