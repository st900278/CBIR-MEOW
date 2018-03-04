from scipy import spatial
import numpy as np
import cv2
from pymongo import *
import os
import os.path
import math
import json
import math
import sys
import time
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
'''
for directory in cat:
    print directory
    fileNum = 40
    for x in range(1, fileNum):
        data = caltech.find({'directory':directory, 'fileName': "image_%04d.jpg" % x})
        longName = directory + "/" + "image_%04d.jpg" % x
        ranksystem[longName] = 0
        index[longName] = {}
        for des in data:
            descriptors.append({'directory': directory, 'fileName': "image_%04d.jpg" % x, 'descriptor':des['descriptor']})
'''

for x in range(0, 1500):
    point = center_collection.find({'idx':x})
    for data in point:
        center.append(data['center'])
        center_hash[tuple(data['center'])] = x

for x in range(0, 1500):
    raw = invertIdx.find({'center':x})
    invertedIndex[tuple(center[x])] = {}
    #"invertedIndex[tuple(center[x])]['total'] = 0"
    for data in raw:
        invertedIndex[tuple(center[x])][data['fileName']] = {}
        invertedIndex[tuple(center[x])][data['fileName']]['appear'] = data['appear']
        "invertedIndex[tuple(center[x])]['total'] += data['appear']"
        if data['fileName'] not in ranksystem:
            ranksystem[data['fileName']] = 0
        if data['fileName'] in index:
            index[data['fileName']][tuple(center[x])] = {'appear': data['appear']}
        else:
            index[data['fileName']] = {}
            index[data['fileName']][tuple(center[x])] = {'appear': data['appear']}


print "TF-IDF"

for key, value in index.iteritems():
    s = 0
    dis = 0
    for key2, value2 in value.iteritems():
        s += value2['appear']
    for key2, value2 in value.iteritems():
        index[key][key2]['TF'] = value2['appear'] / float(s)
        dis += index[key][key2]['TF'] ** 2

    index[key]['euclidean'] = math.sqrt(dis)

'''
for x in center:
    for key, value in invertedIndex[tuple(x)].iteritems():
        if key == 'total': continue
        #invertedIndex[tuple(x)][key]['TF'] = invertedIndex[tuple(x)][key]['appear'] / float(invertedIndex[tuple(x)]['total'])
        invertedIndex[tuple(x)][key]['TF'] = index[key][tuple(x)] / float(sum(map(lambda k, v: v, index[key].iteritems())))
'''     
for key, value in invertedIndex.iteritems():
    invertedIndex[key]['IDF'] = 20 * 40 / float(len(invertedIndex[key])-1)


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


histogram = {} # query{1:1 2:4}
total = 0
# cat/image_0001.jpg

for x in des:
    # x in I
    cen = tree.query(x)[1]
    
    if cen in histogram:
        histogram[cen] += 1
    else:
        histogram[cen] = 1

lx = math.sqrt(sum(map(lambda v: (v / float(len(des)))**2, histogram)))

cens = {}
for x in des:
    cens[tuple(x)] = tree.query(x)[1]


for directory in cat:
    fileNum = 40
    for i in range(1, fileNum):
        data = caltech.find({'directory':directory, 'fileName': "image_%04d.jpg" % i})
        longName = directory + "/" + "image_%04d.jpg" % i
        if not os.path.isfile("./Caltech101/101_ObjectCategories/" + longName):continue
        print longName
        sim = 0
        # I
        print data.count(), len(des)
        for d in data:
            # (x,d)
            # y in I
            y = d['descriptor']
            cen1 = tree.query(y)[1]
            # Q
            total = 0
            for x in des:
                # x in I
                cen = cens[tuple(x)]
                if cen == cen1:
                    #kappa = ??
                    sigma = 10.0
                    
                    dst = spatial.distance.euclidean(x, y)
                    f = math.exp(-(dst**2)/(sigma**2))
                    idf = invertedIndex[tuple(center[cen])]['IDF']
                    sim += f * idf * idf
                
                
        sim = sim / (lx * index[longName]['euclidean'])
        ranksystem[longName] = sim
        print "rank", sim
        
    #for key, value in invertedIndex[tuple(center[cen])].iteritems():
    #    if key == 'total' or key == 'IDF': continue
    #    ranksystem[key] += value['TF']

data = ""
max_value = 0
print data

data = [(key, value) for key, value in ranksystem.iteritems()]
data.sort(key=lambda tup: tup[1], reverse=True)

for x in range(0, 10):
    print data[x]
