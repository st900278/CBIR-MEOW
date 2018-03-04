from scipy import spatial
import numpy as np
import cv2
from pymongo import *
import os
import math
import json
import math
import sys
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
invertedIndex = {}

ranksystem = {}
center = []
center_hash = {}

if len(sys.argv) < 2:
    print 'no argument'
    sys.exit()
option = sys.argv[1]
query_img = option
print query_img



with open("picture_list2.txt", "r") as f:
    cat = f.read().splitlines()

for x in range(0, 1500):
    point = center_collection.find({'idx':x})
    for data in point:
        center.append(data['center'])
        center_hash[tuple(data['center'])] = x

for x in range(0, 1500):
    raw = invertIdx.find({'center':x})
    invertedIndex[tuple(center[x])] = {}
    invertedIndex[tuple(center[x])]['total'] = 0
    for data in raw:
        invertedIndex[tuple(center[x])][data['fileName']] = {}
        invertedIndex[tuple(center[x])][data['fileName']]['appear'] = data['appear']
        invertedIndex[tuple(center[x])]['total'] += data['appear']
        if data['fileName'] not in ranksystem:
            ranksystem[data['fileName']] = 0
        if data['fileName'] in index:
            index[data['fileName']][tuple(center[x])] = data['appear']
        else:
            index[data['fileName']] = {}
            index[data['fileName']][tuple(center[x])] = data['appear']


print "TF-IDF"

for x in center:
    for key, value in invertedIndex[tuple(x)].iteritems():
        if key == 'total': continue
        invertedIndex[tuple(x)][key]['TF'] = invertedIndex[tuple(x)][key]['appear'] / float(invertedIndex[tuple(x)]['total'])

for key, value in invertedIndex.iteritems():
    invertedIndex[key]['IDF'] = math.log(20 * 40 / float(len(invertedIndex[key])-1), 10)


'''
for directory in cat:
    print directory
    for files in range(1, 20):
        print "image_%04d.jpg" % files
        i = 0
        fileName = directory + "/" + "image_%04d.jpg" % files
        sorted_data = sorted(index[fileName].iteritems(), key=lambda (k,v): invertedIndex[tuple(k)][fileName]['TF'] * invertedIndex[tuple(k)]['IDF'], reverse=True)
        
        for key, value in sorted_data:
            print "%s: %s" % (center_hash[key], value)
            i+=1
            if i > 10: break
'''

tree = spatial.KDTree(center)

surf = cv2.xfeatures2d.SURF_create()
img = cv2.imread(query_img, 0)
kp, des = surf.detectAndCompute(img, None)


query = {}
for x in des:
    cen = tree.query(x)[1]
    for key, value in invertedIndex[tuple(center[cen])].iteritems():
        if key == 'total' or key == 'IDF': continue
        ranksystem[key] += value['TF']


data = ""
max_value = 0
print data

data = [(key, value) for key, value in ranksystem.iteritems()]
data.sort(key=lambda tup: tup[1], reverse=True)

for x in range(0, 5):
    print data[x]

