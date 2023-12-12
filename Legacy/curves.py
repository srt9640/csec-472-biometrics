import cv2
import numpy as np
import os

MARGIN = 0.1


def fingerprint(original_path, path_to_images):
    sample = cv2.imread(original_path)
    image, filename, kp1, kp2, mp = None, None, None, None, None
    best_score = 0
    for file in [file for file in os.listdir(path_to_images)]:
        fingerprint_image = cv2.imread(original_path + "/" + file)
        sift = cv2.SIFT()
        keypoints_1, descriptions_1 = sift.detectAndCompute(sample, None)
        keypoints_2, descriptions_2 = sift.detectAndCompute(fingerprint_image, None)
        matches = cv2.FlannBasedMatcher({'algorithm': 1, 'trees': 10}, {}).knnMatch(descriptions_1, descriptions_2, k=2)
        match_points = []
        for p, q in matches:
            if p.distance < MARGIN * q.distance:
                match_points.append(p)
        keypoints = 0
        if len(keypoints_1) < len(keypoints_2):
            keypoints = len(keypoints_1)
        else:
            keypoints = len(keypoints_2)
        if(len(match_points)/keypoints * 100 > best_score):
            best_score = len(match_points)/keypoints * 100
            filename = file
            image = fingerprint_image
            kp1,kp2,mp = keypoints_1,keypoints_2,match_points
            return filename,best_score


def main():
    #Loop through whatever directory you have all the original images in
    path = '' #Path for original photos
    path2 = '' #Path for matching photos
    Threshold = 10 #This is very low but this is basically the similarity score we are gonna use
    for file in os.listdir(path):
        filename,best_score = fingerprint(file,path2)
        if best_score >= Threshold:
            #Score is valid enough so now just make sure that it chose the right file i.e. we load in file f_0001 we recieved s_0001 as the output
            continue
