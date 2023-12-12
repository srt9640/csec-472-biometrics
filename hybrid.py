import pixelAverage
import SIFT
import histogram
from tqdm import tqdm
import pathlib

# Obtain true path for script and data directory
SCRIPT_PATH = str(pathlib.Path(__file__).parent.resolve())
DATA_DIR = SCRIPT_PATH + "\\data\\images\\"

SIFT_RATIO = 0.7
HIST_DEFAULT_CORREL_RATIO = 1.0

def gatherConsensus(targetImage, referenceImage, MarginMaxTotal, MarginMinTotal, MarginStep):
    results = dict()
    for MarginMax in range( MarginMaxTotal, MarginMinTotal, MarginStep):
        consensus = 0

        pAvgResult = pixelAverage.evaluate(targetImage, referenceImage, MarginMax, MarginMinTotal, -1*MarginMax)
        siftResult = SIFT.evaluate(targetImage, referenceImage, MarginMax, MarginMinTotal, -1*MarginMax, SIFT_RATIO)
        histResult = histogram.calculate_difference(targetImage, referenceImage, MarginMax, MarginMinTotal, -1*MarginMax, HIST_DEFAULT_CORREL_RATIO)

        if pAvgResult[MarginMax]:
            consensus += 1 
        if siftResult[MarginMax]:
            consensus += 1 
        if histResult[MarginMax]:
            consensus += 1 
    
        results[MarginMax] = True if consensus >= 2 else False

    return results

def run(imageIndexStart,imageIndexEnd, imageDirectory, MarginMax, MarginMin, MarginStep):
    metrics = dict()

    for i in tqdm(range(imageIndexStart,imageIndexEnd), leave=False):
        i += 1
        testIndex = f'{i:04d}'
        failIndex = '0013' if i == 1 else f'{i-1:04d}'
        imagePaths = pixelAverage.getImagePaths(testIndex, failIndex, imageDirectory)

        # test for match with good pair
        results = gatherConsensus(imagePaths["target"], imagePaths["reference"], MarginMax, MarginMin, MarginStep)
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
        results = gatherConsensus(imagePaths["target"], imagePaths["failImage"], MarginMax, MarginMin, MarginStep)
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
        FARTotal += metrics[delta]["FRR"]
        FRRTotal += metrics[delta]["FAR"]
        count += 1
        print(f'Delta: {round(delta)} {metrics[delta]} ERR {round((metrics[delta]["FRR"] + metrics[delta]["FAR"])/2)}')

    print(f'Average FRR: {round(FRRTotal/count)}\nAverage FAR: {round(FARTotal/count)}\nAverage EER: {round(((FARTotal/count)+(FRRTotal/count))/2)}')

def main():
    imageIndexStart = 0
    imageIndexEnd = 2000
    imageDirectory = DATA_DIR
    MarginMax = 25
    MarginMin = 10
    MarginStep = -5
    
    run(imageIndexStart, imageIndexEnd, imageDirectory, MarginMax, MarginMin, MarginStep)

if __name__ == '__main__':
    main()