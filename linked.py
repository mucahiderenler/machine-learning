import os
import csv
import codecs
import matplotlib.pyplot as plt
import numpy

def plotdata(data,labels,name): #def function plotdata
#colors = ['black']
    fig, ax = plt.subplots()
    plt.scatter([row[0] for row in data], [row[1] for row in data], c=labels)
    ax.grid(True)
    fig.tight_layout()
    plt.title(name)
    plt.show()

infos = []

f = open('player_career.csv','r')
count = 0
try:
    datos = None
    reader = csv.DictReader(f)
    for row in reader:
        datos = []
        if row[('minutes')] == None or count == 1000 :
            break
        datos.append(row[('minutes')])
        datos.append(row[('pts')])
        datos.append(row[('reb')])
        datos.append(row[('asts')])
        datos.append(row[('stl')])
        datos.append(row[('blk')])
        infos.append(datos)
        count = count +1
finally:
    f.close()

import sklearn.cluster

from sklearn import preprocessing

min_max_scaler = preprocessing.MinMaxScaler()
norminfo = min_max_scaler.fit_transform(infos)

# 2. Compute the similarity matrix
dist = sklearn.neighbors.DistanceMetric.get_metric('euclidean')
matsim = dist.pairwise(norminfo)
avSim = numpy.average(matsim)
print "%s\t%6.2f" % ('Average Distance', avSim)

from scipy import cluster
clusters = cluster.hierarchy.linkage(matsim, method = 'complete')
cluster.hierarchy.dendrogram(clusters,color_threshold=0)
plt.show()

labels = cluster.hierarchy.fcluster(clusters, 30, criterion = 'distance')
plotdata(infos,labels, 'hierarchical single')

model = sklearn.cluster.AgglomerativeClustering(n_clusters=3,linkage="complete", affinity='euclidean')
labels = model.fit_predict(infos)

plotdata(infos,labels, 'hierarchical ward')