from numpy import *

def loadDataSet(fileName):
    dataMat = []
    fr = open(fileName)
    for line in fr.readlines():
        curLine = line.strip().split('\t')
        fltLine = map(float,curLine) 
        dataMat.append(fltLine)
    return dataMat

def distEclud(vecA,vecB):    #计算两个向量的距离
    return sqrt(sum(power(vecA - vecB, 2)))

def randCent(dataSet, k):  
    n = shape(dataSet)[1]
    centroids = mat(zeros((k,n)))  # centroids  质心     
    for j in range(n):
        minJ = min(dataSet[:,j])
        rangeJ = float(max(dataSet[:,j]) - minJ)  #最大减最小
        centroids[:,j] = minJ + rangeJ * random.rand(k,1)
    return centroids  #包含k个随机质心的集合


def kMeans(dataSet, k, distMeas = distEclud, createCent = randCent):
    m = shape(dataSet)[0]
    clusterAssment = mat(zeros((m,2)))   #cluster means 簇
    centroids = createCent(dataSet, k)
    clusterChanged = True
    while clusterChanged:
        clusterChanged =False
        for i in range(m):   # 对于每个数据点
            minDist = inf; minIndex = -1
            for j in range(k):  #对于每个质心
                distJI = distMeas(centroids[j,:],dataSet[i,:])
                if distJI < minDist:
                    minDist = distJI; minIndex = j
            if clusterAssment[i,0] != minIndex : clusterChanged = True
            clusterAssment[i,:] = minIndex,minDist**2
        print centroids
        for cent in range(k):    #更新质心的位置？
            ptsInClust = dataSet[nonzero(clusterAssment[:,0].A == cent)[0]]
            centroids[cent,:] = mean(ptsInClust, axis = 0)
    return centroids,clusterAssment

def biKmeans(dataSet, k, distMeas = distEclud):
    m = shape(dataSet)[0]
    clusterAssment = mat(zeros((m,2)))
    centroid0 = mean(dataSet, axis = 0).tolist()[0]
    centList = [centroid0]     #创建初始簇
    print "centroid0 = " , centroid0 
    for j in range(m):
        clusterAssment[j,1] = distMeas(mat(centroid0), dataSet[j,:])**2
    while (len(centList) < k):
        lowestSSE = inf
        print "len(centList) = ",len(centList)
        for i in range(len(centList)):
            ptsInCurrCluster = dataSet[nonzero(clusterAssment[:,0].A == i)[0],:]
            centroidMat, splitClustAss = kMeans(ptsInCurrCluster, 2, distMeas)
            sseSplit = sum(splitClustAss[:,1])
            sseNotSplit = sum(clusterAssment[nonzero(clusterAssment[:,0].A != i)[0],1])
            print "sseSplit, and notSplit: ",sseSplit,sseNotSplit
            if (sseSplit + sseNotSplit) < lowestSSE:
                bestCenToSplit = i
                bestNewCents = centroidMat
                bestClustAss = splitClustAss.copy()
                lowestSSE = sseSplit + sseNotSplit
        bestClustAss[nonzero(bestClustAss[:,0].A == 1)[0],0] = len(centList)
        bestClustAss[nonzero(bestClustAss[:,0].A == 0)[0],0] = bestCenToSplit
        print 'the bestCenToSplit is' , bestCenToSplit
        print "the len of bestClustAss is ", len(bestClustAss)
        centList[bestCenToSplit] = bestNewCents[0,:]
        centList.append(bestNewCents[1,:].tolist()[0])
        clusterAssment[nonzero(clusterAssment[:,0].A == bestCenToSplit)[0],:] = bestClustAss
    print(centList)
    return mat(centList), clusterAssment



"""
def biKmeans(dataSet, k, distMeas=distEclud):
    m = shape(dataSet)[0]
    clusterAssment = mat(zeros((m,2)))
    centroid0 = mean(dataSet, axis=0).tolist()[0]
    centList =[centroid0] #create a list with one centroid
    for j in range(m):#calc initial Error
        clusterAssment[j,1] = distMeas(mat(centroid0), dataSet[j,:])**2
    while (len(centList) < k):
        lowestSSE = inf
        for i in range(len(centList)):
            ptsInCurrCluster = dataSet[nonzero(clusterAssment[:,0].A==i)[0],:]#get the data points currently in cluster i
            centroidMat, splitClustAss = kMeans(ptsInCurrCluster, 2, distMeas)
            sseSplit = sum(splitClustAss[:,1])#compare the SSE to the currrent minimum
            sseNotSplit = sum(clusterAssment[nonzero(clusterAssment[:,0].A!=i)[0],1])
            print "sseSplit, and notSplit: ",sseSplit,sseNotSplit
            if (sseSplit + sseNotSplit) < lowestSSE:
                bestCentToSplit = i
                bestNewCents = centroidMat
                bestClustAss = splitClustAss.copy()
                lowestSSE = sseSplit + sseNotSplit
        bestClustAss[nonzero(bestClustAss[:,0].A == 1)[0],0] = len(centList) #change 1 to 3,4, or whatever
        bestClustAss[nonzero(bestClustAss[:,0].A == 0)[0],0] = bestCentToSplit
        print 'the bestCentToSplit is: ',bestCentToSplit
        print 'the len of bestClustAss is: ', len(bestClustAss)
        centList[bestCentToSplit] = bestNewCents[0,:].tolist()[0]#replace a centroid with two best centroids 
        centList.append(bestNewCents[1,:].tolist()[0])
        clusterAssment[nonzero(clusterAssment[:,0].A == bestCentToSplit)[0],:]= bestClustAss#reassign new clusters, and SSE
    return mat(centList), clusterAssment
                
"""


import urllib
import json
def geoGrab(stAddress,city):
    apiStem = 'http://where.yahooapis.com/geocode?'
    params = {}
    params['flags'] = 'J'
    params['appid'] = 'ppp68N8t'
    params['location'] = '%s %s' % (stAddress, city)
    url_params = urllib.urlencode(params)
    yahhoApi = apiStem + url_params
    print yahhoApi
    c = urllib.urlopen(yahhoApi)
    return json.loads(c.read())

from time import sleep
def massPlaceFind(fileName):
    fw = open('/Users/wakemeup/Documents/MLiA/ch10/places.txt','w')
    for line in open(fileName).readlines():
        line = line.strip()
        lineArr = line.split('\t')
        retDict = geoGrab(lineArr[1],lineArr[2])
        if retDict['ResultSet']['Error'] == 0:
            lat = float(retDict['ResultSet']['Results'][0]['latitude'])
            lng = float(retDict['ResultSet']['Results'][0]['longitude'])
            print "%s\t%f\t%f\n" % (lineArr[0], lat, lng)
            fw.write('%s\t%f\t%f\n'  % (line, lat, lng))
        else: print "error fetching"
        sleep(1)
    fw.close


"""
datMat = mat(loadDataSet('/Users/wakemeup/Documents/MLiA/ch10/testSet.txt'))
print(randCent(datMat, 2))
print(distEclud(datMat[0],datMat[1]))
"""

"""
datMat = mat(loadDataSet('/Users/wakemeup/Documents/MLiA/ch10/testSet.txt'))
myCentroids, clustAssing = kMeans(datMat, 4)
print(myCentroids)
"""

"""
datMat3 = mat(loadDataSet('/Users/wakemeup/Documents/MLiA/ch10/testSet2.txt'))
centList, myNewAssments = biKmeans(datMat3,3)
print(centList)
"""
#geoResults = geoGrab('1 VA Center','Augusta, ME')

