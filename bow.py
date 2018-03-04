from scipy import spatial
import numpy as np
import cv2
from pymongo import *
import os
import math
import json
from ast import literal_eval
client = MongoClient()
db = client.multimedia
caltech = db.caltech101_surf64
idx = db.index2
invertIdx = db.invertIdx2
center_collection = db.center2

descriptors = []
descriptorList = []
directoryList = os.listdir("./Caltech101/101_ObjectCategories")

index = {}
ranksystem= {}
limm = 0

with open("picture_list2.txt", "r") as f:
    cat = f.read().splitlines()

for directory in cat:
    print directory

    '''
    fileNum = len(os.listdir("./Caltech101/101_ObjectCategories/" + directory))/2
    if fileNum > 100: fileNum = 100
    '''
    fileNum = 40
    for x in range(1, fileNum):
        data = caltech.find({'directory':directory, 'fileName': "image_%04d.jpg" % x})
        longName = directory + "/" + "image_%04d.jpg" % x
        ranksystem[longName] = 0
        index[longName] = {}
        for des in data:
            descriptors.append({'directory': directory, 'fileName': "image_%04d.jpg" % x, 'descriptor':des['descriptor']})

tmp = [ des['descriptor'] for des in descriptors]
descriptorList = np.float32(tmp)

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 2)

ret,label,center=cv2.kmeans(descriptorList, 1500, None, criteria,5,cv2.KMEANS_PP_CENTERS)

invertedIndex = {}
for x in center:
    invertedIndex[tuple(x)] = {}


print "create inverted"
"create inverted index and index"
for x in range(0, len(label)):
    fileName = descriptors[x]['directory'] + "/" + descriptors[x]['fileName']
    if fileName in invertedIndex[tuple(center[label[x][0]])]:
        invertedIndex[tuple(center[label[x][0]])][fileName]['appearTimes'] += 1
    else:
        invertedIndex[tuple(center[label[x][0]])][fileName] = {} 
        invertedIndex[tuple(center[label[x][0]])][fileName]['appearTimes'] = 1

    if "total" in invertedIndex[tuple(center[label[x][0]])]:
        invertedIndex[tuple(center[label[x][0]])]['total'] += 1
    else: invertedIndex[tuple(center[label[x][0]])]['total'] = 1


    if tuple(center[label[x][0]]) in index[fileName]:
        index[fileName][tuple(center[label[x][0]])] += 1
    else: index[fileName][tuple(center[label[x][0]])] = 1

center_hash = {}

for x in range(0, len(center)):
    center_collection.insert({'idx': x, 'center': center[x].tolist()})
    center_hash[tuple(center[x])] = x



for x in center:
    for key, value in invertedIndex[tuple(x)].iteritems():
        if key == 'total': continue
        invertIdx.insert({'center': center_hash[tuple(x)], 'fileName': key, 'appear': value['appearTimes']})

for key in index.iterkeys():
    for key2 in index[key].iterkeys():
        idx.insert({'fileName': key, 'center': center_hash[key2], 'appear': index[key][key2]})






