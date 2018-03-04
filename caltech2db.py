import cv2
import numpy as np
from pymongo import *
import os

picture_root = "Caltech101/101_ObjectCategories/"
picture_data = {}

client = MongoClient()
db = client.multimedia
collection = db.caltech101_surf64

surf = cv2.xfeatures2d.SURF_create()
for dirPath, dirNames, fileNames in os.walk(picture_root):
    recentDirectory = dirPath.split("/")[-1]
    picture_data[recentDirectory] = []
    print recentDirectory
    for f in fileNames:
        picture_data[recentDirectory].append(os.path.join(dirPath, f))
        now_img = cv2.imread(os.path.join(dirPath, f))
        keypoints, descriptors = surf.detectAndCompute(now_img, None)
        pack = zip(keypoints, descriptors)
        for kp, des in pack:
            surf_data = {'directory': recentDirectory, 'fileName': f, 'descriptor': des.tolist(), 'keypoint': kp.pt}
            collection.insert(surf_data)

print "finish"
            
