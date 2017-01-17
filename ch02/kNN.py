#!/usr/bin/python
#-*-coding:utf-8-*-
from numpy import *
import operator
import dircache
def createDataSet():
    group = array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]])
    labels = ['A','A','B','B']
    return group, labels
    
def classify0(inX, dataSet, labels, k):
    dataSetSize = dataSet.shape[0]
    diffMat = tile(inX, (dataSetSize,1)) - dataSet
    sqDiffMat = diffMat**2
    sqDistances = sqDiffMat.sum(axis=1)
    distances = sqDistances**0.5
    sortedDistIndicies = distances.argsort()    
    classCount={}          
    for i in range(k):
        voteIlabel = labels[sortedDistIndicies[i]]
        classCount[voteIlabel] = classCount.get(voteIlabel,0) + 1
    #print(classCount)
    sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
    #print(sortedClassCount)
    return sortedClassCount[0][0]
  
def file2matrix(filename):
    fr = open(filename)
    arrayOLines = fr.readlines()  #lines of file 
    numberOfLines = len(arrayOLines) #number of lines
    returnMat = zeros((numberOfLines,3))
    classLabelVector = []
    index = 0
    for line in arrayOLines:
        line = line.strip()
        listFromLine = line.split('\t')
        returnMat[index,:] = listFromLine[0:3]
        classLabelVector.append(int(listFromLine[-1]))
        index += 1
    #print(classLabelVector,returnMat)
    return returnMat,classLabelVector
    
def autoNorm(dataSet):
    minVals = dataSet.min(0)
    maxVals = dataSet.max(0)
    ranges = maxVals - minVals
    normDataSet = zeros(shape(dataSet))
    m = dataSet.shape[0]
    normDataSet = dataSet - tile(minVals, (m,1))
    normDataSet = normDataSet/tile(ranges, (m,1))
    return normDataSet, ranges ,minVals
    
def datingClassTest():
    haRatio = 0.10
    datingDataMat,datingLabels = file2matrix('/Users/wakemeup/Documents/MLiA/ch02/datingTestSet2.txt')
    normMat, ranges, minVals = autoNorm(datingDataMat)
    m = normMat.shape[0]
    numTestVecs = int(m * haRatio)
    errorCount = 0.0
    for i in range(numTestVecs):
        classifierResult = classify0(normMat[i,:], normMat[numTestVecs:m,:],datingLabels[numTestVecs:m],3)
        print "the classifier came back with: %d,the real answer is: %d" % (classifierResult,datingLabels[i])
        if (classifierResult != datingLabels[i]) : errorCount += 1.0
    print "the total error rate is: %f" % (errorCount/float(numTestVecs))
    
    
def img2vector(filename):
    returnVect = zeros((1,1024));
    fr = open(filename)
    for i in range(32):
        lineStr = fr.readline()
        for j in range(32):
            returnVect[0,32*i+j] = int(lineStr[j])
    return returnVect


def handwritingClassTest():
    hwLabels = []
    trainingFileList = dircache.listdir('/Users/wakemeup/Documents/MLiA/ch02/digits/trainingDigits')
    m = len(trainingFileList) 
    #print(m)
    trainingMat = zeros((m-1,1024))
    #print(trainingMat)
    for i in range(1,m):
        #print(trainingFileList)
        fileNameStr = trainingFileList[i]   
        fileStr = fileNameStr.split('.')[0]
        #print('fileStr = %s' % fileStr)
        classNumStr = int(fileStr.split('_')[0])
        #print('classNumStr = %d' % classNumStr)
        hwLabels.append(classNumStr)
        trainingMat[i-1,:] = img2vector('/Users/wakemeup/Documents/MLiA/ch02/digits/trainingDigits/%s' % fileNameStr)
        #print(trainingMat[i,:])
    testFileList = dircache.listdir('/Users/wakemeup/Documents/MLiA/ch02/digits/testDigits')
    errorCount = 0.0
    mTest = len(testFileList) #减去的是 .DS_Store 
    for i in range(1,mTest):
        fileNameStr = testFileList[i]
        fileStr = fileNameStr.split('.')[0]
        classNumStr = int(fileStr.split('_')[0])
        vectorUnderTest = img2vector('/Users/wakemeup/Documents/MLiA/ch02/digits/testDigits/%s' % fileNameStr)
        classifierResult = classify0(vectorUnderTest,trainingMat,hwLabels,3)
        print "the classifier came back with: %d,the real answer is %d" % (classifierResult,classNumStr)
        if (classifierResult != classNumStr) : errorCount += 1.0
    print "\nthe total number of errors is: %d" % errorCount
    print "\nthe total error rate is : %f" % (errorCount/float(mTest))


handwritingClassTest()

